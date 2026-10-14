
"""
Module: task_data.py
Description: Handles loading and saving tasks in JSON format.
"""

import json
from pathlib import Path
from typing import Any

# หาโฟลเดอร์หลักของโปรเจกต์จากตำแหน่งไฟล์นี้
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
TASKS_FILE = DATA_DIR / "tasks.json"


def _is_valid_task(task: Any) -> bool:
    """ตรวจสอบว่า Task มีข้อมูลพื้นฐานครบและถูกชนิดหรือไม่."""
    if not isinstance(task, dict):
        return False

    task_id = task.get("id")
    description = task.get("description")
    completed = task.get("completed")
    priority = task.get("priority", "Medium")

    return (
        isinstance(task_id, int)
        and not isinstance(task_id, bool)
        and task_id > 0
        and isinstance(description, str)
        and isinstance(completed, bool)
        and isinstance(priority, str)
        and priority.capitalize() in ("Low", "Medium", "High")
    )


def load_tasks() -> list[dict[str, Any]]:
    """โหลดรายการงานจาก JSON หากไฟล์ไม่มีหรือข้อมูลผิดรูปแบบให้คืน []."""
    try:
        DATA_DIR.mkdir(parents=True, exist_ok=True)

        if not TASKS_FILE.exists():
            return []

        with TASKS_FILE.open("r", encoding="utf-8") as file:
            tasks = json.load(file)

        if not isinstance(tasks, list):
            print("[Warning] tasks.json must contain a list.")
            return []

        if not all(_is_valid_task(task) for task in tasks):
            print("[Warning] Invalid task data found in tasks.json.")
            return []

        # รองรับไฟล์เก่าที่ไม่มี priority
        for task in tasks:
            task.setdefault("priority", "Medium")

        # ป้องกัน ID ซ้ำ
        ids = [task["id"] for task in tasks]
        if len(ids) != len(set(ids)):
            print("[Warning] Duplicate task IDs found in tasks.json.")
            return []

        return tasks

    except json.JSONDecodeError as error:
        print(
            "[Warning] Invalid JSON in tasks.json "
            f"(line {error.lineno}, column {error.colno})."
        )
        return []

    except OSError as error:
        print(f"[Error] Could not read tasks.json: {error}")
        return []


def save_tasks(tasks: list[dict[str, Any]]) -> bool:
    """บันทึกรายการงานลง JSON คืน True เมื่อสำเร็จ."""
    try:
        DATA_DIR.mkdir(parents=True, exist_ok=True)

        with TASKS_FILE.open("w", encoding="utf-8") as file:
            json.dump(
                tasks,
                file,
                indent=4,
                ensure_ascii=False
            )

        return True

    except (OSError, TypeError, ValueError) as error:
        print(f"[Error] Could not save tasks: {error}")
        return False
