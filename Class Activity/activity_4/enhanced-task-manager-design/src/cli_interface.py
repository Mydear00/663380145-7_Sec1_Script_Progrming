
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
        print("7. Search Tasks")
        print("8. Filter Tasks")
        print("9. Sort Tasks")
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
                datetime.date.fromisoformat(date_text)
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

        # Remove duplicate tags while preserving order.
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

    def _display_tasks(self, tasks, heading="Tasks"):
        """Display a list of tasks or a no-results message."""
        if not tasks:
            print("No tasks found.")
            return

        print(f"\n--- {heading} ---")

        for task in tasks:
            print(task)

        print("-" * (len(heading) + 8))

    def _search_tasks(self):
        keyword = input("Enter search keyword: ").strip()

        if not keyword:
            print("Search keyword cannot be empty.")
            return

        tasks = self.manager.search_tasks(keyword)
        self._display_tasks(tasks, "Search Results")

    def _filter_tasks(self):
        print("\n--- Filter Tasks ---")
        print("Leave a field blank to skip that filter.")

        status = input(
            "Status (Pending/Completed): "
        ).strip() or None

        due_date_before = input(
            "Due date on or before (YYYY-MM-DD): "
        ).strip() or None

        due_date_after = input(
            "Due date on or after (YYYY-MM-DD): "
        ).strip() or None

        priority = input(
            "Priority (High/Medium/Low): "
        ).strip() or None

        tags = input(
            "Tags (comma-separated; task must have all tags): "
        ).strip() or None

        try:
            tasks = self.manager.filter_tasks(
                status=status,
                due_date_before=due_date_before,
                due_date_after=due_date_after,
                priority=priority,
                tags=tags,
            )

            self._display_tasks(tasks, "Filter Results")

        except ValueError as error:
            print(f"Filter error: {error}")

    def _sort_tasks(self):
        criterion = input(
            "Sort by (id, description, status, due_date, priority; "
            "default id): "
        ).strip().lower() or "id"

        direction = input(
            "Descending order? (yes/no; default no): "
        ).strip().lower()

        reverse = direction in {"yes", "y"}

        try:
            tasks = self.manager.sort_tasks(
                criterion=criterion,
                reverse=reverse,
            )

            self._display_tasks(tasks, "Sorted Tasks")

        except ValueError as error:
            print(f"Sort error: {error}")

    def run(self):
        """Run the main command-line menu."""
        while True:
            self.display_menu()
            choice = self.get_user_choice()

            if choice == "1":
                description = self.get_task_description()
                tags = self.get_tags_input()

                try:
                    task = self.manager.add_normal_task(
                        description, tags=tags
                    )
                    print(f"Normal task added with ID {task.id}.")
                except (ValueError, TypeError) as error:
                    print(f"Could not add task: {error}")

            elif choice == "2":
                description = self.get_task_description()
                due_date = self.get_due_date_input()
                tags = self.get_tags_input()

                try:
                    task = self.manager.add_due_date_task(
                        description, due_date, tags=tags
                    )
                    print(f"Due-date task added with ID {task.id}.")
                except (ValueError, TypeError) as error:
                    print(f"Could not add task: {error}")

            elif choice == "3":
                description = self.get_task_description()
                priority = self.get_priority_input()
                tags = self.get_tags_input()

                try:
                    task = self.manager.add_priority_task(
                        description, priority, tags=tags
                    )
                    print(f"Priority task added with ID {task.id}.")
                except (ValueError, TypeError) as error:
                    print(f"Could not add task: {error}")

            elif choice == "4":
                tasks = self.manager.get_all_tasks()
                self._display_tasks(tasks, "Your Tasks")

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
                self._search_tasks()

            elif choice == "8":
                self._filter_tasks()

            elif choice == "9":
                self._sort_tasks()

            elif choice == "0":
                print("Exiting Task Manager. Goodbye!")
                break

            else:
                print(
                    "Invalid choice. Please enter a number between 0 and 9."
                )
