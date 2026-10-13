print("--- Activity 4.2 : To-Do List ---")

todo_list = []

while True:
    print("\n===== MENU =====")
    print("1. Add Task")
    print("2. View Tasks")
    print("3. Complete Task")
    print("4. Exit")

    choice = input("Enter your choice: ")

    # เพิ่มงาน
    if choice == "1":
        task = input("Enter task: ")
        todo_list.append(task)
        print("Task added.")

    # ดูงานทั้งหมด
    elif choice == "2":
        if len(todo_list) == 0:
            print("No tasks.")
        else:
            print("\nTo-Do List")
            for i, task in enumerate(todo_list, start=1):
                print(f"{i}. {task}")

    # ทำงานเสร็จ (ลบงาน)
    elif choice == "3":
        if len(todo_list) == 0:
            print("No tasks to remove.")
        else:
            task = input("Enter task name to complete: ")

            if task in todo_list:
                todo_list.remove(task)
                print("Task completed and removed.")
            else:
                print("Task not found.")

    # ออกจากโปรแกรม
    elif choice == "4":
        print("Goodbye!")
        break

    else:
        print("Invalid choice.")