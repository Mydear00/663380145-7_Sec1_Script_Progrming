# Week10_LabX ADV — Advanced Spreadsheet Automation & Agentic Workflows

โปรเจกต์นี้เป็น Agentic Sales Reporter ใช้ Python + `openpyxl` อ่านข้อมูลยอดขายจาก Excel แล้วรันงานตาม JSON configuration

## Features
- คัดลอกข้อมูลไปยัง `Raw Data`
- ใส่สูตรคำนวณ `Total Revenue = Quantity × Unit Price`
- ทำ Conditional Formatting สำหรับรายได้และสถานะ
- สร้างชีต `Summary` และกราฟรายได้ตามสินค้า
- สร้างชีต `Audit Log` บันทึกงานที่สำเร็จ/ผิดพลาด
- บันทึก log ลง `data/agent.log`
- มี placeholder สำหรับ Google Sheets API (ยังไม่ได้เชื่อมต่อจริง)

## Requirements
- Python 3.10+
- `openpyxl`

## Run on Windows PowerShell
```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install openpyxl
python main.py
```

ถ้า PowerShell ไม่อนุญาตให้ activate venv ให้รัน `python -m pip install openpyxl` แล้ว `python main.py` ได้โดยตรง

## Input data
ไฟล์ `data/input_data.xlsx` มีชีต `SalesData` และคอลัมน์ `Product Name`, `Quantity`, `Unit Price`

## Output
หลังรันจะได้ `data/output_report.xlsx` ซึ่งมี `Audit Log`, `SalesData`, `Raw Data`, `Summary` และกราฟ

หมายเหตุ: openpyxl ใส่สูตรลงใน Excel แต่ไม่ได้คำนวณสูตรให้เอง ค่า formula จะถูกคำนวณเมื่อเปิดไฟล์ด้วย Excel หรือโปรแกรมสเปรดชีตที่รองรับ ส่วน Summary ของตัวอย่างนี้คำนวณยอดจาก Quantity × Unit Price โดยตรงเพื่อให้รายงานมีตัวเลขทันที

## Configuration
แก้ `configs/example_spreadsheet_config.json` เพื่อเปลี่ยนไฟล์ต้นทาง ปลายทาง และลำดับ tasks ได้
