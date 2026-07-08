print("=== ส่วนที่ 2: เกมทายตัวเลขปริศนา ===")
secret_number = 42
attempts = 0
max_attempts = 5

print(f"(ทายเลข)เลือก 1 ถึง 100 ลองทายซิ! (มีโอกาสทาย {max_attempts} ครั้ง)")

while True:
    try:
        guess = int(input(f"รอบที่ {attempts + 1}/{max_attempts} - ทายตัวเลขของคุณ: "))
        attempts += 1
        
        if guess == secret_number:
            print("ยินดีด้วย! คุณทายถูกแล้ว!")
            break  # ออกจากลูปทันทีเมื่อทายถูก
        elif guess < secret_number:
            print("น้อยเกินไป! ลองใหม่อีกครั้ง")
        else:
            print("มากเกินไป! ลองใหม่อีกครั้ง")
            
        # ตรวจสอบเงื่อนไขท้าทาย: หากใช้โควตาครบแล้ว
        if attempts >= max_attempts:
            print(f"\nจบเกม! คุณหมดสิทธิ์ทายแล้ว ตัวเลขที่ถูกต้องคือ {secret_number}")
            break
            
    except ValueError:
        print("คำเตือน: กรุณากรอกเฉพาะตัวเลขจำนวนเต็มเท่านั้น")