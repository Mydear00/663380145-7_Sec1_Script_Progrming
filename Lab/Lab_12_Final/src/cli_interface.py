"""Command-line interface for the Enhanced Task Manager."""

from datetime import date

from .task import DueDateTask, PriorityTask


class CLIInterface:
    """Display menus and handle user input."""

    def __init__(self, task_manager):
        self.manager = task_manager

    def display_menu(self):
        """Display the main menu."""
        print("\n" + "=" * 48)
        print("       ENHANCED TASK MANAGER")
        print("=" * 48)
        print("1. Add Normal Task")
        print("2. Add Due Date Task")
        print("3. Add Priority Task")
        print("4. List All Tasks")
        print("5. Complete Task")
        print("6. Delete Task")
        print("7. Search Tasks")
        print("8. Filter Tasks")
        print("9. Sort Tasks")
        print("10. Add Tag to Task")
        print("11. Remove Tag from Task")
        print("0. Exit")
        print("=" * 48)

    @staticmethod
    def get_task_description():
        """Ask for a non-empty task description."""
        while True:
            description = input("Enter task description: ").strip()

            if description:
                return description

            print("Description cannot be empty.")

    @staticmethod
    def get_tags_input():
        """Ask for optional comma-separated tags."""
        raw_tags = input(
            "Enter tags separated by commas (optional): "
        ).strip()

        # Remove duplicate tags without considering letter case.
        tags = []
        seen = set()

        for raw_tag in raw_tags.split(","):
            tag = raw_tag.strip()

            if tag and tag.casefold() not in seen:
                tags.append(tag)
                seen.add(tag.casefold())

        return tags

    @staticmethod
    def get_task_id(prompt="Enter task ID: "):
        """Read a positive integer task ID."""
        raw_id = input(prompt).strip()

        try:
            task_id = int(raw_id)

            if task_id <= 0:
                raise ValueError

            return task_id

        except ValueError:
            print("Please enter a positive numeric task ID.")
            return None

    @staticmethod
    def get_date_input(prompt="Enter date (YYYY-MM-DD): "):
        """Read and validate a date."""
        while True:
            raw_date = input(prompt).strip()

            try:
                return date.fromisoformat(raw_date)

            except ValueError:
                print("Invalid date. Example: 2026-12-31")

    @staticmethod
    def get_priority_input():
        """Read a valid priority."""
        while True:
            priority = input(
                "Enter priority (High/Medium/Low): "
            ).strip().capitalize()

            if priority in {"High", "Medium", "Low"}:
                return priority

            print("Please enter High, Medium, or Low.")

    @staticmethod
    def display_tasks(tasks, title="Tasks"):
        """Display a list of tasks."""
        print(f"\n--- {title} ---")

        if not tasks:
            print("No tasks found.")
        else:
            for task in tasks:
                print(task)

        print("-" * 48)

    def add_normal_task(self):
        """Create a normal task."""
        description = self.get_task_description()
        tags = self.get_tags_input()

        task = self.manager.add_normal_task(description, tags)
        print(f"Normal task added successfully. ID: {task.id}")

    def add_due_date_task(self):
        """Create a task with a due date."""
        description = self.get_task_description()
        due_date = self.get_date_input(
            "Enter due date (YYYY-MM-DD): "
        )
        tags = self.get_tags_input()

        task = self.manager.add_due_date_task(
            description,
            due_date,
            tags,
        )

        print(f"Due-date task added successfully. ID: {task.id}")

    def add_priority_task(self):
        """Create a task with a priority."""
        description = self.get_task_description()
        priority = self.get_priority_input()
        tags = self.get_tags_input()

        task = self.manager.add_priority_task(
            description,
            priority,
            tags,
        )

        print(f"Priority task added successfully. ID: {task.id}")

    def list_all_tasks(self):
        """Display all tasks."""
        self.display_tasks(
            self.manager.get_all_tasks(),
            "All Tasks",
        )

    def complete_task(self):
        """Mark a task as completed."""
        task_id = self.get_task_id(
            "Enter ID of task to complete: "
        )

        if task_id is None:
            return

        success, message = self.manager.complete_task(task_id)
        print(message)

    def delete_task(self):
        """Delete a task."""
        task_id = self.get_task_id(
            "Enter ID of task to delete: "
        )

        if task_id is None:
            return

        confirm = input(
            "Are you sure you want to delete this task? (y/n): "
        ).strip().casefold()

        if confirm not in {"y", "yes"}:
            print("Deletion cancelled.")
            return

        success, message = self.manager.delete_task(task_id)
        print(message)

    def search_tasks(self):
        """Search by description or tag."""
        keyword = input("Enter keyword to search: ").strip()

        results = self.manager.search_tasks(keyword)

        self.display_tasks(
            results,
            f"Search Results: {keyword}",
        )

    def filter_tasks(self):
        """Filter tasks using multiple criteria."""
        print("\n--- Filter Tasks ---")
        print("Leave a field blank to skip that filter.")

        status_input = input(
            "Status (completed/pending): "
        ).strip().casefold()

        status = None

        if status_input in {"completed", "done", "true"}:
            status = True
        elif status_input in {"pending", "incomplete", "false"}:
            status = False
        elif status_input:
            print("Unknown status. Status filter will be skipped.")

        before_input = input(
            "Due on or before (YYYY-MM-DD): "
        ).strip()

        after_input = input(
            "Due on or after (YYYY-MM-DD): "
        ).strip()

        before = self._parse_optional_date(before_input)
        after = self._parse_optional_date(after_input)

        priority_input = input(
            "Priority (High/Medium/Low): "
        ).strip()

        priority = None

        if priority_input:
            normalized = priority_input.capitalize()

            if normalized in {"High", "Medium", "Low"}:
                priority = normalized
            else:
                print("Unknown priority. Priority filter will be skipped.")

        tags_input = input(
            "Required tags separated by commas: "
        ).strip()

        tags = [
            tag.strip()
            for tag in tags_input.split(",")
            if tag.strip()
        ]

        try:
            results = self.manager.filter_tasks(
                status=status,
                due_date_before=before,
                due_date_after=after,
                priority_level=priority,
                contains_tags=tags or None,
            )

            self.display_tasks(results, "Filtered Tasks")

        except (ValueError, TypeError) as error:
            print(f"Could not filter tasks: {error}")

    @staticmethod
    def _parse_optional_date(raw_date):
        """Parse an optional date without interrupting the menu."""
        if not raw_date:
            return None

        try:
            return date.fromisoformat(raw_date)

        except ValueError:
            print("Invalid date. This date filter will be skipped.")
            return None

    def sort_tasks(self):
        """Sort tasks by a selected criterion."""
        print("\nAvailable sorting criteria:")
        print("1. ID")
        print("2. Description")
        print("3. Completed status")
        print("4. Due date")
        print("5. Priority")

        choices = {
            "1": "id",
            "2": "description",
            "3": "completed",
            "4": "due_date",
            "5": "priority",
        }

        choice = input("Select sorting criterion: ").strip()

        if choice not in choices:
            print("Invalid sorting choice.")
            return

        direction = input(
            "Descending order? (y/n): "
        ).strip().casefold()

        reverse = direction in {"y", "yes"}

        try:
            results = self.manager.sort_tasks(
                choices[choice],
                reverse=reverse,
            )

            self.display_tasks(
                results,
                f"Sorted by {choices[choice]}",
            )

        except ValueError as error:
            print(error)

    def add_tag(self):
        """Add a tag to an existing task."""
        task_id = self.get_task_id()

        if task_id is None:
            return

        tag = input("Enter tag to add: ").strip()

        success, message = self.manager.add_tag(task_id, tag)
        print(message)

    def remove_tag(self):
        """Remove a tag from an existing task."""
        task_id = self.get_task_id()

        if task_id is None:
            return

        tag = input("Enter tag to remove: ").strip()

        success, message = self.manager.remove_tag(task_id, tag)
        print(message)

    def run(self):
        """Run the main application loop."""
        actions = {
            "1": self.add_normal_task,
            "2": self.add_due_date_task,
            "3": self.add_priority_task,
            "4": self.list_all_tasks,
            "5": self.complete_task,
            "6": self.delete_task,
            "7": self.search_tasks,
            "8": self.filter_tasks,
            "9": self.sort_tasks,
            "10": self.add_tag,
            "11": self.remove_tag,
        }

        while True:
            self.display_menu()
            choice = input("Enter your choice: ").strip()

            if choice == "0":
                print("Thank you for using Enhanced Task Manager!")
                break

            action = actions.get(choice)

            if action is None:
                print("Invalid choice. Please select 0-11.")
                continue

            try:
                action()

            except (OSError, ValueError, TypeError) as error:
                print(f"Operation failed: {error}")

            except EOFError:
                print("\nInput ended. Exiting Task Manager.")
                break