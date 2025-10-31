from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from markdownify import markdownify
import os
import time

from src.utils import format_title_for_filename

output_dir = "../docs/markdown/"
def main():
    os.makedirs(output_dir, exist_ok=True)
    # Setup Selenium Chrome Driver
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run Chrome in headless mode (no GUI)
    chrome_options.add_argument("--disable-gpu")  # Disable GPU (useful for headless mode)
    chrome_options.add_argument("--no-sandbox")  # Bypass OS security model
    chrome_options.add_argument("--disable-dev-shm-usage")  # Overcome limited resource problems

    url = "https://www.tradingview.com/pine-script-reference/v6/"
    # Install ChromeDriver and start Selenium WebDriver
    driver = webdriver.Chrome(options=chrome_options)

    driver.get(url)
    time.sleep(2)  # Give time for JavaScript to load content

    # Parse the HTML page source
    soup = BeautifulSoup(driver.page_source, "html.parser")
    # select div with class 'tv-script-reference__right-column js-main-header'
    content_div = soup.select_one('div[class^="tv-script-reference__right-column"]')

    if not content_div:
        raise Exception(f"Could not find the main content div in {url}")

    markdown_content = markdownify(str(content_div))

    # select text from <h1 class="tv-script-reference__main-header">Pine Script® language reference manual</h1>
    title = soup.select_one('h1[class^="tv-script-reference__main-header"]').text

    # Save the Markdown Content to a File
    with open(f"{output_dir}/{format_title_for_filename(title)}.md", "w", encoding="utf-8") as file:
        file.write(markdown_content)

if __name__ == "__main__":
    main()