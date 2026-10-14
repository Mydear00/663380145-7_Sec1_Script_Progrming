# src/task.py

class Task:
    """
    คลาสสำหรับจำลองข้อมูลงานแต่ละรายการ (Single Task)

    Attributes:
        id (int): รหัสประจำงานที่ไม่ซ้ำกัน
        description (str): รายละเอียดข้อความของงาน
        completed (bool): สถานะการทำงาน
    """

    def __init__(
        self,
        id: int,
        description: str,
        completed: bool = False
    ):
        """Constructor สำหรับสร้าง Instance ของ Task."""
        self.id = id
        self.description = description
        self.completed = completed

    def mark_complete(self):
        """เปลี่ยนสถานะของงานเป็นเสร็จสมบูรณ์."""
        self.completed = True

    def to_dict(self) -> dict:
        """แปลง Task Object เป็น Dictionary สำหรับบันทึก JSON."""
        return {
            "id": self.id,
            "description": self.description,
            "completed": self.completed
        }

    def __str__(self) -> str:
        """แสดงข้อมูลงานในรูปแบบที่อ่านง่าย."""
        status = "Completed" if self.completed else "Pending"

        return (
            f"ID: {self.id} | "
            f"Description: {self.description} | "
            f"Status: {status}"
        )

    def __repr__(self) -> str:
        """แสดงข้อมูลเชิงเทคนิคสำหรับ Debugging."""
        return (
            f"Task(id={self.id!r}, "
            f"description={self.description!r}, "
            f"completed={self.completed!r})"
        )