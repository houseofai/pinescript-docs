import os
import time

from bs4 import BeautifulSoup
from markdownify import markdownify

from src.utils import create_selenium_driver, format_title_for_filename


def crawl_reference():
    """Crawl Pine Script reference manual."""
    URL = "https://www.tradingview.com/pine-script-reference/v6/"
    OUTPUT_DIR = "../docs/markdown"

    print(f"Crawling Pine Script reference from {URL}...")

    # Create output directory
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # Initialize Selenium driver
    driver = create_selenium_driver()

    try:
        # Load the webpage
        driver.get(URL)
        time.sleep(2)  # Wait for JavaScript to load

        # Parse HTML
        soup = BeautifulSoup(driver.page_source, "html.parser")

        # Extract main content
        content_div = soup.select_one('div[class^="tv-script-reference__right-column"]')
        if not content_div:
            raise Exception(f"Could not find the main content div in {URL}")

        # Convert to markdown
        markdown_content = markdownify(str(content_div))

        # Extract title
        title_element = soup.select_one('h1[class^="tv-script-reference__main-header"]')
        if not title_element:
            raise Exception(f"Could not find title in {URL}")

        title = title_element.text

        # Save to file
        filename = f"{OUTPUT_DIR}/{format_title_for_filename(title)}.md"
        with open(filename, "w", encoding="utf-8") as file:
            file.write(markdown_content)

        print(f"✓ Successfully crawled reference to {filename}")

    finally:
        driver.quit()


if __name__ == "__main__":
    crawl_reference()