"""
CSV to JSON Converter Tool - Cleaned Version

Converts product CSV files to JSON format for the BEIJ e-commerce platform.
This is a demonstration of how the legacy converter.py could be refactored.
"""

import json
import csv
from pathlib import Path
from typing import List, Dict, Any
import argparse
import logging

# Configuration constants
DEFAULT_INPUT_FILE = "test.csv"
DEFAULT_OUTPUT_FILE = "target.json"
ENCODING = "Latin1"
CURRENCY_PREFIX_LENGTH = 3  # Remove first 3 chars (e.g., "₹1,234" -> "1,234")

# Field indices in CSV
CATEGORY_INDEX = 2
DISCOUNTED_PRICE_INDEX = 3
ACTUAL_PRICE_INDEX = 4
RATING_INDEX = 6
RATING_COUNT_INDEX = 7
REVIEW_START_INDEX = 9
REVIEW_FIELD_COUNT = 4

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def clean_text_field(text: str) -> str:
    """Clean text field by replacing problematic characters."""
    return text.replace('"', "'").replace("\\", "\\\\")


def parse_price(price_str: str) -> float:
    """Parse price string by removing currency symbol and commas."""
    try:
        cleaned = price_str[CURRENCY_PREFIX_LENGTH:].replace(",", "")
        return float(cleaned)
    except (ValueError, IndexError) as e:
        logger.warning(f"Failed to parse price '{price_str}': {e}")
        return 0.0


def parse_rating(rating_str: str) -> float:
    """Parse rating string, handling commas and empty values."""
    try:
        cleaned = rating_str.replace(",", "")
        return float(cleaned) if cleaned else 0.0
    except ValueError as e:
        logger.warning(f"Failed to parse rating '{rating_str}': {e}")
        return 0.0


def parse_rating_count(count_str: str) -> int:
    """Parse rating count string, handling commas and empty values."""
    try:
        cleaned = count_str.replace(",", "")
        return int(cleaned) if cleaned else 0
    except ValueError as e:
        logger.warning(f"Failed to parse rating count '{count_str}': {e}")
        return 0


def process_csv_row(row: List[str], headers: List[str]) -> Dict[str, Any]:
    """Process a single CSV row into a structured dictionary."""
    # Clean text fields
    for i in range(len(row)):
        row[i] = clean_text_field(row[i])
    
    # Parse category list
    row[CATEGORY_INDEX] = row[CATEGORY_INDEX].split("|")
    
    # Parse price fields
    row[DISCOUNTED_PRICE_INDEX] = parse_price(row[DISCOUNTED_PRICE_INDEX])
    row[ACTUAL_PRICE_INDEX] = parse_price(row[ACTUAL_PRICE_INDEX])
    
    # Parse rating fields
    row[RATING_INDEX] = parse_rating(row[RATING_INDEX])
    row[RATING_COUNT_INDEX] = parse_rating_count(row[RATING_COUNT_INDEX])
    
    # Parse review fields (convert to lists)
    for i in range(REVIEW_FIELD_COUNT):
        review_index = REVIEW_START_INDEX + i
        if review_index < len(row):
            row[review_index] = row[review_index].split(",")
    
    return dict(zip(headers, row))


def convert_csv_to_json(input_file: str, output_file: str, limit: int = None) -> None:
    """Convert CSV file to JSON format."""
    input_path = Path(input_file)
    output_path = Path(output_file)
    
    if not input_path.exists():
        raise FileNotFoundError(f"Input file not found: {input_file}")
    
    logger.info(f"Converting {input_file} to {output_file}")
    
    items = []
    headers = []
    
    try:
        with input_path.open(newline='', encoding=ENCODING) as csvfile:
            reader = csv.reader(csvfile)
            
            for row_num, row in enumerate(reader):
                if row_num == 0:
                    headers = row
                    logger.info(f"Found {len(headers)} columns")
                else:
                    try:
                        processed_row = process_csv_row(row, headers)
                        items.append(processed_row)
                        
                        # Optional limit for testing
                        if limit and len(items) >= limit:
                            logger.info(f"Reached limit of {limit} items")
                            break
                            
                    except Exception as e:
                        logger.error(f"Error processing row {row_num}: {e}")
                        continue
        
        # Write JSON output
        with output_path.open('w', encoding=ENCODING) as jsonfile:
            json.dump(items, jsonfile, ensure_ascii=False, indent=2)
        
        logger.info(f"Successfully converted {len(items)} items to {output_file}")
        
    except Exception as e:
        logger.error(f"Conversion failed: {e}")
        raise


def main():
    """Main function with command line argument support."""
    parser = argparse.ArgumentParser(description="Convert CSV to JSON for BEIJ platform")
    parser.add_argument("--input", "-i", default=DEFAULT_INPUT_FILE, 
                       help=f"Input CSV file (default: {DEFAULT_INPUT_FILE})")
    parser.add_argument("--output", "-o", default=DEFAULT_OUTPUT_FILE,
                       help=f"Output JSON file (default: {DEFAULT_OUTPUT_FILE})")
    parser.add_argument("--limit", "-l", type=int,
                       help="Limit number of items for testing")
    parser.add_argument("--verbose", "-v", action="store_true",
                       help="Enable verbose logging")
    
    args = parser.parse_args()
    
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    try:
        convert_csv_to_json(args.input, args.output, args.limit)
        print(f"✅ Conversion completed: {args.input} → {args.output}")
    except Exception as e:
        print(f"❌ Conversion failed: {e}")
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main())

