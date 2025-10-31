"""
Split the Pine Script Language Reference Manual into individual markdown files
organized by category (Variables, Functions, Constants, etc.).
"""

import os
import re

INPUT_FILE = "docs/markdown/pine_script_language_reference_manual.md"
OUTPUT_DIR = "docs/markdown/reference"


def format_title_for_filename(title: str) -> str:
    """Convert title to a safe filename."""
    # Convert to lowercase
    title = title.lower().strip()

    # Replace spaces with underscores
    title = title.replace(" ", "_")

    # Remove special characters (keep only alphanumeric, underscores, hyphens, and dots)
    title = re.sub(r'[^a-z0-9._-]', '', title)

    # Limit filename length to 255 characters (safe for most filesystems)
    return title[:255]


def parse_markdown_file(file_path):
    """
    Parse the markdown file and extract sections and items.

    Returns:
        dict: A dictionary where keys are section names (e.g., 'Variables', 'Functions')
              and values are lists of tuples (item_name, item_content)
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    sections = {}
    current_section = None
    current_item_name = None
    current_item_lines = []

    i = 0
    while i < len(lines):
        line = lines[i]

        # Check if this is a section header (followed by dashes)
        if i + 1 < len(lines) and re.match(r'^-+\s*$', lines[i + 1]):
            # Save previous item if exists
            if current_section and current_item_name:
                item_content = ''.join(current_item_lines).strip()
                if current_section not in sections:
                    sections[current_section] = []
                sections[current_section].append((current_item_name, item_content))

            # Start new section
            current_section = line.strip()
            current_item_name = None
            current_item_lines = []
            i += 2  # Skip the section name and dashes
            continue

        # Check if this is an item header (### heading)
        if line.startswith('### '):
            # Save previous item if exists
            if current_section and current_item_name:
                item_content = ''.join(current_item_lines).strip()
                if current_section not in sections:
                    sections[current_section] = []
                sections[current_section].append((current_item_name, item_content))

            # Start new item
            current_item_name = line[4:].strip()  # Remove "### " prefix
            current_item_lines = [line]  # Include the heading in the content
            i += 1
            continue

        # Accumulate lines for current item
        if current_item_name:
            current_item_lines.append(line)

        i += 1

    # Save the last item
    if current_section and current_item_name:
        item_content = ''.join(current_item_lines).strip()
        if current_section not in sections:
            sections[current_section] = []
        sections[current_section].append((current_item_name, item_content))

    return sections


def save_items_to_files(sections, output_dir):
    """
    Save each item to its own markdown file organized by category.

    Args:
        sections: Dictionary of sections and their items
        output_dir: Base directory for output files
    """
    # Create output directory
    os.makedirs(output_dir, exist_ok=True)

    stats = {}

    for section_name, items in sections.items():
        # Create folder for this section
        section_folder = os.path.join(output_dir, format_title_for_filename(section_name))
        os.makedirs(section_folder, exist_ok=True)

        stats[section_name] = len(items)

        for item_name, item_content in items:
            # Create filename from item name
            filename = format_title_for_filename(item_name) + '.md'
            file_path = os.path.join(section_folder, filename)

            # Write content to file
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(item_content + '\n')

            print(f"Created: {file_path}")

    return stats


def main():
    print(f"Reading from: {INPUT_FILE}")
    print(f"Output directory: {OUTPUT_DIR}")
    print()

    # Parse the markdown file
    print("Parsing markdown file...")
    sections = parse_markdown_file(INPUT_FILE)

    print(f"Found {len(sections)} sections:")
    for section_name in sections.keys():
        print(f"  - {section_name}: {len(sections[section_name])} items")
    print()

    # Save items to individual files
    print("Creating individual markdown files...")
    stats = save_items_to_files(sections, OUTPUT_DIR)

    print()
    print("Summary:")
    print("=" * 50)
    total_items = 0
    for section_name, count in stats.items():
        print(f"{section_name}: {count} files")
        total_items += count
    print("=" * 50)
    print(f"Total: {total_items} files created")
    print(f"\nAll files saved to: {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
