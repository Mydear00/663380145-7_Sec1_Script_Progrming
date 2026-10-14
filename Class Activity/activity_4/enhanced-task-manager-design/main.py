"""Application entry point and orchestrator."""

from src.task_manager import TaskManager
from src.cli_interface import CLIInterface


def main():
    """Initialize the manager and start the CLI."""
    manager = TaskManager()
    cli = CLIInterface(manager)
    cli.run()


if __name__ == "__main__":
    main()