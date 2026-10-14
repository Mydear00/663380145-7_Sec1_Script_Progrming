"""
Module: main.py
Description: Entry point for the API Data Fetcher CLI.
"""

from src.api_client import APIClient


def display_menu() -> None:
    """แสดงเมนูหลัก."""
    print("\n" + "=" * 42)
    print("         API DATA FETCHER CLI")
    print("=" * 42)
    print("  1. Fetch a Single TODO Item")
    print("  2. Fetch All Posts")
    print("  3. Fetch TODOs by User ID")
    print("  4. Exit")
    print("=" * 42)


def get_positive_integer(prompt: str) -> int:
    """รับค่าจำนวนเต็มบวกจากผู้ใช้."""
    value = int(input(prompt).strip())

    if value <= 0:
        raise ValueError("Please enter a positive integer.")

    return value


def show_single_todo(client: APIClient) -> None:
    """ดึงและแสดงข้อมูล TODO หนึ่งรายการ."""
    try:
        todo_id = get_positive_integer("Enter TODO ID: ")
    except ValueError:
        print("Error: Please enter a valid positive number.")
        return

    todo = client.fetch_single_todo(todo_id)

    if todo is None:
        print("Could not retrieve the TODO item.")
        return

    if not isinstance(todo, dict) or "id" not in todo:
        print("No valid TODO item was returned.")
        return

    print("\n--- TODO Item Details ---")
    print(f"ID: {todo.get('id')}")
    print(f"User ID: {todo.get('userId')}")
    print(f"Title: {todo.get('title')}")
    print(
        "Status: "
        f"{'Completed' if todo.get('completed') else 'Pending'}"
    )
    print("-------------------------")


def show_all_posts(client: APIClient) -> None:
    """ดึงโพสต์ทั้งหมดและแสดง 5 รายการแรก."""
    posts = client.fetch_all_posts()

    if posts is None:
        print("Could not retrieve posts.")
        return

    if not isinstance(posts, list):
        print("Error: Unexpected data format from API.")
        return

    if not posts:
        print("No posts found.")
        return

    print("\n--- First 5 Posts ---")

    for post in posts[:5]:
        print(f"\nPost ID: {post.get('id')}")
        print(f"Title: {post.get('title')}")

        body = post.get("body", "")
        print(f"Body: {body[:100]}{'...' if len(body) > 100 else ''}")
        print("-" * 40)

    if len(posts) > 5:
        print(f"Displaying 5 of {len(posts)} posts.")

    print("---------------------")


def show_user_todos(client: APIClient) -> None:
    """ดึงและแสดง TODO ของผู้ใช้."""
    try:
        user_id = get_positive_integer("Enter User ID: ")
    except ValueError:
        print("Error: Please enter a valid positive number.")
        return

    todos = client.fetch_user_todos(user_id)

    if todos is None:
        print(f"Could not retrieve TODOs for User ID {user_id}.")
        return

    if not isinstance(todos, list):
        print("Error: Unexpected data format from API.")
        return

    print(f"\n--- TODOs for User ID {user_id} ---")

    if not todos:
        print("No TODOs found for this user.")
        return

    for todo in todos:
        status = "Completed" if todo.get("completed") else "Pending"

        print(
            f"ID: {todo.get('id')} | "
            f"Title: {todo.get('title')} | "
            f"Status: {status}"
        )

    print("-" * 60)
    print(f"Total TODOs: {len(todos)}")


def main() -> None:
    """เริ่มการทำงานของโปรแกรม."""
    client = APIClient()

    while True:
        display_menu()
        choice = input("Enter your choice (1-4): ").strip()

        # แสดงเส้นคั่นก่อนดำเนินการตามเมนู
        print("=" * 42)

        if choice == "1":
            show_single_todo(client)

        elif choice == "2":
            show_all_posts(client)

        elif choice == "3":
            show_user_todos(client)

        elif choice == "4":
            print("Exiting API Data Fetcher. Goodbye!")
            break

        else:
            print("Invalid choice. Please select 1, 2, 3, or 4.")


if __name__ == "__main__":
    main()