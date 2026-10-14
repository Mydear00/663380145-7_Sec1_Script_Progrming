
"""Business logic for managing tasks."""

import datetime

from .task import Task, DueDateTask, PriorityTask
from .data_persistence import DataPersistence


class TaskManager:
    """Manage task objects without directly accessing files."""

    def __init__(self, data_file="data/tasks.json"):
        self.persistence = DataPersistence(data_file)
        self.tasks = self.persistence.load_tasks()
        self.next_id = self._get_next_task_id()

    def _get_next_task_id(self):
        """Return the next unused task ID."""
        return max((task.id for task in self.tasks), default=0) + 1

    def _save_changes(self):
        """Save the current task collection."""
        self.persistence.save_tasks(self.tasks)

    def add_normal_task(self, description, tags=None):
        """Create and save a normal task."""
        task = Task(self.next_id, description, tags=tags)
        self.tasks.append(task)
        self.next_id += 1
        self._save_changes()
        return task

    def add_due_date_task(self, description, due_date_str, tags=None):
        """Create and save a task with a due date."""
        task = DueDateTask(
            self.next_id, description, due_date_str, tags=tags
        )
        self.tasks.append(task)
        self.next_id += 1
        self._save_changes()
        return task

    def add_priority_task(self, description, priority, tags=None):
        """Create and save a task with a priority."""
        task = PriorityTask(
            self.next_id, description, priority, tags=tags
        )
        self.tasks.append(task)
        self.next_id += 1
        self._save_changes()
        return task

    def get_task_by_id(self, task_id):
        """Find a task by its ID."""
        return next(
            (task for task in self.tasks if task.id == task_id),
            None,
        )

    def complete_task(self, task_id):
        """Mark a task as completed."""
        task = self.get_task_by_id(task_id)

        if task is None:
            return False, "Task not found."

        if task.completed:
            return False, "Task is already completed."

        task.mark_complete()
        self._save_changes()
        return True, "Task marked as completed."

    def delete_task(self, task_id):
        """Delete a task by its ID."""
        task = self.get_task_by_id(task_id)

        if task is None:
            return False, "Task not found."

        self.tasks.remove(task)
        self._save_changes()
        return True, "Task deleted successfully."

    def get_all_tasks(self):
        """Return all tasks without exposing the internal list."""
        return list(self.tasks)

    # --------------------------------------------------
    # Search
    # --------------------------------------------------

    def search_tasks(self, keyword):
        """Search descriptions and tags, ignoring letter case."""
        keyword = keyword.strip().casefold()

        if not keyword:
            return []

        results = []

        for task in self.tasks:
            description = task.description.casefold()
            task_tags = [
                str(tag).casefold()
                for tag in task.tags
            ]

            if (
                keyword in description
                or any(keyword in tag for tag in task_tags)
            ):
                results.append(task)

        return results

    # --------------------------------------------------
    # Filter
    # --------------------------------------------------

    @staticmethod
    def _parse_filter_date(date_text):
        """Validate and normalize a date to YYYY-MM-DD."""
        if not date_text:
            return None

        try:
            parsed = datetime.date.fromisoformat(date_text.strip())
        except (ValueError, TypeError):
            raise ValueError(
                "Invalid date. Please use YYYY-MM-DD."
            ) from None

        return parsed.isoformat()

    @staticmethod
    def _normalize_task_date(value):
        """Convert a task date to YYYY-MM-DD, if available."""
        if value is None:
            return None

        if isinstance(value, datetime.datetime):
            return value.date().isoformat()

        if isinstance(value, datetime.date):
            return value.isoformat()

        try:
            return datetime.date.fromisoformat(
                str(value).strip()[:10]
            ).isoformat()
        except (ValueError, TypeError):
            return None

    def filter_tasks(
        self,
        status=None,
        due_date_before=None,
        priority=None,
        tags=None,
        due_date_after=None,
    ):
        """
        Filter by status, due date, priority, and tags.

        All provided conditions are combined using AND.
        Due-date comparisons include the boundary date.
        """
        results = list(self.tasks)

        # Validate dates even if there are no tasks.
        before = self._parse_filter_date(due_date_before)
        after = self._parse_filter_date(due_date_after)

        if before and after and after > before:
            raise ValueError(
                "The 'due date after' cannot be later than "
                "the 'due date before'."
            )

        # Filter by completion status.
        if status:
            status_value = status.strip().casefold()

            if status_value in {
                "completed", "complete", "done", "เสร็จแล้ว"
            }:
                results = [
                    task for task in results if task.completed
                ]
            elif status_value in {
                "pending", "incomplete", "not completed", "ยังไม่เสร็จ"
            }:
                results = [
                    task for task in results if not task.completed
                ]
            else:
                raise ValueError(
                    "Status must be Pending or Completed."
                )

        # Filter by due date.
        if before:
            results = [
                task for task in results
                if (
                    self._normalize_task_date(
                        getattr(task, "due_date", None)
                    ) is not None
                    and self._normalize_task_date(
                        getattr(task, "due_date", None)
                    ) <= before
                )
            ]

        if after:
            results = [
                task for task in results
                if (
                    self._normalize_task_date(
                        getattr(task, "due_date", None)
                    ) is not None
                    and self._normalize_task_date(
                        getattr(task, "due_date", None)
                    ) >= after
                )
            ]

        # Filter by priority.
        if priority:
            wanted_priority = priority.strip().casefold()

            if wanted_priority not in {"high", "medium", "low"}:
                raise ValueError(
                    "Priority must be High, Medium, or Low."
                )

            results = [
                task for task in results
                if str(
                    getattr(task, "priority", "")
                ).casefold() == wanted_priority
            ]

        # Filter by tags.
        # Every requested tag must exist on the task.
        if tags:
            if isinstance(tags, str):
                requested_tags = [
                    tag.strip().casefold()
                    for tag in tags.split(",")
                    if tag.strip()
                ]
            else:
                requested_tags = [
                    str(tag).strip().casefold()
                    for tag in tags
                    if str(tag).strip()
                ]

            for wanted_tag in requested_tags:
                results = [
                    task for task in results
                    if any(
                        wanted_tag == str(task_tag).casefold()
                        for task_tag in task.tags
                    )
                ]

        return results

    # --------------------------------------------------
    # Sort
    # --------------------------------------------------

    def sort_tasks(self, criterion="id", reverse=False):
        """
        Sort by ID, due date, priority, description, or status.

        Tasks missing the selected value stay at the end,
        including when reverse=True.
        """
        criterion = criterion.strip().casefold()

        allowed_criteria = {
            "id",
            "description",
            "status",
            "completed",
            "due_date",
            "priority",
        }

        if criterion not in allowed_criteria:
            raise ValueError(
                "Invalid sort criterion. Choose id, description, "
                "status, completed, due_date, or priority."
            )

        priority_order = {
            "low": 1,
            "medium": 2,
            "high": 3,
        }

        def get_sort_value(task):
            if criterion == "id":
                return task.id

            if criterion == "description":
                return task.description.casefold()

            if criterion in {"status", "completed"}:
                return bool(task.completed)

            if criterion == "due_date":
                return self._normalize_task_date(
                    getattr(task, "due_date", None)
                )

            if criterion == "priority":
                value = getattr(task, "priority", None)

                if value is None:
                    return None

                return priority_order.get(
                    str(value).casefold()
                )

            return None

        tasks_with_value = []
        tasks_without_value = []

        for task in self.tasks:
            value = get_sort_value(task)

            if value is None:
                tasks_without_value.append(task)
            else:
                tasks_with_value.append((value, task))

        tasks_with_value.sort(
            key=lambda item: item[0],
            reverse=reverse,
        )

        return (
            [task for _, task in tasks_with_value]
            + tasks_without_value
        )
