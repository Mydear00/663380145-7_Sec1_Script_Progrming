
"""
Module: task.py
Description: Defines the Task class.
"""


class Task:
    """แทนรายการงานหนึ่งรายการ."""

    def __init__(
        self,
        id: int,
        description: str,
        completed: bool = False,
        priority: str = "Medium"
    ):
        """กำหนดค่าเริ่มต้นให้กับวัตถุ Task."""
        self.id = id
        self.description = description
        self.completed = completed
        self.priority = priority

    def mark_complete(self) -> None:
        """เปลี่ยนสถานะงานเป็นเสร็จแล้ว."""
        self.completed = True

    def to_dict(self) -> dict:
        """แปลง Task object เป็น Dictionary สำหรับบันทึก JSON."""
        return {
            "id": self.id,
            "description": self.description,
            "completed": self.completed,
            "priority": self.priority
        }

    def __str__(self) -> str:
        """แสดงข้อมูลงานให้อ่านง่าย."""
        status = "DONE" if self.completed else "PENDING"
        return (
            f"#{self.id:<3} | [{status:<7}] | "
            f"{self.priority:<8} | {self.description}"
        )

    def __repr__(self) -> str:
        """แสดงข้อมูลวัตถุสำหรับช่วยตรวจสอบโค้ด."""
        return (
            f"Task(id={self.id!r}, "
            f"description={self.description!r}, "
            f"completed={self.completed!r}, "
            f"priority={self.priority!r})"
        )
