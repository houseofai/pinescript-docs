import os

import requests
from bs4 import BeautifulSoup
from markdownify import markdownify
from tqdm import tqdm

from utils import get_doc_links, format_title_for_filename


def crawl_docs():
    """Crawl Pine Script documentation."""
    BASE_URL = "https://www.tradingview.com/pine-script-docs/"
    OUTPUT_DIR = "../docs/markdown/pine-script-docs"

    print(f"Crawling Pine Script docs from {BASE_URL}...")

    # Get all documentation links
    links = get_doc_links(BASE_URL)

    if not links:
        print("No URLs found to crawl.")
        return

    print(f"Found {len(links)} links to process")

    # Create output directory
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    pbar = tqdm(links, desc="Processing docs")

    for link in pbar:
        pbar.set_description(f"Processing {link.split('/')[-1]}")

        # Fetch the webpage
        response = requests.get(link)
        if response.status_code != 200:
            print(f"\nWarning: Failed to retrieve {link}")
            continue

        # Parse HTML
        soup = BeautifulSoup(response.text, "html.parser")

        # Extract main content
        content_div = soup.select_one('div[id="slot-container"]')
        if not content_div:
            print(f"\nWarning: Could not find content in {link}")
            continue

        # Extract title
        title_element = soup.select_one('h1')
        if not title_element:
            print(f"\nWarning: Could not find title in {link}")
            continue

        title = title_element.text

        # Convert to markdown
        markdown_content = markdownify(str(content_div))

        # Save to file
        filename = f"{OUTPUT_DIR}/{format_title_for_filename(title)}.md"
        with open(filename, "w", encoding="utf-8") as file:
            file.write(markdown_content)

    print(f"\n✓ Successfully crawled {len(links)} docs to {OUTPUT_DIR}")


if __name__ == "__main__":
    crawl_docs()