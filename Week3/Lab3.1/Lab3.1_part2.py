# --- Lab 3.1 Part 2: Full 12x12 Multiplication Grid ---
print("12x12 Multiplication Table:")

for i in range(1, 13):
    for j in range(1, 13):
        print(f"{i*j:4}", end="")
    print()

print()  # spacer