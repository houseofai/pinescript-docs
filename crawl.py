#!/usr/bin/env python3
"""
PineScript Documentation Crawler
Main entry point to run all or individual crawlers from root directory.
"""

import sys
import os

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from main import main

if __name__ == "__main__":
    main()
