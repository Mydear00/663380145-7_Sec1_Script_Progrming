"""Command-line user interface."""

import datetime


class CLIInterface:
    """Handle user interaction and delegate operations to TaskManager."""

    def __init__(self, task_manager):
        self.manager = task_manager

    def display_menu(self):
        print("\n--- Enhanced Task Manager Menu ---")
        print("1. Add Normal Task")
        print("2. Add Due Date Task")
        print("3. Add Priority Task")
        print("4. List All Tasks")
        print("5. Complete Task")
        print("6. Delete Task")
        print("7. Search Tasks (Placeholder)")
        print("8. Filter Tasks (Placeholder)")
        print("9. Sort Tasks (Placeholder)")
        print("0. Exit")
        print("----------------------------------")

    def get_user_choice(self):
        return input("Enter your choice (0-9): ").strip()

    def get_task_description(self):
        while True:
            description = input("Enter task description: ").strip()

            if description:
                return description

            print("Task description cannot be empty. Please try again.")

    def get_due_date_input(self):
        while True:
            date_text = input(
                "Enter due date (YYYY-MM-DD): "
            ).strip()

            try:
                datetime.datetime.strptime(date_text, "%Y-%m-%d")
                return date_text
            except ValueError:
                print(
                    "Invalid date. Please use YYYY-MM-DD, "
                    "e.g. 2026-12-31."
                )

    def get_priority_input(self):
        while True:
            priority = input(
                "Enter priority (High/Medium/Low): "
            ).strip().capitalize()

            if priority in {"High", "Medium", "Low"}:
                return priority

            print("Invalid priority. Please enter High, Medium, or Low.")

    def get_tags_input(self):
        raw_tags = input(
            "Enter tags separated by commas "
            "(optional, e.g. work,urgent): "
        ).strip()

        tags = [
            tag.strip()
            for tag in raw_tags.split(",")
            if tag.strip()
        ]

        # Remove duplicate tags while preserving their order.
        return list(dict.fromkeys(tags))

    def _get_task_id(self, prompt):
        try:
            task_id = int(input(prompt).strip())

            if task_id <= 0:
                raise ValueError

            return task_id

        except ValueError:
            print("Invalid input. Please enter a positive Task ID.")
            return None

    def run(self):
        while True:
            self.display_menu()
            choice = self.get_user_choice()

            if choice == "1":
                description = self.get_task_description()
                tags = self.get_tags_input()

                task = self.manager.add_normal_task(
                    description, tags=tags
                )
                print(f"Normal task added with ID {task.id}.")

            elif choice == "2":
                description = self.get_task_description()
                due_date = self.get_due_date_input()
                tags = self.get_tags_input()

                task = self.manager.add_due_date_task(
                    description, due_date, tags=tags
                )
                print(f"Due-date task added with ID {task.id}.")

            elif choice == "3":
                description = self.get_task_description()
                priority = self.get_priority_input()
                tags = self.get_tags_input()

                task = self.manager.add_priority_task(
                    description, priority, tags=tags
                )
                print(f"Priority task added with ID {task.id}.")

            elif choice == "4":
                tasks = self.manager.get_all_tasks()

                if not tasks:
                    print("No tasks found.")
                else:
                    print("\n--- Your Tasks ---")

                    for task in tasks:
                        print(task)

                    print("------------------")

            elif choice == "5":
                task_id = self._get_task_id(
                    "Enter ID of task to complete: "
                )

                if task_id is not None:
                    _, message = self.manager.complete_task(task_id)
                    print(message)

            elif choice == "6":
                task_id = self._get_task_id(
                    "Enter ID of task to delete: "
                )

                if task_id is not None:
                    _, message = self.manager.delete_task(task_id)
                    print(message)

            elif choice == "7":
                keyword = input("Enter search keyword: ").strip()
                found_tasks = self.manager.search_tasks(keyword)

                if found_tasks:
                    print("\n--- Search Results ---")

                    for task in found_tasks:
                        print(task)
                else:
                    print(f"No tasks found matching {keyword!r}.")

            elif choice == "8":
                self.manager.filter_tasks()
                print(
                    "Filtering is a placeholder in this scaffold. "
                    "See PLAN.md for details."
                )

            elif choice == "9":
                criterion = input(
                    "Sort by (id, due_date, priority; default id): "
                ).strip().lower() or "id"

                reverse = (
                    input("Reverse order (yes/no; default no): ")
                    .strip()
                    .lower() == "yes"
                )

                tasks = self.manager.sort_tasks(criterion, reverse)

                if tasks:
                    print("\n--- Sorted Tasks ---")

                    for task in tasks:
                        print(task)
                else:
                    print("No tasks found.")

            elif choice == "0":
                print("Exiting Task Manager. Goodbye!")
                break

            else:
                print(
                    "Invalid choice. Please enter a number between 0 and 9."
                )