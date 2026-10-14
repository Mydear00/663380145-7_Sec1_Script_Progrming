"""Task models for the Enhanced Task Manager."""

import datetime


class Task:
    """Base class for all tasks."""

    def __init__(self, id, description, completed=False, tags=None):
        self.id = id
        self.description = description
        self.completed = completed
        self.tags = list(tags) if tags is not None else []

    def mark_complete(self):
        """Mark this task as completed."""
        self.completed = True

    def add_tag(self, tag):
        """Add a tag if it does not already exist."""
        tag = tag.strip()
        if tag and tag not in self.tags:
            self.tags.append(tag)

    def remove_tag(self, tag):
        """Remove a tag if it exists."""
        if tag in self.tags:
            self.tags.remove(tag)

    def to_dict(self):
        """Convert the task to a dictionary for JSON storage."""
        return {
            "id": self.id,
            "description": self.description,
            "completed": self.completed,
            "tags": self.tags,
            "_type": "Task",
        }

    def __str__(self):
        status = "Completed" if self.completed else "Pending"
        tags_text = f" | Tags: {', '.join(self.tags)}" if self.tags else ""

        return (
            f"ID: {self.id} | Description: {self.description} | "
            f"Status: {status}{tags_text}"
        )

    def __repr__(self):
        return (
            f"Task(id={self.id!r}, description={self.description!r}, "
            f"completed={self.completed!r}, tags={self.tags!r})"
        )


class DueDateTask(Task):
    """Task with a due date."""

    def __init__(self, id, description, due_date, completed=False, tags=None):
        super().__init__(id, description, completed, tags)

        if isinstance(due_date, str):
            self.due_date = datetime.datetime.strptime(
                due_date, "%Y-%m-%d"
            ).date()
        elif isinstance(due_date, datetime.datetime):
            self.due_date = due_date.date()
        elif isinstance(due_date, datetime.date):
            self.due_date = due_date
        else:
            raise TypeError(
                "due_date must be a YYYY-MM-DD string or date object"
            )

    def to_dict(self):
        data = super().to_dict()
        data["due_date"] = self.due_date.strftime("%Y-%m-%d")
        data["_type"] = "DueDateTask"
        return data

    def __str__(self):
        status = "Completed" if self.completed else "Pending"
        tags_text = f" | Tags: {', '.join(self.tags)}" if self.tags else ""

        return (
            f"ID: {self.id} | Description: {self.description} | "
            f"Status: {status} | Due: {self.due_date:%Y-%m-%d}{tags_text}"
        )

    def __repr__(self):
        return (
            f"DueDateTask(id={self.id!r}, description={self.description!r}, "
            f"due_date={self.due_date!r}, completed={self.completed!r}, "
            f"tags={self.tags!r})"
        )


class PriorityTask(Task):
    """Task with a priority level."""

    VALID_PRIORITIES = {"High", "Medium", "Low"}

    def __init__(self, id, description, priority, completed=False, tags=None):
        super().__init__(id, description, completed, tags)

        normalized_priority = str(priority).strip().capitalize()

        if normalized_priority not in self.VALID_PRIORITIES:
            raise ValueError("Priority must be High, Medium, or Low.")

        self.priority = normalized_priority

    def to_dict(self):
        data = super().to_dict()
        data["priority"] = self.priority
        data["_type"] = "PriorityTask"
        return data

    def __str__(self):
        status = "Completed" if self.completed else "Pending"
        tags_text = f" | Tags: {', '.join(self.tags)}" if self.tags else ""

        return (
            f"ID: {self.id} | Description: {self.description} | "
            f"Status: {status} | Priority: {self.priority}{tags_text}"
        )

    def __repr__(self):
        return (
            f"PriorityTask(id={self.id!r}, description={self.description!r}, "
            f"priority={self.priority!r}, completed={self.completed!r}, "
            f"tags={self.tags!r})"
        )