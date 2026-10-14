"""
Module: main.py
Description: Entry point for the OOP Task Manager CLI.
"""

import sys

from src.task_manager import TaskManager


def display_menu() -> None:
    """แสดงเมนูหลัก."""
    print("\n" + "=" * 40)
    print("       OOP TASK MANAGER CLI")
    print("=" * 40)
    print("  1. Add Task")
    print("  2. List Tasks")
    print("  3. Complete Task")
    print("  4. Delete Task")
    print("  5. Save and Exit")
    print("=" * 40)


def get_task_id(prompt: str) -> int:
    """รับรหัสงานที่ต้องเป็นจำนวนเต็มบวก."""
    value = input(prompt).strip()

    if value.startswith("#"):
        value = value[1:].strip()

    task_id = int(value)

    if task_id <= 0:
        raise ValueError("Task ID must be positive.")

    return task_id


def main() -> None:
    """เริ่มการทำงานของโปรแกรม."""
    print("Welcome to OOP Task Manager CLI!")
    print("Loading tasks from storage...")

    manager = TaskManager()
    print(f"Ready: {len(manager.tasks)} task(s) loaded.")

    # ไม่แสดงรายการงานอัตโนมัติเมื่อเริ่มโปรแกรม
    try:
        while True:
            display_menu()
            choice = input("Enter choice (1-5): ").strip()

            if choice == "1":
                description = input(
                    "Enter task description: "
                ).strip()

                if not description:
                    print("[Error] Task description cannot be empty.")
                    continue

                priority = input(
                    "Enter priority (Low/Medium/High) "
                    "[Default: Medium]: "
                ).strip()

                if not priority:
                    priority = "Medium"
                else:
                    priority = priority.capitalize()

                manager.add_task(description, priority)

            elif choice == "2":
                # แสดงรายการงานเมื่อผู้ใช้เลือกเมนู 2 เท่านั้น
                manager.list_tasks()

            elif choice == "3":
                try:
                    task_id = get_task_id(
                        "Enter task ID to complete: "
                    )
                    manager.complete_task(task_id)

                except ValueError:
                    print(
                        "[Error] Enter a positive integer, "
                        "for example 1 or #2."
                    )

            elif choice == "4":
                try:
                    task_id = get_task_id(
                        "Enter task ID to delete: "
                    )

                    task = next(
                        (
                            item
                            for item in manager.tasks
                            if item.id == task_id
                        ),
                        None
                    )

                    if task is None:
                        print(
                            f"Error: Task #{task_id} not found."
                        )
                        continue

                    confirm = input(
                        f"Delete task #{task_id}? (y/N): "
                    ).strip().lower()

                    if confirm in ("y", "yes"):
                        manager.delete_task(task_id)
                    else:
                        print("Deletion cancelled.")

                except ValueError:
                    print(
                        "[Error] Enter a valid positive task ID."
                    )

            elif choice == "5":
                print("\nSaving tasks...")

                if manager._save_tasks():
                    print("All tasks saved successfully.")
                    print("Goodbye!")
                else:
                    print("Warning: Tasks could not be saved.")

                break

            else:
                print(
                    "[Error] Invalid choice. "
                    "Please select a number from 1 to 5."
                )

    except KeyboardInterrupt:
        print("\n\nProgram interrupted.")
        print("Saving tasks before exiting...")

        if manager._save_tasks():
            print("Tasks saved successfully.")
        else:
            print("Warning: Tasks could not be saved.")

        sys.exit(0)


if __name__ == "__main__":
    main()