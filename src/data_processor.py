from .utils import clean_jira_description, format_to_iso8601, extract_attachment_urls

# Constants
JIRA_BASE_URL = "https://microtec.atlassian.net/browse/"

PRIORITY_MAPPING = {
    "Lowest": "4",
    "Low": "4",
    "Medium": "3",
    "High": "2",
    "Highest": "1"
}

def process_all_fields(all_fields_data):
    processed_data = {}
    for row in all_fields_data:
        issue_key = row.get("Issue key")
        if not issue_key:
            continue

        attachment_urls = extract_attachment_urls(row.get("Attachment", ""))
        processed_data[issue_key] = {
            "Description": clean_jira_description(row.get("Description", "")),
            "Environment": row.get("Environment", "Not Provided"),
            "Attachments": "\n".join(attachment_urls) if attachment_urls else "No Attachments"
        }
    return processed_data

def process_default_fields(default_fields_data, all_fields_data):
    results = []
    for row in default_fields_data:
        issue_key = row.get("Issue key")
        if not issue_key:
            continue

        all_field_entry = all_fields_data.get(issue_key, {})

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
            "Priority": PRIORITY_MAPPING.get(row.get("Priority", "Medium"), "2"),
            "State": row.get("Status", ""),
            "Created Date": format_to_iso8601(row.get("Created", "")),
            "Changed Date": format_to_iso8601(row.get("Updated", "")),
            "Description": refined_description
        })
    return results