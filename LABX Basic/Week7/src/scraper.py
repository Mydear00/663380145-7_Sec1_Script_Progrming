# Week7/src/scraper.py

import requests
from bs4 import BeautifulSoup


class SimpleWebScraper:
    """คลาสสำหรับดึงข้อมูลพื้นฐานจากเว็บไซต์"""

    def __init__(self, target_url):
        self.target_url = target_url

    def _get_html_content(self):
        """ดาวน์โหลดเนื้อหา HTML จากเว็บไซต์"""

        print(f"กำลังดาวน์โหลดเนื้อหาจาก: {self.target_url}")

        headers = {
            "User-Agent": "EducationalWebScraper/1.0"
        }

        try:
            response = requests.get(
                self.target_url,
                headers=headers,
                timeout=30
            )

            response.raise_for_status()
            response.encoding = response.apparent_encoding

            print("ดาวน์โหลดเนื้อหาสำเร็จ")
            return response.text

        except requests.exceptions.HTTPError as e:
            print(f"เกิดข้อผิดพลาด HTTP: {e}")
        except requests.exceptions.ConnectionError:
            print("ไม่สามารถเชื่อมต่อเว็บไซต์ได้")
        except requests.exceptions.Timeout:
            print("การร้องขอใช้เวลานานเกินไป")
        except requests.exceptions.RequestException as e:
            print(f"เกิดข้อผิดพลาด: {e}")

        return None

    def scrape_main_titles(self):
        """ดึงชื่อหนังสือและชื่อบทจากหน้าเว็บไซต์"""

        html_content = self._get_html_content()

        if not html_content:
            return None

        soup = BeautifulSoup(html_content, "html.parser")

        # ดึงชื่อหนังสือจาก h1
        book_title_tag = soup.find("h1")

        if book_title_tag:
            book_title = book_title_tag.get_text(" ", strip=True)
        else:
            book_title = "ไม่พบชื่อหนังสือ"

        # ดึงรายการลิงก์ที่อาจเป็นชื่อบท
        chapter_titles = []

        # ลองค้นหาจากส่วนสารบัญก่อน
        content_body = soup.find("div", class_="content-body")

        if content_body:
            chapter_links = content_body.select("ul li a")
        else:
            # ใช้ตัวเลือกสำรองสำหรับเว็บไซต์ที่มีสารบัญแบบอื่น
            chapter_links = soup.select(
                "div.toctree-wrapper li a, "
                "nav a, "
                "main a"
            )

        for link in chapter_links:
            title = link.get_text(" ", strip=True)

            if title and title not in chapter_titles:
                chapter_titles.append(title)

        return {
            "book_title": book_title,
            "chapter_titles": chapter_titles
        }