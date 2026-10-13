print("=== ส่วนที่ 1: โปรแกรมนับถอยหลัง ===")
try:
    count = int(input("กรอกตัวเลขเริ่มต้นสำหรับนับถอยหลัง: "))
    
    while count >= 0:
        print(count)
        count -= 1  # ขั้นตอนสำคัญ! ลดค่าลงเพื่อไม่ให้เกิด Infinite Loop (ลูปไม่รู้จบ)
    print("Blast off! 🚀")
except ValueError:
    print("ข้อผิดพลาด: กรุณากรอกเฉพาะตัวเลขจำนวนเต็มเท่านั้น")

print("\n" + "-"*40 + "\n")