
"""
Module: main.py
Description: Entry point for the Task Manager CLI application.
"""

import sys

from src import task_data
from src import task_logic


def display_menu() -> None:
    """แสดงเมนูหลักของโปรแกรม."""
    print("\n" + "=" * 38)
    print("          TASK MANAGER CLI")
    print("=" * 38)
    print("  1. Add New Task")
    print("  2. List All Tasks")
    print("  3. List Pending Tasks")
    print("  4. List Completed Tasks")
    print("  5. Search Tasks by Keyword")
    print("  6. Mark Task as Completed")
    print("  7. Delete Task")
    print("  8. Save and Exit")
    print("=" * 38)


def prompt_task_id(prompt_text: str) -> int:
    """รับ ID ที่ต้องเป็นจำนวนเต็มบวก."""
    raw_value = input(prompt_text).strip()

    # รองรับทั้ง 2 และ #2
    if raw_value.startswith("#"):
        raw_value = raw_value[1:].strip()

    task_id = int(raw_value)

    if task_id <= 0:
        raise ValueError("Task ID must be a positive integer.")

    return task_id


def save_if_changed(
    tasks: list[dict],
    previous_tasks: list[dict]
) -> None:
    """บันทึกเมื่อรายการงานเปลี่ยนแปลง."""
    if tasks != previous_tasks:
        if task_data.save_tasks(tasks):
            print("[OK] Changes saved.")
        else:
            print("[Warning] Changes could not be saved.")


def main() -> None:
    """เริ่มการทำงานของ Task Manager CLI."""
    print("Welcome to Task Manager CLI!")
    print("Loading tasks from storage...")

    tasks = task_data.load_tasks()
    print(f"Loaded {len(tasks)} task(s).")

    try:
        while True:
            display_menu()
            choice = input("Enter choice (1-8): ").strip()

            if choice == "1":
                description = input(
                    "Enter task description: "
                ).strip()

                if not description:
                    print("[Error] Description cannot be empty.")
                    continue

                priority = input(
                    "Enter priority (Low/Medium/High) "
                    "[Default: Medium]: "
                ).strip()

                if not priority:
                    priority = "Medium"

                previous_tasks = [task.copy() for task in tasks]

                tasks = task_logic.add_task(
                    tasks, description, priority
                )
                save_if_changed(tasks, previous_tasks)

            elif choice == "2":
                task_logic.list_tasks(tasks)

            elif choice == "3":
                task_logic.list_tasks(
                    tasks, filter_status="pending"
                )

            elif choice == "4":
                task_logic.list_tasks(
                    tasks, filter_status="completed"
                )

            elif choice == "5":
                keyword = input(
                    "Enter search keyword: "
                ).strip()

                task_logic.search_tasks(tasks, keyword)

            elif choice == "6":
                try:
                    task_id = prompt_task_id(
                        "Enter task ID to complete: "
                    )

                    previous_tasks = [
                        task.copy() for task in tasks
                    ]

                    tasks = task_logic.complete_task(
                        tasks, task_id
                    )
                    save_if_changed(tasks, previous_tasks)

                except ValueError:
                    print(
                        "[Error] Enter a positive integer, "
                        "for example 1 or #2."
                    )

            elif choice == "7":
                try:
                    task_id = prompt_task_id(
                        "Enter task ID to delete: "
                    )

                    # ตรวจสอบว่ามี ID นี้จริงก่อนขอคำยืนยัน
                    task_exists = any(
                        task["id"] == task_id for task in tasks
                    )

                    if not task_exists:
                        print(
                            f"[Error] Task #{task_id} "
                            "was not found."
                        )
                        continue

                    confirm = input(
                        f"Delete Task #{task_id}? (y/N): "
                    ).strip().lower()

                    if confirm in ("y", "yes"):
                        previous_tasks = [
                            task.copy() for task in tasks
                        ]

                        tasks = task_logic.delete_task(
                            tasks, task_id
                        )
                        save_if_changed(tasks, previous_tasks)
                    else:
                        print("[Info] Deletion cancelled.")

                except ValueError:
                    print(
                        "[Error] Enter a valid positive task ID."
                    )

            elif choice == "8":
                print("\nSaving tasks...")

                if task_data.save_tasks(tasks):
                    print("[OK] All tasks saved successfully.")
                    print("Goodbye!")
                else:
                    print(
                        "[Error] Save failed. "
                        "Please check file permissions."
                    )

                break

            else:
                print(
                    "[Error] Invalid choice. "
                    "Please select a number from 1 to 8."
                )

    except KeyboardInterrupt:
        print("\n\n[Notice] Program interrupted by user.")
        print("Attempting to save tasks before exiting...")

        if task_data.save_tasks(tasks):
            print("[OK] Tasks saved.")
        else:
            print("[Error] Could not save tasks.")

        sys.exit(0)


if __name__ == "__main__":
    main()
