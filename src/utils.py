import os
import re
from urllib.parse import urljoin, urlparse

import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


def format_title_for_filename(title: str) -> str:
    """Convert title to a safe filename."""
    title = title.lower().strip()
    title = title.replace(" ", "_")
    title = re.sub(r'[^a-z0-9._-]', '', title)
    return title[:255]  # Limit to 255 characters for filesystem compatibility


def create_selenium_driver():
    """Create and configure a Selenium Chrome driver in headless mode."""
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    return webdriver.Chrome(options=chrome_options)


def clean_html_content(content_div):
    """Remove links, images, and format code tags for markdown conversion."""
    # Remove links (keep text only)
    for a_tag in content_div.find_all("a", href=True):
        text = a_tag.get_text(" ", strip=True)
        a_tag.replace_with(text)

    # Remove images
    for img_tag in content_div.find_all("img"):
        img_tag.decompose()

    # Convert code tags to markdown format
    for code_tag in content_div.find_all("code"):
        code_text = code_tag.get_text()
        code_tag.replace_with(f"`{code_text}`")

    return content_div


def get_doc_links(url):
    """Extract all documentation links from a given URL."""
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Failed to retrieve {url}")
        raise ValueError("Failed to retrieve the Pine Script documentation.")

    soup = BeautifulSoup(response.text, 'html.parser')
    links = []

    for a_tag in soup.find_all("a", href=True):
        href = a_tag["href"]
        full_url = urljoin(url, href)
        links.append(full_url)

    # Remove base URL from links
    links = [link for link in links if link != url]

    links = remove_duplicates(links)
    links = remove_slash_ending_urls(links)
    links = remove_external_links(links, base_domain=url)
    return links


def remove_external_links(links, base_domain="www.tradingview.com"):
    """Filter links to keep only those from the base domain."""
    return [link for link in links if base_domain in link]


def remove_duplicates(lst):
    """Remove duplicate items while preserving order."""
    seen = set()
    result = []
    for item in lst:
        if item not in seen:
            seen.add(item)
            result.append(item)
    return result


def remove_slash_ending_urls(links):
    """Remove URLs that end with a slash."""
    return [link for link in links if not link.endswith("/")]


def save_webpage(url, output_folder):
    """Download and save an entire webpage (HTML only) locally."""
    response = requests.get(url)
    if response.status_code != 200:
        raise ValueError(f"Failed to retrieve {url}")

    soup = BeautifulSoup(response.text, "html.parser")
    url_path = urlparse(url).path.strip("/")

    os.makedirs(output_folder, exist_ok=True)

    basename = os.path.basename(url_path)
    filename = os.path.join(output_folder, f"{basename}.html")

    with open(filename, "w", encoding="utf-8") as file:
        file.write(soup.prettify())