import logging
import re
from datetime import datetime

def clean_jira_description(jira_text):
    if not jira_text:
        return "No description available."

    cleaned_text = re.sub(r"h[34]\.\s*\*", "**", jira_text)
    cleaned_text = re.sub(r"\*(.*?)\*", r"_\1_", cleaned_text)
    cleaned_text = re.sub(r"#", "-", cleaned_text)
    cleaned_text = re.sub(r"\n\s*\n", "\n", cleaned_text)
    return cleaned_text.strip()

def format_to_iso8601(date_string):
    if not date_string:
        return ""

    try:
        parsed_date = datetime.strptime(date_string, "%d/%b/%y %I:%M %p")
        return parsed_date.isoformat()
    except ValueError:
        logging.warning(f"Invalid date format: {date_string}")
        return ""

def extract_attachment_urls(attachment_cell):
    if not attachment_cell:
        return []

    url_regex = r"https://[^\s;]+"
    return re.findall(url_regex, attachment_cell)