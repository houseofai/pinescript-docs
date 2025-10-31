import os
import time

from bs4 import BeautifulSoup
from markdownify import markdownify
from tqdm import tqdm

from src.utils import (
    create_selenium_driver,
    get_doc_links,
    clean_html_content,
    format_title_for_filename
)


def crawl_indicators():
    """Crawl TradingView built-in indicators documentation."""
    URL = "https://www.tradingview.com/support/folders/43000587405-built-in-indicators/"
    OUTPUT_DIR = "../docs/markdown/built-in-indicators"

    print(f"Crawling built-in indicators from {URL}...")

    # Get all documentation links
    urls = get_doc_links(URL)
    urls = [url for url in urls if url.startswith("https://www.tradingview.com/support/solutions/")]

    if not urls:
        print("No URLs found to crawl.")
        return

    print(f"Found {len(urls)} URLs to process")

    # Create output directory
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # Initialize Selenium driver
    driver = create_selenium_driver()

    try:
        pbar = tqdm(urls, desc="Processing indicators")

        for url in pbar:
            pbar.set_description(f"Processing {url.split('/')[-1]}")

            # Load the webpage
            driver.get(url)
            time.sleep(2)  # Wait for JavaScript to load

            # Parse HTML
            soup = BeautifulSoup(driver.page_source, "html.parser")

            # Extract main content
            content_div = soup.select_one('div[itemprop="text"][class^="solution-"]')
            if not content_div:
                print(f"\nWarning: Could not find content in {url}")
                continue

            # Clean HTML content
            content_div = clean_html_content(content_div)

            # Convert to markdown
            markdown_content = markdownify(str(content_div))

            # Extract title
            title_element = soup.select_one('[class^="page-title"] > span:nth-child(1)')
            if not title_element:
                print(f"\nWarning: Could not find title in {url}")
                continue

            # Save to file
            filename = f"{OUTPUT_DIR}/{format_title_for_filename(title_element.text)}.md"
            with open(filename, "w", encoding="utf-8") as file:
                file.write(markdown_content)

        print(f"\n✓ Successfully crawled {len(urls)} indicators to {OUTPUT_DIR}")

    finally:
        driver.quit()


if __name__ == "__main__":
    crawl_indicators()
