# PineScript Documentation Crawler

A simple Python tool to crawl and convert PineScript documentation from TradingView to offline Markdown files.

## Features

- Crawls 4 types of PineScript documentation:
  - **Pine Script Docs**: Main documentation (https://www.tradingview.com/pine-script-docs/)
  - **Pine Script Reference**: Language reference manual (https://www.tradingview.com/pine-script-reference/v6/)
  - **Built-in Indicators**: Documentation for built-in indicators (https://www.tradingview.com/support/folders/43000587405-built-in-indicators/)
  - **Built-in Strategies**: Documentation for built-in strategies (https://www.tradingview.com/support/folders/43000587406-built-in-strategies/)
- Clean, maintainable code structure
- Run individual crawlers or all at once
- Progress bars for tracking crawl progress
- Converts HTML to clean Markdown format

## Installation

1. Clone the repository
2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Install ChromeDriver for Selenium (required for some crawlers)

## Usage

### Option 1: Run from root directory (recommended)

Run all crawlers:
```bash
python crawl.py all
```

Run individual crawlers:
```bash
python crawl.py docs           # Pine Script documentation
python crawl.py reference      # Pine Script reference manual
python crawl.py indicators     # Built-in indicators
python crawl.py strategies     # Built-in strategies
```

Run multiple crawlers:
```bash
python crawl.py docs reference
python crawl.py indicators strategies
```

### Option 2: Run from src directory

All crawlers:
```bash
cd src
python main.py all
```

Individual crawlers:
```bash
cd src
python main.py docs reference
```

### Run Individual Crawler Scripts Directly

You can also run each crawler independently from within the src directory:

```bash
cd src
python crawl_pine_script_docs.py
python crawl_pine_script_reference.py
python crawl_indicators_docs.py
python crawl_strategies_docs.py
```

## Output

Markdown files are saved to:
- `../docs/markdown/pine-script-docs/` - Pine Script documentation
- `../docs/markdown/` - Pine Script reference manual
- `../docs/markdown/built-in-indicators/` - Built-in indicators
- `../docs/markdown/built-in-strategies/` - Built-in strategies

## Project Structure

```
pinescript-docs/
├── src/
│   ├── main.py                      # Main CLI entry point
│   ├── crawl_pine_script_docs.py    # Crawls main docs
│   ├── crawl_pine_script_reference.py  # Crawls reference manual
│   ├── crawl_indicators_docs.py     # Crawls built-in indicators
│   ├── crawl_strategies_docs.py     # Crawls built-in strategies
│   └── utils.py                     # Shared utility functions
└── docs/
    └── markdown/                    # Output directory
```

## Development

The code is designed to be simple and maintainable:

- **utils.py**: Contains shared functions for all crawlers
  - `create_selenium_driver()`: Creates configured Chrome driver
  - `get_doc_links()`: Extracts documentation links
  - `clean_html_content()`: Cleans HTML before conversion
  - `format_title_for_filename()`: Sanitizes titles for filenames

- Each crawler is a simple function that can be run independently
- Main script provides a unified CLI interface

## Notes

- Some crawlers use Selenium (indicators, strategies, reference) for JavaScript-rendered pages
- Others use simple requests (docs) for static content
- All output is converted to clean Markdown format
- Images are removed, links are converted to plain text