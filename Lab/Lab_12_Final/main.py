"""Entry point for the Enhanced Task Manager."""

from src.task_manager import TaskManager
from src.cli_interface import CLIInterface


def main():
    """Initialize and run the application."""
    try:
        manager = TaskManager()
        app = CLIInterface(manager)
        app.run()

    except (OSError, ValueError) as error:
        print(f"Unable to start Task Manager: {error}")


if __name__ == "__main__":
    main()