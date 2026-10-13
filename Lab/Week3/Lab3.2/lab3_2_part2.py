print("=== ส่วนที่ 2: เกมทายตัวเลขปริศนา ===")
secret_number = 42
attempts = 0
max_attempts = 5

print(f"(ทายเลข)เลือก 1 ถึง 100 ลองทายซิ! (มีโอกาสทาย {max_attempts} ครั้ง)")

while True:
    try:
        guess = int(input(f"รอบที่ {attempts + 1}/{max_attempts} - Guess the number: "))
        attempts += 1
        
        if guess == secret_number:
            print( "Congratulations! You guessed it!")
            break  # ออกจากลูปทันทีเมื่อทายถูก
        elif guess < secret_number:
            print("Too low! Try again.")
        else:
            print("Too high! Try again.")
            
        # ตรวจสอบเงื่อนไขท้าทาย: หากใช้โควตาครบแล้ว
        if attempts >= max_attempts:
            print(f"\nจบเกม! คุณหมดสิทธิ์ทายแล้ว ตัวเลขที่ถูกต้องคือ {secret_number}")
            break
            
    except ValueError:
        print("คำเตือน: กรุณากรอกเฉพาะตัวเลขจำนวนเต็มเท่านั้น")