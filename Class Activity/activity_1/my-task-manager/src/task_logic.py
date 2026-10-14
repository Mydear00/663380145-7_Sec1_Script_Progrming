
"""
Module: task_logic.py
Description: Core task management logic.
"""

from typing import Any

VALID_PRIORITIES = ("Low", "Medium", "High")


def get_next_task_id(tasks: list[dict[str, Any]]) -> int:
    """สร้าง ID ใหม่ที่ไม่ซ้ำกับ ID ของงานเดิม."""
    if not tasks:
        return 1

    return max(task["id"] for task in tasks) + 1


def add_task(
    tasks: list[dict[str, Any]],
    description: str,
    priority: str = "Medium"
) -> list[dict[str, Any]]:
    """เพิ่มงานใหม่พร้อม ID และระดับความสำคัญ."""
    cleaned_description = description.strip()

    if not cleaned_description:
        print("[Error] Task description cannot be empty.")
        return tasks

    cleaned_priority = priority.strip().capitalize()

    if cleaned_priority not in VALID_PRIORITIES:
        print("[Warning] Invalid priority. Using Medium instead.")
        cleaned_priority = "Medium"

    new_task = {
        "id": get_next_task_id(tasks),
        "description": cleaned_description,
        "completed": False,
        "priority": cleaned_priority
    }

    tasks.append(new_task)

    print(
        f"[OK] Task '{cleaned_description}' added "
        f"with ID #{new_task['id']} "
        f"(Priority: {cleaned_priority})."
    )

    return tasks


def list_tasks(
    tasks: list[dict[str, Any]],
    filter_status: str | None = None
) -> None:
    """แสดงงานทั้งหมด หรือกรองตาม pending/completed."""
    if filter_status not in (None, "pending", "completed"):
        print("[Error] Invalid task status filter.")
        return

    filtered_tasks = tasks

    if filter_status == "pending":
        filtered_tasks = [
            task for task in tasks if not task["completed"]
        ]
    elif filter_status == "completed":
        filtered_tasks = [
            task for task in tasks if task["completed"]
        ]

    if not filtered_tasks:
        print("\n[Empty] No tasks found.")
        return

    print("\n" + "=" * 78)
    print(
        f"{'ID':<7} | {'Status':<12} | "
        f"{'Priority':<10} | Description"
    )
    print("-" * 78)

    for task in filtered_tasks:
        task_id = f"#{task['id']}"
        status = (
            "Completed" if task["completed"] else "Pending"
        )
        priority = task.get("priority", "Medium")
        description = task["description"]

        print(
            f"{task_id:<7} | {status:<12} | "
            f"{priority:<10} | {description}"
        )

    print("=" * 78)

    total = len(tasks)
    completed_count = sum(
        1 for task in tasks if task["completed"]
    )
    print(
        f"Summary: {completed_count}/{total} "
        "task(s) completed."
    )


def complete_task(
    tasks: list[dict[str, Any]],
    task_id: int
) -> list[dict[str, Any]]:
    """ทำเครื่องหมายงานที่ตรงกับ ID ว่าเสร็จแล้ว."""
    for task in tasks:
        if task["id"] == task_id:
            if task["completed"]:
                print(f"[Info] Task #{task_id} is already completed.")
            else:
                task["completed"] = True
                print(
                    f"[OK] Task #{task_id} marked as completed."
                )
            return tasks

    print(f"[Error] Task #{task_id} was not found.")
    return tasks


def delete_task(
    tasks: list[dict[str, Any]],
    task_id: int
) -> list[dict[str, Any]]:
    """ลบงานที่ตรงกับ ID."""
    for index, task in enumerate(tasks):
        if task["id"] == task_id:
            removed_task = tasks.pop(index)
            print(
                f"[OK] Task #{task_id} "
                f"('{removed_task['description']}') deleted."
            )
            return tasks

    print(f"[Error] Task #{task_id} was not found.")
    return tasks


def search_tasks(
    tasks: list[dict[str, Any]],
    keyword: str
) -> None:
    """ค้นหางานโดยไม่สนใจตัวพิมพ์เล็กหรือใหญ่."""
    cleaned_keyword = keyword.strip().casefold()

    if not cleaned_keyword:
        print("[Error] Search keyword cannot be empty.")
        return

    matches = [
        task for task in tasks
        if cleaned_keyword in task["description"].casefold()
    ]

    if not matches:
        print(f"[Search] No tasks found for '{keyword}'.")
        return

    print(f"\n[Search Results] Keyword: '{keyword}'")
    list_tasks(matches)
