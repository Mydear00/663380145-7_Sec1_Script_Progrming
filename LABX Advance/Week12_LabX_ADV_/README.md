# Week12 LabX ADV — Agentic Communication Workflows

ระบบตัวอย่าง Communication Agent ที่อ่านงานจากไฟล์ JSON แล้วประมวลผลอีเมล, SMS, กฎจัดการกล่องจดหมาย และบันทึก Audit Log

## ความสามารถ
- อ่านการตั้งค่าจาก `configs/comm_pipeline_config.json`
- ใช้ template เช่น `{report_date}`, `{sales_figure:.2f}` และตัวแปรจาก `.env` เช่น `${TEST_RECIPIENT_EMAIL}`
- ส่งอีเมลพร้อมไฟล์แนบหลายไฟล์ (To/CC/BCC และ HTML)
- ส่ง SMS ผ่าน email-to-SMS gateway ที่ผู้ให้บริการรองรับ
- ค้นหาอีเมลผ่าน IMAP, ดาวน์โหลดไฟล์แนบตามนามสกุล, ทำเครื่องหมายว่าอ่านแล้ว และใช้กฎส่ง SMS/ตอบกลับ
- เขียน audit log เป็น JSON ใน `reports/`

## 1. เปิดโฟลเดอร์และติดตั้ง
Windows PowerShell:
```powershell
cd "D:\663380145-7_Sec1_Script_Progrming\LABX Advance\Week12_LabX ADV_"
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```
หาก PowerShell ไม่อนุญาตให้ activate ให้ใช้ `python -m pip install -r requirements.txt` โดยไม่ activate ก็ได้

## 2. ตั้งค่า `.env`
เปิด `.env` และกรอกอีเมลที่ใช้ทดสอบ, Gmail App Password และผู้รับที่ควบคุมได้เอง อย่าใช้รหัสผ่าน Gmail ปกติ และอย่าอัปโหลด `.env` ไป GitHub

**ค่าเริ่มต้น `DRY_RUN=true` ปลอดภัยที่สุด:** ระบบจะแสดงตัวอย่างข้อความ ไม่ส่งอีเมล/SMS จริงและไม่เชื่อม IMAP เพื่ออ่านกล่องจดหมาย

เมื่อทดสอบ config และผู้รับเรียบร้อยแล้ว และต้องการส่งจริง ให้เปลี่ยนเป็น `DRY_RUN=false` ด้วยความระมัดระวัง ก่อนใช้ IMAP ต้องเปิด IMAP ในบัญชีอีเมล และตั้งค่า App Password ให้ถูกต้อง

## 3. รันโปรแกรม
```powershell
python main.py
```
ระบบจะสร้าง audit log ที่ `reports/audit_report_comm_YYYYMMDD_HHMMSS.json`

## 4. ไฟล์ตัวอย่าง
- `data/reports/sales_report.pdf` — รายงานตัวอย่าง PDF
- `data/reports/summary_data.xlsx` — ข้อมูลตัวอย่าง Excel

## ข้อควรทราบ
- Email-to-SMS gateway ไม่รองรับทุกเครือข่าย/ทุกประเทศ; ในไทยมักไม่มี gateway สาธารณะให้ใช้ได้ทั่วไป หากใช้ไม่ได้ให้คง `DRY_RUN=true` หรือเปลี่ยนไปใช้ผู้ให้บริการ SMS API ที่ได้รับอนุญาต
- Workflow ส่งอีเมลจำลองคำขอเข้าหาตัวเองไว้ใน config แต่ในโหมด DRY RUN จะไม่ส่งจริง
- IMAP search มีความแตกต่างตามผู้ให้บริการอีเมล ควรทดสอบกับบัญชีที่ควบคุมเอง
- ตรวจสอบผู้รับและข้อความทุกครั้งก่อนตั้ง `DRY_RUN=false`
