import math

print("--- Lab 4.2: Geometric Calculations ---")

# 1) กำหนดจุดสองจุดด้วย tuple
point1 = (3, 4)
point2 = (6, 8)

# 2) เข้าถึงค่าพิกัด x, y ของแต่ละจุด
print("\n[1] Access Coordinates")
print(f"Point 1: x = {point1[0]}, y = {point1[1]}")
print(f"Point 2: x = {point2[0]}, y = {point2[1]}")

# 3) ทดลองแก้ไขค่าใน tuple
print("\n[2] Attempt Modification (Immutability Demonstration)")
try:
    point1[0] = 5
except TypeError as e:
    print(f"Error trying to modify tuple: {e}")

# 4) คำนวณระยะห่างระหว่างจุดสองจุด
print("\n[3] Calculate Distance")
distance = math.sqrt((point2[0] - point1[0]) ** 2 + (point2[1] - point1[1]) ** 2)
print(f"Distance between point1 {point1} and point2 {point2}: {distance}")