import requests
import json
import re
from datetime import datetime, timedelta
import argparse
import getpass
import sys

WP_URL = "https://your-domain.com"       # The URL of your WordPress site
WP_USERNAME = "your_wp_username"         # Your WordPress username
POST_SPLIT_REGEX = r'(?=^day \d+:)'      # Regex to detect the start of a new post
POST_TIME_STR = "22:00"                  # The fixed time in "HH:MM" (24-hour) format

def cleanup_text(text_block):
    """
    Cleans a block of text from common whitespace errors.
    - Removes leading/trailing whitespace from each line.
    - Reduces multiple spaces within a line to a single space.
    - Joins the cleaned lines with a newline character.
    """
    if not text_block:
        return ""
    
    lines = text_block.splitlines()
    cleaned_lines = []
    
    for line in lines:
        line_no_multi_space = re.sub(r' +', ' ', line)
        stripped_line = line_no_multi_space.strip()
        cleaned_lines.append(stripped_line)
        
    return "\n".join(cleaned_lines)


def get_or_create_category_path(api_url, auth, category_path_str):
    """
    Ensures a category hierarchy exists and returns the ID of the final category.
    Checks each level of the hierarchy and creates categories if they don't exist.
    """
    path_parts = [part.strip() for part in category_path_str.split('>')]
    parent_id = 0  # Start at the top level

    for name in path_parts:
        if not name: continue
        print(f"Checking category '{name}' (under parent ID: {parent_id})...")
        
        params = {'search': name, 'parent': parent_id}
        try:
            response = requests.get(f"{api_url}/categories", params=params, auth=auth)
            response.raise_for_status()
            found_category = next((cat for cat in response.json() if cat['name'] == name), None)

            if found_category:
                parent_id = found_category['id']
                print(f"-> Found. ID is {parent_id}.")
            else:
                print(f"-> Not found. Creating category '{name}'...")
                create_data = {'name': name, 'parent': parent_id}
                response = requests.post(f"{api_url}/categories", json=create_data, auth=auth)
                response.raise_for_status()
                parent_id = response.json()['id']
                print(f"-> Successfully created. New ID is {parent_id}.")

        except requests.exceptions.RequestException as e:
            print(f"ERROR processing category '{name}': {e}", file=sys.stderr)
            if e.response: print(f"Server response: {e.response.text}", file=sys.stderr)
            return None
    
    return parent_id

def create_post(api_url, auth, title, content, date, category_id):
    """Creates a post via the REST API."""
    post_data = {'title': title, 'content': content, 'status': 'draft', 'date': date.isoformat(), 'categories': [category_id]}
    try:
        response = requests.post(f"{api_url}/posts", json=post_data, auth=auth)
        response.raise_for_status()
        print(f"Post successfully created: '{title}' (Date: {date.strftime('%Y-%m-%d %H:%M')})")
    except requests.exceptions.RequestException as e:
        print(f"ERROR creating post '{title}': {e}", file=sys.stderr)
        if e.response: print(f"Server response: {e.response.text}", file=sys.stderr)

def main():
    """Main function to parse arguments and execute the logic."""
    parser = argparse.ArgumentParser(
        description="Creates WordPress posts from a text file and sets up the category hierarchy if needed.",
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument('--category-path', required=True, help='Category hierarchy, separated by ">".\nExample: "Destinations > Norway > Norway 2025"')
    parser.add_argument('--file', required=True, help="Path to the input text file")
    parser.add_argument('--start-date', required=True, help="Start date for the first post (Format: YYYY-MM-DD)")
    args = parser.parse_args()

    try:
        hour_str, minute_str = POST_TIME_STR.split(':')
        post_hour, post_minute = int(hour_str), int(minute_str)
    except (ValueError, IndexError):
        print(f"ERROR: Invalid time format in POST_TIME_STR constant. Please use 'HH:MM'.", file=sys.stderr)
        return

    try:
        wp_app_password = getpass.getpass(f"Please enter the application password for user '{WP_USERNAME}': ")
    except Exception:
        print("\nCould not read password. Aborting.", file=sys.stderr)
        return

    if not wp_app_password:
        print("\nNo password entered. Aborting.", file=sys.stderr)
        return

    auth = (WP_USERNAME, wp_app_password)
    api_url = f"{WP_URL.rstrip('/')}/wp-json/wp/v2"

    final_category_id = get_or_create_category_path(api_url, auth, args.category_path)
    if not final_category_id:
        print("\nAborting because the category hierarchy could not be created.", file=sys.stderr)
        return

    print("-" * 30)

    try:
        with open(args.file, 'r', encoding='utf-8') as f:
            full_text = f.read()
    except FileNotFoundError:
        print(f"ERROR: File '{args.file}' not found.", file=sys.stderr)
        return

    posts_raw = re.split(POST_SPLIT_REGEX, full_text, flags=re.MULTILINE)
    
    try:
        start_date = datetime.strptime(args.start_date, "%Y-%m-%d")
    except ValueError:
        print(f"ERROR: Invalid date format for --start-date. Please use YYYY-MM-DD.", file=sys.stderr)
        return

    category_for_title = args.category_path.split('>')[-1].strip()
    day_counter = 0

    for post_raw in posts_raw:
        if not post_raw.strip(): continue

        lines = post_raw.split('\n', 1)
        title_line = cleanup_text(lines[0])
        content = cleanup_text(lines[1]) if len(lines) > 1 else ""
        
        full_title = f"{category_for_title} {title_line}"
        
        post_date_base = start_date + timedelta(days=day_counter)
        post_date = post_date_base.replace(hour=post_hour, minute=post_minute, second=0)
        
        create_post(api_url, auth, full_title, content, post_date, final_category_id)
        day_counter += 1

    print("\nDone! All posts have been processed.")

if __name__ == "__main__":
    main()