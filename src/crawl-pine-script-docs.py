import os

import requests
from bs4 import BeautifulSoup
from markdownify import markdownify
from tqdm import tqdm
from src.utils import get_doc_links, save_webpage, format_title_for_filename

BASE_URL = "https://www.tradingview.com/pine-script-docs/"
OUTPUT_FOLDER = "../docs/markdown/pine-script-docs"

def main():
    os.makedirs(OUTPUT_FOLDER, exist_ok=True)

    print(f"Processing {BASE_URL}...")
    links = get_doc_links(BASE_URL)
    print(f"Found {len(links)} links in {BASE_URL}")

    pbar = tqdm(links)
    for link in pbar:
        pbar.set_description(f"Processing {link}")
        response = requests.get(link)
        if response.status_code != 200:
            raise ValueError(f"Failed to retrieve {link}")

        # Parse HTML
        soup = BeautifulSoup(response.text, "html.parser")
        # get div with id slot-container
        content_div = soup.select_one('div[id="slot-container"]')
        # get first h1 text
        title = soup.select_one('h1').text

        markdown_content = markdownify(str(content_div))

        with open(f"{OUTPUT_FOLDER}/{format_title_for_filename(title)}.md", "w", encoding="utf-8") as file:
            file.write(markdown_content)

if __name__ == "__main__":
    main()