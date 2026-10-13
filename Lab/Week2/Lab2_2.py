age = int(input("Enter your age: "))

if age < 5:
    print("Recommended Rating: Cartoons")
elif age <= 12:
    print("Recommended Rating: G / PG")
elif age <= 17:
    print("Recommended Rating: PG-13 / R")
else:
    print("Recommended Rating: Any Rating")

like = input("Do you like action movies? (yes/no): ").strip().lower()

if like == "yes":
    print("Recommended Movie: Mission: Impossible")
else:
    print("Recommended Movie: Inside Out")