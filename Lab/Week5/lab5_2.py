# ============================================================
# Lab 5.2: Course Enrollment & Collaboration
# Set Focus
# ============================================================

# ข้อ 1 และ 2: กำหนด Set ของนักศึกษา
python_students = {"S001", "S003", "S005", "S007", "S009"}
java_students = {"S002", "S003", "S006", "S007", "S010"}

print(f"Python Students: {python_students}")
print(f"Java Students:   {java_students}\n")

# ข้อ 3: นักศึกษาที่เรียนทั้งสองวิชา
both_courses = python_students.intersection(java_students)
print(f"Students in Both Courses: {both_courses}")

# ข้อ 4: นักศึกษาทั้งหมดแบบไม่ซ้ำกัน
all_unique_students = python_students.union(java_students)
print(f"All Unique Students: {all_unique_students}")

# ข้อ 5: นักศึกษาที่เรียนเฉพาะ Python
only_python = python_students.difference(java_students)
print(f"Students Only in Python: {only_python}")

# ข้อ 6: นักศึกษาที่เรียนเพียงวิชาใดวิชาหนึ่ง
exclusive_students = python_students.symmetric_difference(java_students)
print(f"Students in Only One Course: {exclusive_students}\n")

# ข้อ 7: ลบข้อมูลซ้ำออกจาก List
all_students_list = ["S001", "S003", "S005", "S001", "S002"]

print(f"Original List (with duplicates): {all_students_list}")

unique_students_list = list(set(all_students_list))
print(f"Unique List (after removing duplicates): {unique_students_list}")