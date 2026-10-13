# Lab 6.2: การสร้าง Custom Module และการใช้งาน Standard Library
# File: main_program.py

# นำเข้าโมดูลที่สร้างขึ้นเอง
import Lab.Week6.my_utils as my_utils

# นำเข้าโมดูลมาตรฐานสำหรับคำนวณทางคณิตศาสตร์
import math

# นำเข้าโมดูลมาตรฐานสำหรับสุ่มตัวเลข
import random


# แสดงหัวข้อการใช้งาน Custom Module
print("===== การใช้งาน Custom Module =====")

# เรียกใช้ฟังก์ชัน greet() เพื่อแสดงข้อความทักทาย
my_utils.greet("Alice")

# ทดสอบว่าตัวเลขเป็นจำนวนเฉพาะหรือไม่
print("7 เป็นจำนวนเฉพาะหรือไม่?", my_utils.is_prime(7))
print("10 เป็นจำนวนเฉพาะหรือไม่?", my_utils.is_prime(10))
print("2 เป็นจำนวนเฉพาะหรือไม่?", my_utils.is_prime(2))
print("1 เป็นจำนวนเฉพาะหรือไม่?", my_utils.is_prime(1))


# แสดงหัวข้อการใช้งาน Math Module
print("\n===== การใช้งาน Math Module =====")

# กำหนดตัวเลขที่ต้องการหารากที่สอง
number = 25

# ใช้ math.sqrt() คำนวณรากที่สองของตัวเลข
result = math.sqrt(number)

# แสดงผลลัพธ์การคำนวณรากที่สอง
print(f"รากที่สองของ {number} คือ {result}")

# แสดงค่าพาย (Pi) จากโมดูล math
print(f"ค่าพาย (Pi) คือ {math.pi}")


# แสดงหัวข้อการใช้งาน Random Module
print("\n===== การใช้งาน Random Module =====")

# สุ่มจำนวนเต็มตั้งแต่ 1 ถึง 100
random_number = random.randint(1, 100)

# แสดงตัวเลขที่สุ่มได้
print(f"ตัวเลขสุ่มระหว่าง 1 ถึง 100 คือ {random_number}")