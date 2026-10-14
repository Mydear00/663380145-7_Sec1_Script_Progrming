"""
Module: api_client.py
Description: Fetches and processes data from JSONPlaceholder API.
"""

import requests


class APIClient:
    """คลาสสำหรับเรียกใช้งาน JSONPlaceholder API."""

    BASE_URL = "https://jsonplaceholder.typicode.com"

    def _make_request(self, endpoint: str):
        """ส่ง GET request และคืนค่าข้อมูล JSON หรือ None เมื่อเกิดข้อผิดพลาด."""
        url = f"{self.BASE_URL}{endpoint}"

        print(f"\nFetching data from: {url}")

        try:
            response = requests.get(url, timeout=10)

            print(f"HTTP Status Code: {response.status_code}")

            response.raise_for_status()

            try:
                return response.json()
            except requests.exceptions.JSONDecodeError:
                print("Error: The API returned invalid JSON.")
                print(f"Response: {response.text[:100]}")
                return None

        except requests.exceptions.HTTPError as error:
            print(f"HTTP Error: {error}")

        except requests.exceptions.ConnectionError as error:
            print(f"Connection Error: {error}")

        except requests.exceptions.Timeout:
            print("Timeout Error: The server took too long to respond.")

        except requests.exceptions.RequestException as error:
            print(f"Request Error: {error}")

        return None

    def fetch_single_todo(self, todo_id: int):
        """ดึงข้อมูล TODO ตาม ID."""
        return self._make_request(f"/todos/{todo_id}")

    def fetch_all_posts(self):
        """ดึงข้อมูลโพสต์ทั้งหมด."""
        return self._make_request("/posts")

    def fetch_user_todos(self, user_id: int):
        """ดึงรายการ TODO ของผู้ใช้ตาม User ID."""
        return self._make_request(f"/todos?userId={user_id}")