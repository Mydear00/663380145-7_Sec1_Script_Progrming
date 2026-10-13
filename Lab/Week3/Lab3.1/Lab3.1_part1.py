# --- Lab 3.1 Part 1: Single Number Multiplication Table ---
n = int(input("Enter a number for its multiplication table (e.g., 7): "))

for i in range(1, 13):
    print(f"{n} * {i} = {n * i}")

print()  # spacer