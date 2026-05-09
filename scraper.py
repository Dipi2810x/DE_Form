#!/usr/bin/env python3
"""
Scraper script to fetch form data from SheetDB API and save to docs/data directory.
"""
import json
import os
from datetime import datetime, timezone
from urllib.request import urlopen
from urllib.error import URLError, HTTPError


def fetch_data(api_url):
    """Fetch data from SheetDB API."""
    try:
        with urlopen(api_url, timeout=30) as response:
            data = json.loads(response.read().decode('utf-8'))
            return data
    except HTTPError as e:
        print(f"HTTP Error: {e.code} - {e.reason}")
        raise
    except URLError as e:
        print(f"URL Error: {e.reason}")
        raise
    except Exception as e:
        print(f"Error fetching data: {e}")
        raise


def save_data(data, output_dir):
    """Save data to JSON files in the output directory."""
    os.makedirs(output_dir, exist_ok=True)
    
    # Save all data
    all_data_path = os.path.join(output_dir, 'all_submissions.json')
    with open(all_data_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"Saved {len(data)} submissions to {all_data_path}")
    
    # Save metadata
    metadata = {
        'last_updated': datetime.now(timezone.utc).isoformat(),
        'total_submissions': len(data)
    }
    metadata_path = os.path.join(output_dir, 'metadata.json')
    with open(metadata_path, 'w', encoding='utf-8') as f:
        json.dump(metadata, f, indent=2)
    print(f"Saved metadata to {metadata_path}")
    
    # Group by project type
    by_type = {}
    for submission in data:
        project_type = submission.get('project_type', 'Unknown')
        if project_type not in by_type:
            by_type[project_type] = []
        by_type[project_type].append(submission)
    
    # Save each project type separately
    for project_type, submissions in by_type.items():
        # Create safe filename
        safe_type = project_type.replace('/', '_').replace(' ', '_').lower()
        type_path = os.path.join(output_dir, f'{safe_type}.json')
        with open(type_path, 'w', encoding='utf-8') as f:
            json.dump(submissions, f, indent=2, ensure_ascii=False)
        print(f"Saved {len(submissions)} {project_type} submissions to {type_path}")


def main():
    """Main function to run the scraper."""
    api_url = 'https://sheetdb.io/api/v1/rn4vpf7g0o20e'
    output_dir = 'docs/data'
    
    print(f"Fetching data from {api_url}...")
    try:
        data = fetch_data(api_url)
    except Exception as e:
        print(f"Error fetching data: {e}")
        print("Using empty data set")
        data = []
    
    print(f"Saving data to {output_dir}...")
    save_data(data, output_dir)
    
    print("Scraper completed successfully!")


if __name__ == '__main__':
    main()
