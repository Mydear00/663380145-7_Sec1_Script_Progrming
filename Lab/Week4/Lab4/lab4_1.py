print("--- Lab 4.1: Student Management System ---")

student_names = []

while True:
    print("\n========== MENU ==========")
    print("1. Add Student")
    print("2. Find Student")
    print("3. Remove Student")
    print("4. Sort Students")
    print("5. View Students")
    print("6. Count Students")
    print("7. Exit")
    print("==========================")

    choice = input("Enter your choice (1-7): ")

    # เพิ่มนักศึกษา
    if choice == "1":
        print("\n[Add 3 Students]")
        for i in range(3):
            name = input(f"Enter student name #{i + 1}: ")
            student_names.append(name)

        print("Students have been added.")
        print(f"Current list: {student_names}")

    # ค้นหานักศึกษา
    elif choice == "2":
        search_name = input("Enter a name to search: ")
        if search_name in student_names:
            position = student_names.index(search_name)
            print(f"Found '{search_name}' at index {position}")
        else:
            print(f"'{search_name}' not found.")

    # ลบนักศึกษา
    elif choice == "3":
        remove_name = input("Enter a name to remove: ")
        if remove_name in student_names:
            student_names.remove(remove_name)
            print(f"'{remove_name}' has been removed.")
        else:
            print(f"'{remove_name}' not found.")

    # เรียงลำดับ
    elif choice == "4":
        student_names.sort()
        print("Students have been sorted.")
        print(student_names)

    # แสดงรายชื่อทั้งหมด
    elif choice == "5":
        if len(student_names) == 0:
            print("No students in the list.")
        else:
            print("\nStudent List")
            for i, name in enumerate(student_names, start=1):
                print(f"{i}. {name}")

    # นับจำนวนนักศึกษา
    elif choice == "6":
        print(f"Total students: {len(student_names)}")

    # ออกจากโปรแกรม
    elif choice == "7":
        print("Exiting program...")
        break

    # กรอกเมนูผิด
    else:
        print("Invalid choice! Please try again.")