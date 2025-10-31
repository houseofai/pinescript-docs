#!/usr/bin/env python3
"""
PineScript Documentation Crawler
Main entry point to run all or individual crawlers.
"""

import argparse
import sys

from crawl_indicators_docs import crawl_indicators
from crawl_strategies_docs import crawl_strategies
from crawl_pine_script_reference import crawl_reference
from crawl_pine_script_docs import crawl_docs


CRAWLERS = {
    'indicators': {
        'function': crawl_indicators,
        'description': 'Crawl built-in indicators documentation'
    },
    'strategies': {
        'function': crawl_strategies,
        'description': 'Crawl built-in strategies documentation'
    },
    'reference': {
        'function': crawl_reference,
        'description': 'Crawl Pine Script reference manual'
    },
    'docs': {
        'function': crawl_docs,
        'description': 'Crawl Pine Script documentation'
    }
}


def run_crawler(crawler_name):
    """Run a specific crawler by name."""
    if crawler_name not in CRAWLERS:
        print(f"Error: Unknown crawler '{crawler_name}'")
        print(f"Available crawlers: {', '.join(CRAWLERS.keys())}")
        return False

    print(f"\n{'=' * 60}")
    print(f"Running {crawler_name} crawler...")
    print(f"{'=' * 60}\n")

    try:
        CRAWLERS[crawler_name]['function']()
        return True
    except Exception as e:
        print(f"\nError running {crawler_name} crawler: {e}")
        return False


def run_all_crawlers():
    """Run all crawlers sequentially."""
    print("\n" + "=" * 60)
    print("Running ALL crawlers")
    print("=" * 60)

    results = {}
    for name in CRAWLERS.keys():
        success = run_crawler(name)
        results[name] = success

    # Print summary
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    for name, success in results.items():
        status = "✓ Success" if success else "✗ Failed"
        print(f"{name:20s}: {status}")

    all_success = all(results.values())
    return all_success


def main():
    """Main entry point with CLI argument parsing."""
    parser = argparse.ArgumentParser(
        description='PineScript Documentation Crawler',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Available crawlers:
  indicators    - Crawl built-in indicators documentation
  strategies    - Crawl built-in strategies documentation
  reference     - Crawl Pine Script reference manual
  docs          - Crawl Pine Script documentation
  all           - Run all crawlers

Examples:
  python main.py all              # Run all crawlers
  python main.py indicators       # Run only indicators crawler
  python main.py docs reference   # Run docs and reference crawlers
        """
    )

    parser.add_argument(
        'crawlers',
        nargs='+',
        choices=list(CRAWLERS.keys()) + ['all'],
        help='Crawler(s) to run'
    )

    args = parser.parse_args()

    # Run the requested crawlers
    if 'all' in args.crawlers:
        success = run_all_crawlers()
    else:
        results = []
        for crawler in args.crawlers:
            success = run_crawler(crawler)
            results.append(success)
        success = all(results)

    # Exit with appropriate code
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
