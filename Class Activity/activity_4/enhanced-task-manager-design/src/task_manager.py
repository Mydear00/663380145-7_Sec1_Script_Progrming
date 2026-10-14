"""Business logic for managing tasks."""

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
        task = Task(self.next_id, description, tags=tags)
        self.tasks.append(task)
        self.next_id += 1
        self._save_changes()
        return task

    def add_due_date_task(self, description, due_date_str, tags=None):
        task = DueDateTask(
            self.next_id, description, due_date_str, tags=tags
        )
        self.tasks.append(task)
        self.next_id += 1
        self._save_changes()
        return task

    def add_priority_task(self, description, priority, tags=None):
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
            None
        )

    def complete_task(self, task_id):
        task = self.get_task_by_id(task_id)

        if task is None:
            return False, "Task not found."

        if task.completed:
            return False, "Task is already completed."

        task.mark_complete()
        self._save_changes()
        return True, "Task marked as completed."

    def delete_task(self, task_id):
        task = self.get_task_by_id(task_id)

        if task is None:
            return False, "Task not found."

        self.tasks.remove(task)
        self._save_changes()
        return True, "Task deleted successfully."

    def get_all_tasks(self):
        """Return all tasks."""
        return list(self.tasks)

    # Planned features: placeholders for future implementation.

    def search_tasks(self, keyword):
        """Placeholder: search descriptions and tags."""
        print(
            f"DEBUG: Search functionality for {keyword!r} "
            "is not implemented yet."
        )
        return []

    def filter_tasks(
        self,
        status=None,
        due_date_before=None,
        priority=None,
        tags=None
    ):
        """Placeholder: filter by status, due date, priority, or tags."""
        print("DEBUG: Filter functionality is not implemented yet.")
        return []

    def sort_tasks(self, criterion="id", reverse=False):
        """Placeholder: sort by ID, due date, priority, or creation date."""
        print(
            f"DEBUG: Sort functionality for {criterion!r} "
            "is not implemented yet."
        )
        return list(self.tasks)