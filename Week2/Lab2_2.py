age = int(input("Enter your age: "))

if age < 5:
    print("You are a toddler.")
elif age <= 12:
    print("You are a child.")
elif age <= 17:
    print("You are a teenager.")
else:
    print("You are an adult.")

like = input("Do you like action movies? (yes/no): ").strip().lower()

if like == "yes":
    print("Since you like action movies, I recommend Mission: Impossible.")
else:
    print("If action movies are not your thing, you might enjoy Inside Out.")