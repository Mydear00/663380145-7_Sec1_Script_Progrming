"""JSON file persistence for task objects."""

import json
from pathlib import Path

from .task import Task, DueDateTask, PriorityTask


class DataPersistence:
    """Load and save tasks using a JSON file."""

    def __init__(self, data_file="data/tasks.json"):
        project_root = Path(__file__).resolve().parent.parent
        requested_path = Path(data_file)

        if requested_path.is_absolute():
            self.data_file_path = requested_path
        else:
            self.data_file_path = project_root / requested_path

    def load_tasks(self):
        """Load tasks and reconstruct the appropriate task class."""
        if not self.data_file_path.exists():
            self.data_file_path.parent.mkdir(
                parents=True, exist_ok=True
            )
            self.data_file_path.write_text("[]", encoding="utf-8")
            return []

        try:
            with self.data_file_path.open("r", encoding="utf-8") as file:
                raw_tasks = json.load(file)

            if not isinstance(raw_tasks, list):
                raise ValueError("The JSON root must be a list.")

            loaded_tasks = []

            for original_data in raw_tasks:
                if not isinstance(original_data, dict):
                    continue

                task_data = dict(original_data)
                task_type = task_data.pop("_type", "Task")
                task_data.setdefault("tags", [])

                try:
                    if task_type == "Task":
                        task = Task(**task_data)
                    elif task_type == "DueDateTask":
                        task = DueDateTask(**task_data)
                    elif task_type == "PriorityTask":
                        task = PriorityTask(**task_data)
                    else:
                        print(
                            f"Warning: Unknown task type {task_type!r}. "
                            "Skipping this task."
                        )
                        continue

                    loaded_tasks.append(task)

                except (TypeError, ValueError) as error:
                    print(f"Warning: Skipping invalid task: {error}")

            return loaded_tasks

        except (json.JSONDecodeError, ValueError) as error:
            print(
                f"Warning: Could not read tasks.json ({error}). "
                "Starting with an empty task list."
            )
            return []

        except OSError as error:
            print(f"Warning: Could not load tasks: {error}")
            return []

    def save_tasks(self, tasks):
        """Save task objects to a JSON file."""
        self.data_file_path.parent.mkdir(
            parents=True, exist_ok=True
        )

        task_data = [task.to_dict() for task in tasks]

        with self.data_file_path.open("w", encoding="utf-8") as file:
            json.dump(
                task_data,
                file,
                indent=4,
                ensure_ascii=False
            )