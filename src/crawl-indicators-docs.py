from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from markdownify import markdownify
from tqdm import tqdm
import os
import time
import re

from src.utils import get_doc_links

# Setup Selenium Chrome Driver
chrome_options = Options()
chrome_options.add_argument("--headless")  # Run Chrome in headless mode (no GUI)
chrome_options.add_argument("--disable-gpu")  # Disable GPU (useful for headless mode)
chrome_options.add_argument("--no-sandbox")  # Bypass OS security model
chrome_options.add_argument("--disable-dev-shm-usage")  # Overcome limited resource problems

# Install ChromeDriver and start Selenium WebDriver
driver = webdriver.Chrome(options=chrome_options)

def format_title_for_filename(title: str) -> str:
    # Convert to lowercase
    title = title.lower().strip()

    # Replace spaces with underscores
    title = title.replace(" ", "_")

    # Remove special characters (keep only alphanumeric, underscores, hyphens, and dots)
    title = re.sub(r'[^a-z0-9._-]', '', title)

    # Limit filename length to 255 characters (safe for most filesystems)
    return title[:255]

# Read URLs from file
URL = "https://www.tradingview.com/support/folders/43000587405-built-in-indicators/"
urls = get_doc_links(URL)
# remove urls not starting with https://www.tradingview.com/support/solutions/
urls = [url for url in urls if url.startswith("https://www.tradingview.com/support/solutions/")]
# print links for debugging
for url in urls:
    print(url)

# Create output directory if not exists
output_dir = "../docs/markdown/built-in-indicators"
os.makedirs(output_dir, exist_ok=True)

pbar = tqdm(urls, desc="Processing URLs")

for url in pbar:
    # Load the webpage using Selenium
    driver.get(url)
    time.sleep(2)  # Give time for JavaScript to load content

    # Parse the HTML page source
    soup = BeautifulSoup(driver.page_source, "html.parser")

    # Extract the main content area
    content_div = soup.select_one('div[itemprop="text"][class^="solution-"]')

    if not content_div:
        raise Exception(f"Could not find the main content div in {url}")

    # Remove External Links (Keep Internal TradingView Links)
    for a_tag in content_div.find_all("a", href=True):
        text = a_tag.get_text(" ", strip=True)  # Preserve spaces properly
        a_tag.replace_with(text)  # Replace the tag with plain text

    # Remove Images
    for img_tag in content_div.find_all("img"):
        img_tag.decompose()  # Completely remove image tags

    # Convert <code> Tags to Markdown inline format
    for code_tag in content_div.find_all("code"):
        code_text = code_tag.get_text()
        code_tag.replace_with(f"`{code_text}`")  # Convert inline code to Markdown

    #markdown_content = html_to_markdown(str(content_div))
    markdown_content = markdownify(str(content_div))
    title_element = soup.select_one('[class^="page-title"] > span:nth-child(1)')

    # Save the Markdown Content to a File
    with open(f"{output_dir}/{format_title_for_filename(title_element.text)}.md", "w", encoding="utf-8") as file:
        file.write(markdown_content)


driver.quit()
