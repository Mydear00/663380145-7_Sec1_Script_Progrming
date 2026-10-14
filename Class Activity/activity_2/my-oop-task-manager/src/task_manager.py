
"""
Module: task_manager.py
Description: Manages Task objects and JSON persistence.
"""

import json
from pathlib import Path

from .task import Task


class TaskManager:
    """จัดการรายการงานและการบันทึกข้อมูล."""

    def __init__(self, data_file="data/tasks.json"):
        """สร้าง TaskManager และโหลดงานเดิม."""
        project_root = Path(__file__).resolve().parent.parent

        self.data_file = Path(data_file)

        if not self.data_file.is_absolute():
            self.data_file = project_root / self.data_file

        self.tasks = self._load_tasks()
        self.next_id = self._get_next_task_id()

    def _get_next_task_id(self) -> int:
        """หา ID จำนวนเต็มบวกที่น้อยที่สุดซึ่งยังไม่ได้ใช้งาน."""
        existing_ids = {task.id for task in self.tasks}

        next_id = 1

        while next_id in existing_ids:
            next_id += 1

        return next_id

    def _load_tasks(self) -> list[Task]:
        """โหลดข้อมูล JSON แล้วแปลงเป็น Task objects."""
        if not self.data_file.exists():
            return []

        try:
            with self.data_file.open("r", encoding="utf-8") as file:
                raw_tasks = json.load(file)

            if not isinstance(raw_tasks, list):
                raise ValueError("Task data must be a list.")

            tasks = []

            for item in raw_tasks:
                if not isinstance(item, dict):
                    raise ValueError("Invalid task record.")

                task_id = item.get("id")
                description = item.get("description")
                completed = item.get("completed", False)
                priority = item.get("priority", "Medium")

                if (
                    not isinstance(task_id, int)
                    or isinstance(task_id, bool)
                    or task_id <= 0
                ):
                    raise ValueError("Invalid task ID.")

                if (
                    not isinstance(description, str)
                    or not description.strip()
                ):
                    raise ValueError("Invalid description.")

                if not isinstance(completed, bool):
                    raise ValueError("Invalid completion status.")

                if priority not in ("Low", "Medium", "High"):
                    priority = "Medium"

                tasks.append(
                    Task(
                        task_id,
                        description,
                        completed,
                        priority
                    )
                )

            ids = [task.id for task in tasks]

            if len(ids) != len(set(ids)):
                raise ValueError("Duplicate task IDs.")

            print(f"Loaded {len(tasks)} task(s).")
            return tasks

        except (
            json.JSONDecodeError,
            ValueError,
            TypeError
        ) as error:
            print(f"Warning: Could not load tasks: {error}")
            print("Starting with an empty task list.")
            return []

        except OSError as error:
            print(f"Warning: Could not read tasks file: {error}")
            return []

    def _save_tasks(self) -> bool:
        """บันทึก Task objects ลงไฟล์ JSON."""
        try:
            self.data_file.parent.mkdir(
                parents=True,
                exist_ok=True
            )

            tasks_as_dicts = [
                task.to_dict() for task in self.tasks
            ]

            with self.data_file.open(
                "w",
                encoding="utf-8"
            ) as file:
                json.dump(
                    tasks_as_dicts,
                    file,
                    indent=4,
                    ensure_ascii=False
                )

            return True

        except OSError as error:
            print(f"Error saving tasks: {error}")
            return False

    def add_task(
        self,
        description: str,
        priority: str = "Medium"
    ) -> None:
        """สร้างงานใหม่โดยใช้ ID ที่ว่างอยู่ แล้วบันทึกข้อมูล."""
        description = description.strip()

        if not description:
            print("Error: Task description cannot be empty.")
            return

        if priority not in ("Low", "Medium", "High"):
            print("Error: Invalid priority.")
            print("Please use Low, Medium, or High.")
            return

        # คำนวณ ID ใหม่ทุกครั้ง เพื่อใช้ ID ที่ว่างหลังลบงาน
        self.next_id = self._get_next_task_id()

        new_task = Task(
            self.next_id,
            description,
            priority=priority
        )

        self.tasks.append(new_task)

        if self._save_tasks():
            print(
                f"Task '{description}' added "
                f"with ID {new_task.id}."
            )
            self.next_id = self._get_next_task_id()
        else:
            self.tasks.remove(new_task)
            self.next_id = self._get_next_task_id()
            print("Task was not added because saving failed.")

    def list_tasks(self) -> None:
        """แสดงรายการงานในรูปแบบข้อความที่อ่านง่าย."""
        print("\n--- Your Task ---")

        if not self.tasks:
            print("No tasks found.")
            print("-------------------")
            return

        for task in self.tasks:
            status = "Completed" if task.completed else "Pending"

            print(
                f"ID: {task.id}   | "
                f"Description: {task.description}   | "
                f"Status: {status}"
            )

        print("-------------------")

    def complete_task(self, task_id: int) -> None:
        """ทำเครื่องหมายว่างานเสร็จแล้ว."""
        task = next(
            (item for item in self.tasks if item.id == task_id),
            None
        )

        if task is None:
            print(f"Error: Task #{task_id} not found.")
            return

        if task.completed:
            print(f"Task #{task_id} is already completed.")
            return

        task.mark_complete()

        if self._save_tasks():
            print(f"Task #{task_id} marked as completed.")
        else:
            task.completed = False
            print("Could not save the completion status.")

    def delete_task(self, task_id: int) -> None:
        """ลบงานตามรหัสที่กำหนด."""
        task = next(
            (item for item in self.tasks if item.id == task_id),
            None
        )

        if task is None:
            print(f"Error: Task #{task_id} not found.")
            return

        original_index = self.tasks.index(task)
        self.tasks.remove(task)

        if self._save_tasks():
            self.next_id = self._get_next_task_id()
            print(f"Task #{task_id} deleted successfully.")
        else:
            self.tasks.insert(original_index, task)
            self.next_id = self._get_next_task_id()
            print("Could not save deletion. Task was restored.")
