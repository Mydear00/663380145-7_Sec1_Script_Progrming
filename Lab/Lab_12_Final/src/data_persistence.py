"""Load and save tasks using JSON."""

import json
from pathlib import Path

from .task import Task, DueDateTask, PriorityTask


class DataPersistence:
    """Handle JSON persistence for task objects."""

    def __init__(self, file_path="data/tasks.json"):
        self.file_path = Path(file_path)

    def load_tasks(self):
        """Load tasks from JSON and restore their class types."""
        if not self.file_path.exists():
            self.save_tasks([])
            return []

        try:
            with self.file_path.open("r", encoding="utf-8") as file:
                data = json.load(file)
        except (json.JSONDecodeError, OSError) as error:
            raise ValueError(
                f"Cannot read task data from {self.file_path}: {error}"
            ) from error

        if not isinstance(data, list):
            raise ValueError("Task data must be a JSON list.")

        tasks = []

        for item in data:
            if not isinstance(item, dict):
                raise ValueError("Each task must be a JSON object.")

            task_type = item.get("type", "normal")

            if task_type == "due_date":
                task = DueDateTask.from_dict(item)
            elif task_type == "priority":
                task = PriorityTask.from_dict(item)
            elif task_type == "normal":
                task = Task.from_dict(item)
            else:
                raise ValueError(f"Unknown task type: {task_type}")

            tasks.append(task)

        return tasks

    def save_tasks(self, tasks):
        """Save tasks as JSON."""
        self.file_path.parent.mkdir(parents=True, exist_ok=True)

        data = [task.to_dict() for task in tasks]

        with self.file_path.open("w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=4)