import os
import re
from urllib.parse import urljoin, urlparse

import requests
from bs4 import BeautifulSoup


def format_title_for_filename(title: str) -> str:
    # Convert to lowercase
    title = title.lower().strip()

    # Replace spaces with underscores
    title = title.replace(" ", "_")

    # Remove special characters (keep only alphanumeric, underscores, hyphens, and dots)
    title = re.sub(r'[^a-z0-9._-]', '', title)

    # Limit filename length to 255 characters (safe for most filesystems)
    return title[:255]

def get_doc_links(url):
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Failed to retrieve {url}")
        raise ValueError("Failed to retrieve the Pine Script documentation.")

    soup = BeautifulSoup(response.text, 'html.parser')
    links = list()

    for a_tag in soup.find_all("a", href=True):
        href = a_tag["href"]
        full_url = urljoin(url, href)

        links.append(full_url)

    # drop BASE URL from links
    links = [link for link in links if link != url]

    links = remove_duplicates(links)
    links = remove_slash_ending_urls(links)
    links = remove_external_links(links, base_domain=url)
    return links

def remove_external_links(links, base_domain="www.tradingview.com"):
    filtered_links = []
    for link in links:
        # check if link starts with base_domain
        if base_domain in link:
            filtered_links.append(link)
    return filtered_links

def remove_duplicates(lst):
    seen = set()
    result = []
    for item in lst:
        if item not in seen:
            seen.add(item)
            result.append(item)
    return result

def remove_slash_ending_urls(links):
    for link in links:
        # Drop if ends with /
        if link.endswith("/"):
            links.remove(link)
            continue
    return links

def save_webpage(url, output_folder):
    """Downloads and saves an entire webpage (HTML only) locally."""
    response = requests.get(url)
    if response.status_code != 200:
        raise ValueError(f"Failed to retrieve {url}")

    # Parse HTML
    soup = BeautifulSoup(response.text, "html.parser")
    # python
    url_path = urlparse(url).path.strip("/")

    # create full folder hierarchy under output_folder/pine-script-docs
    #full_path = os.path.join(output_folder, os.path.dirname(url_path)) if os.path.dirname(url_path) else base_dir
    os.makedirs(output_folder, exist_ok=True)

    # determine filename (use 'index' if URL ends with a slash or has no basename)
    basename = os.path.basename(url_path)# or "index"
    filename = os.path.join(output_folder, f"{basename}.html")

    with open(filename, "w", encoding="utf-8") as file:
        file.write(soup.prettify())