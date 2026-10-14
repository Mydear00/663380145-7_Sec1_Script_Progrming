def list_tasks(self):
    """แสดงรายการงานทั้งหมดในรูปแบบที่อ่านง่าย."""

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