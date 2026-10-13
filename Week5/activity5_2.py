# ============================================================
# Activity 5.2: Word Frequency Counter
# ============================================================

import string

# ขั้นตอนที่ 1: รับข้อความจากผู้ใช้
sentence = input("Enter a sentence: ")

# ขั้นตอนที่ 2: แปลงเป็นตัวพิมพ์เล็ก
sentence = sentence.lower()

# ขั้นตอนที่ 3: แยกข้อความเป็นคำ
words = sentence.split()

# ขั้นตอนที่ 4: สร้าง Dictionary ว่าง
word_counts = {}

# ขั้นตอนที่ 5-8: ทำความสะอาดคำและนับความถี่
for word in words:
    # ลบเครื่องหมายวรรคตอนที่อยู่หัวและท้ายคำ
    word = word.strip(string.punctuation)

    # ข้ามข้อมูลที่ไม่มีตัวอักษรหรือเครื่องหมายเหลืออยู่
    if not word:
        continue

    if word in word_counts:
        word_counts[word] += 1
    else:
        word_counts[word] = 1

# ขั้นตอนที่ 9: แสดงผล
print("\n--- Word Frequency ---")

for word, count in word_counts.items():
    print(f"{word}: {count}")

print("\nWord Counts Dictionary:", word_counts)