# ============================================================
# Lab 5.1: Simple Contact Book Manager
# Dictionary Focus
# ============================================================

# ข้อ 1: สร้าง Dictionary ว่าง
contacts = {}

while True:
    print("\n=== Contact Book Manager ===")
    print("1. Add/Update Contact")
    print("2. View Contact Details")
    print("3. List All Contacts")
    print("4. Delete Contact")
    print("5. Exit")

    choice = input("Enter choice (1-5): ")

    # เมนู 1: เพิ่มหรืออัปเดตข้อมูล
    if choice == '1':
        name = input("Enter contact name: ").strip().lower()
        phone = input("Enter phone number: ")
        email = input("Enter email: ")

        # ข้อ 2: บันทึกข้อมูลลง Dictionary
        contacts[name] = {
            "phone": phone,
            "email": email
        }

        print(f"Contact '{name}' saved successfully!")

    # เมนู 2: ดูรายละเอียดผู้ติดต่อ
    elif choice == '2':
        name = input("Enter contact name to view: ").strip().lower()

        # ข้อ 3: ใช้ get() ค้นหาข้อมูล
        info = contacts.get(name)

        if info:
            print(f"\nName: {name}")
            print(f"Phone: {info['phone']}")
            print(f"Email: {info['email']}")
        else:
            print("Contact not found.")

    # เมนู 3: แสดงรายชื่อทั้งหมด
    elif choice == '3':
        if not contacts:
            print("No contacts available.")
        else:
            print("\n--- All Contacts ---")

            # ข้อ 4: ใช้ items() วนลูป
            for name, details in contacts.items():
                print(
                    f"Name: {name} | "
                    f"Phone: {details['phone']} | "
                    f"Email: {details['email']}"
                )

    # เมนู 4: ลบข้อมูล
    elif choice == '4':
        name = input("Enter contact name to delete: ").strip().lower()

        # ข้อ 5: ใช้ pop() และกำหนดค่าเริ่มต้นเป็น None
        removed_contact = contacts.pop(name, None)

        if removed_contact is not None:
            print(f"Contact '{name}' deleted successfully!")
        else:
            print("Contact not found.")

    # เมนู 5: ออกจากโปรแกรม
    elif choice == '5':
        print("Exiting Contact Book Manager. Goodbye!")

        # ข้อ 6: หยุด while loop
        break

    else:
        print("Invalid choice! Please enter a number from 1 to 5.")