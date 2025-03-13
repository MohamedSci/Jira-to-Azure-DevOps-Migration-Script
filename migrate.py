import csv
import re
from datetime import datetime
import logging
import chardet

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# File paths
DEFAULT_FIELDS_FILE = "default_fields.csv"
ALL_FIELDS_FILE = "all_fields.csv"
OUTPUT_FILE = "azure_output.csv"

# Base URL for Jira issue links
JIRA_BASE_URL = "https://microtec.atlassian.net/browse/"

# Priority Mapping: Jira → Azure DevOps
PRIORITY_MAPPING = {
    "Lowest": "1",
    "Low": "1",
    "Medium": "2",
    "High": "3",
    "Highest": "4"
}

# Function to detect file encoding
def detect_encoding(file_path):
    with open(file_path, "rb") as file:
        raw_data = file.read()
        result = chardet.detect(raw_data)
        return result["encoding"]

# Function to clean Jira description formatting
def clean_jira_description(jira_text):
    if not jira_text:
        return "No description available."

    # Replace Jira formatting with Markdown
    cleaned_text = re.sub(r"h[34]\.\s*\*", "**", jira_text)  # Convert h3/h4. *Title:* → **Title:**
    cleaned_text = re.sub(r"\*(.*?)\*", r"_\1_", cleaned_text)  # Convert *bold* → _italic_
    cleaned_text = re.sub(r"#", "-", cleaned_text)  # Convert # Lists → - Lists
    cleaned_text = re.sub(r"\n\s*\n", "\n", cleaned_text)  # Remove extra blank lines
    return cleaned_text.strip()

# Function to format date to ISO 8601 for Azure DevOps
def format_to_iso8601(date_string):
    if not date_string:
        return ""

    try:
        parsed_date = datetime.strptime(date_string, "%d/%b/%y %I:%M %p")  # Example: 11/Mar/25 1:31 PM
        return parsed_date.isoformat()
    except ValueError:
        logging.warning(f"Invalid date format: {date_string}")
        return ""

# Function to extract attachment URLs
def extract_attachment_urls(attachment_cell):
    if not attachment_cell:
        return []

    # Match URLs starting with https:// and ending with a space or end of string
    url_regex = r"https://[^\s]+"
    return re.findall(url_regex, attachment_cell)

# Function to process all_fields.csv
def process_all_fields():
    all_fields_data = {}

    # Detect encoding for all_fields.csv
    encoding = detect_encoding(ALL_FIELDS_FILE)
    logging.info(f"Detected encoding for {ALL_FIELDS_FILE}: {encoding}")

    with open(ALL_FIELDS_FILE, mode="r", encoding=encoding) as file:
        reader = csv.DictReader(file)
        for row in reader:
            issue_key = row.get("Issue key")
            if not issue_key:
                logging.warning(f"Skipping row with missing Issue key: {row}")
                continue

            # Extract attachments
            attachment_urls = extract_attachment_urls(row.get("Attachment", ""))

            all_fields_data[issue_key] = {
                "Description": clean_jira_description(row.get("Description", "")),
                "Environment": row.get("Environment", "Not Provided"),
                "Attachments": "\n".join(attachment_urls) if attachment_urls else "No Attachments"
            }

    logging.info(f"Processed {len(all_fields_data)} rows from all_fields.csv")
    return all_fields_data

# Function to process default_fields.csv
def process_default_fields(all_fields_data):
    results = []

    # Detect encoding for default_fields.csv
    encoding = detect_encoding(DEFAULT_FIELDS_FILE)
    logging.info(f"Detected encoding for {DEFAULT_FIELDS_FILE}: {encoding}")

    with open(DEFAULT_FIELDS_FILE, mode="r", encoding=encoding) as file:
        reader = csv.DictReader(file)
        for row in reader:
            issue_key = row.get("Issue key")
            if not issue_key:
                logging.warning(f"Skipping row with missing Issue key: {row}")
                continue

            all_field_entry = all_fields_data.get(issue_key, {})

            # Construct refined description
            refined_description = "\n\n".join([
                f"### Description\n{all_field_entry.get('Description', 'No description available.')}",
                f"### Environment\n{all_field_entry.get('Environment', 'Not Provided')}",
                f"### Original Issue\n[View in Jira]({JIRA_BASE_URL}{issue_key})",
                f"### Attachments\n{all_field_entry.get('Attachments', 'No Attachments')}"
            ])

            results.append({
                "Work Item Type": "Bug",
                "Title": row.get("Summary", ""),
                "Assigned To": row.get("Assignee", ""),
                "Created By": row.get("Reporter", ""),
                "Priority": PRIORITY_MAPPING.get(row.get("Priority", "Medium"), "2"),  # Default to Medium
                "State": row.get("Status", ""),
                "Created Date": format_to_iso8601(row.get("Created", "")),
                "Changed Date": format_to_iso8601(row.get("Updated", "")),
                "Description": refined_description
            })

    logging.info(f"Processed {len(results)} rows from default_fields.csv")
    return results

# Function to write output CSV
def write_output(results):
    fieldnames = [
        "Work Item Type", "Title", "Assigned To", "Created By", "Priority",
        "State", "Created Date", "Changed Date", "Description"
    ]

    with open(OUTPUT_FILE, mode="w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(results)

    logging.info(f"✅ Final cleaned CSV saved as: {OUTPUT_FILE}")

# Main function
def main():
    try:
        # Step 1: Process all_fields.csv
        all_fields_data = process_all_fields()

        # Step 2: Process default_fields.csv
        results = process_default_fields(all_fields_data)

        # Step 3: Write output CSV
        write_output(results)
    except Exception as e:
        logging.error(f"❌ Error: {e}")

# Run the script
if __name__ == "__main__":
    main()