"""Task classes for the Enhanced Task Manager."""

import datetime


class Task:
    """Represent a normal task."""

    def __init__(self, task_id, description, completed=False, tags=None):
        if not isinstance(description, str) or not description.strip():
            raise ValueError("Task description cannot be empty.")

        self.id = int(task_id)
        self.description = description.strip()
        self.completed = bool(completed)
        self.tags = []

        for tag in tags or []:
            self.add_tag(tag)

    def add_tag(self, tag):
        """Add a tag without duplicates."""
        if not isinstance(tag, str) or not tag.strip():
            return False

        tag = tag.strip()

        if any(existing.casefold() == tag.casefold() for existing in self.tags):
            return False

        self.tags.append(tag)
        return True

    def remove_tag(self, tag):
        """Remove a tag without case sensitivity."""
        if not isinstance(tag, str):
            return False

        for existing in self.tags:
            if existing.casefold() == tag.strip().casefold():
                self.tags.remove(existing)
                return True

        return False

    def mark_complete(self):
        """Mark the task as completed."""
        self.completed = True

    def to_dict(self):
        """Convert the task to a JSON-compatible dictionary."""
        return {
            "id": self.id,
            "description": self.description,
            "completed": self.completed,
            "tags": list(self.tags),
            "type": "normal",
        }

    @classmethod
    def from_dict(cls, data):
        """Create a task from a dictionary."""
        return cls(
            task_id=data["id"],
            description=data["description"],
            completed=data.get("completed", False),
            tags=data.get("tags", []),
        )

    def __str__(self):
        """Return a readable task description."""
        status = "Completed" if self.completed else "Pending"
        tags_text = ", ".join(self.tags) if self.tags else "None"

        return (
            f"ID: {self.id} | "
            f"Description: {self.description} | "
            f"Status: {status} | "
            f"Tags: {tags_text}"
        )


class DueDateTask(Task):
    """Represent a task with a due date."""

    def __init__(
        self,
        task_id,
        description,
        due_date,
        completed=False,
        tags=None,
    ):
        super().__init__(task_id, description, completed, tags)

        if isinstance(due_date, datetime.datetime):
            due_date = due_date.date()

        if isinstance(due_date, str):
            try:
                due_date = datetime.date.fromisoformat(due_date)
            except ValueError as error:
                raise ValueError(
                    "Due date must use YYYY-MM-DD format."
                ) from error

        if not isinstance(due_date, datetime.date):
            raise TypeError("Due date must be a date or YYYY-MM-DD string.")

        self.due_date = due_date

    def to_dict(self):
        """Convert the due-date task to a dictionary."""
        data = super().to_dict()
        data["type"] = "due_date"
        data["due_date"] = self.due_date.isoformat()
        return data

    @classmethod
    def from_dict(cls, data):
        """Restore a due-date task from a dictionary."""
        return cls(
            task_id=data["id"],
            description=data["description"],
            due_date=data["due_date"],
            completed=data.get("completed", False),
            tags=data.get("tags", []),
        )

    def __str__(self):
        return f"{super().__str__()} | Due date: {self.due_date.isoformat()}"


class PriorityTask(Task):
    """Represent a task with a priority level."""

    VALID_PRIORITIES = {"High", "Medium", "Low"}

    def __init__(
        self,
        task_id,
        description,
        priority,
        completed=False,
        tags=None,
    ):
        super().__init__(task_id, description, completed, tags)

        if not isinstance(priority, str):
            raise ValueError("Priority must be High, Medium, or Low.")

        normalized_priority = priority.strip().capitalize()

        if normalized_priority not in self.VALID_PRIORITIES:
            raise ValueError("Priority must be High, Medium, or Low.")

        self.priority = normalized_priority

    def to_dict(self):
        """Convert the priority task to a dictionary."""
        data = super().to_dict()
        data["type"] = "priority"
        data["priority"] = self.priority
        return data

    @classmethod
    def from_dict(cls, data):
        """Restore a priority task from a dictionary."""
        return cls(
            task_id=data["id"],
            description=data["description"],
            priority=data["priority"],
            completed=data.get("completed", False),
            tags=data.get("tags", []),
        )

    def __str__(self):
        return f"{super().__str__()} | Priority: {self.priority}"