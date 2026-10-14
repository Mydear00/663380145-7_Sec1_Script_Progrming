"""Business logic for the Enhanced Task Manager."""

from datetime import date

from .task import Task, DueDateTask, PriorityTask
from .data_persistence import DataPersistence


class TaskManager:
    """Manage tasks, including CRUD, search, filtering, and sorting."""

    PRIORITY_ORDER = {
        "High": 1,
        "Medium": 2,
        "Low": 3,
    }

    def __init__(self, data_file="data/tasks.json"):
        self.persistence = DataPersistence(data_file)
        self.tasks = self.persistence.load_tasks()
        self.next_id = self._get_next_id()

    def _get_next_id(self):
        """Return the next unique task ID."""
        return max(
            (task.id for task in self.tasks),
            default=0,
        ) + 1

    def _save(self):
        """Save current tasks to JSON."""
        self.persistence.save_tasks(self.tasks)

    @staticmethod
    def _parse_date(value):
        """Convert a date string to a date object when necessary."""
        if value is None or value == "":
            return None

        if isinstance(value, date):
            return value

        if isinstance(value, str):
            try:
                return date.fromisoformat(value)
            except ValueError as error:
                raise ValueError(
                    "Date must use YYYY-MM-DD format."
                ) from error

        raise TypeError("Date must be a date object or a date string.")

    def add_normal_task(self, description, tags=None):
        """Add a normal task."""
        task = Task(
            task_id=self.next_id,
            description=description,
            tags=tags,
        )

        self.tasks.append(task)
        self.next_id += 1
        self._save()

        return task

    def add_due_date_task(self, description, due_date, tags=None):
        """Add a task with a due date."""
        task = DueDateTask(
            task_id=self.next_id,
            description=description,
            due_date=due_date,
            tags=tags,
        )

        self.tasks.append(task)
        self.next_id += 1
        self._save()

        return task

    def add_priority_task(self, description, priority, tags=None):
        """Add a task with a priority."""
        task = PriorityTask(
            task_id=self.next_id,
            description=description,
            priority=priority,
            tags=tags,
        )

        self.tasks.append(task)
        self.next_id += 1
        self._save()

        return task

    def get_task_by_id(self, task_id):
        """Find a task using its ID."""
        return next(
            (task for task in self.tasks if task.id == task_id),
            None,
        )

    def get_all_tasks(self):
        """Return all tasks."""
        return list(self.tasks)

    def complete_task(self, task_id):
        """Mark a task as completed."""
        task = self.get_task_by_id(task_id)

        if task is None:
            return False, "Task not found."

        if task.completed:
            return False, "Task is already completed."

        task.mark_complete()
        self._save()

        return True, "Task marked as completed."

    def delete_task(self, task_id):
        """Delete a task by its ID."""
        task = self.get_task_by_id(task_id)

        if task is None:
            return False, "Task not found."

        self.tasks.remove(task)
        self._save()

        return True, "Task deleted successfully."

    def add_tag(self, task_id, tag):
        """Add a tag to an existing task."""
        task = self.get_task_by_id(task_id)

        if task is None:
            return False, "Task not found."

        if not task.add_tag(tag):
            return False, "Tag is empty or already exists."

        self._save()
        return True, "Tag added successfully."

    def remove_tag(self, task_id, tag):
        """Remove a tag from an existing task."""
        task = self.get_task_by_id(task_id)

        if task is None:
            return False, "Task not found."

        if not task.remove_tag(tag):
            return False, "Tag not found."

        self._save()
        return True, "Tag removed successfully."

    def search_tasks(self, keyword):
        """
        Search task descriptions and tags.

        Matching is case-insensitive and supports partial keywords.
        """
        if not isinstance(keyword, str) or not keyword.strip():
            return []

        keyword = keyword.strip().casefold()

        return [
            task
            for task in self.tasks
            if keyword in task.description.casefold()
            or any(
                keyword in tag.casefold()
                for tag in task.tags
            )
        ]

    def filter_tasks(
        self,
        status=None,
        due_date_before=None,
        due_date_after=None,
        priority_level=None,
        contains_tags=None,
    ):
        """
        Filter by status, due date, priority, and tags.

        Multiple supplied criteria are combined using AND.
        """
        results = list(self.tasks)

        if status is not None:
            if isinstance(status, str):
                normalized_status = status.strip().casefold()

                if normalized_status in {"completed", "done", "true"}:
                    status = True
                elif normalized_status in {"pending", "incomplete", "false"}:
                    status = False
                else:
                    raise ValueError(
                        "Status must be completed, pending, True, or False."
                    )

            if not isinstance(status, bool):
                raise TypeError("Status must be a boolean or valid status string.")

            results = [
                task for task in results
                if task.completed == status
            ]

        before = self._parse_date(due_date_before)
        after = self._parse_date(due_date_after)

        if before is not None:
            results = [
                task for task in results
                if isinstance(task, DueDateTask)
                and task.due_date <= before
            ]

        if after is not None:
            results = [
                task for task in results
                if isinstance(task, DueDateTask)
                and task.due_date >= after
            ]

        if priority_level is not None and str(priority_level).strip():
            priority = str(priority_level).strip().capitalize()

            if priority not in self.PRIORITY_ORDER:
                raise ValueError("Priority must be High, Medium, or Low.")

            results = [
                task for task in results
                if isinstance(task, PriorityTask)
                and task.priority == priority
            ]

        if contains_tags:
            if isinstance(contains_tags, str):
                contains_tags = contains_tags.split(",")

            wanted_tags = {
                tag.strip().casefold()
                for tag in contains_tags
                if isinstance(tag, str) and tag.strip()
            }

            if wanted_tags:
                results = [
                    task for task in results
                    if wanted_tags.issubset(
                        {tag.casefold() for tag in task.tags}
                    )
                ]

        return results

    def sort_tasks(self, criterion="id", reverse=False):
        """
        Sort tasks by ID, description, completion, due date, or priority.

        Tasks without due dates or priorities are placed last for those
        respective sorting criteria.
        """
        criterion = criterion.strip().casefold()

        if criterion == "id":
            return sorted(
                self.tasks,
                key=lambda task: task.id,
                reverse=reverse,
            )

        if criterion == "description":
            return sorted(
                self.tasks,
                key=lambda task: task.description.casefold(),
                reverse=reverse,
            )

        if criterion in {"completed", "status"}:
            return sorted(
                self.tasks,
                key=lambda task: (task.completed, task.id),
                reverse=reverse,
            )

        if criterion in {"due_date", "due date"}:
            with_dates = [
                task for task in self.tasks
                if isinstance(task, DueDateTask)
            ]

            without_dates = [
                task for task in self.tasks
                if not isinstance(task, DueDateTask)
            ]

            with_dates.sort(
                key=lambda task: (task.due_date, task.id),
                reverse=reverse,
            )
            without_dates.sort(key=lambda task: task.id)

            return with_dates + without_dates

        if criterion == "priority":
            with_priority = [
                task for task in self.tasks
                if isinstance(task, PriorityTask)
            ]

            without_priority = [
                task for task in self.tasks
                if not isinstance(task, PriorityTask)
            ]

            with_priority.sort(
                key=lambda task: (
                    self.PRIORITY_ORDER[task.priority],
                    task.id,
                ),
                reverse=reverse,
            )
            without_priority.sort(key=lambda task: task.id)

            return with_priority + without_priority

        raise ValueError(
            "Unknown sorting criterion. Use id, description, "
            "completed, due_date, or priority."
        )