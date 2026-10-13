# Week7/main.py

from src.scraper import SimpleWebScraper


def main():
    """จุดเริ่มต้นหลักของโปรแกรม"""

    target_url = "https://automatetheboringstuff.com/3e/"
    scraper = SimpleWebScraper(target_url)

    scraped_data = scraper.scrape_main_titles()

    if scraped_data:
        print("\n--- ข้อมูลที่ Scrape ได้ ---")
        print(f"ชื่อหนังสือ: {scraped_data['book_title']}")

        print("\nชื่อบทต่าง ๆ:")

        if scraped_data["chapter_titles"]:
            for i, title in enumerate(
                scraped_data["chapter_titles"], start=1
            ):
                print(f"{i}. {title}")
        else:
            print("ไม่พบชื่อบท อาจต้องตรวจสอบโครงสร้าง HTML")

        print("--------------------")
    else:
        print("ไม่สามารถดึงข้อมูลจากเว็บไซต์ได้")


if __name__ == "__main__":
    main()