import csv
import re

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

# Input and output file paths
input_file = "to_migrate.csv"
output_file = "formatted_to_migrate.csv"

# Read the input CSV, clean the Description column, and write to the output CSV
with open(input_file, mode="r", encoding="utf-8") as infile, open(output_file, mode="w", encoding="utf-8", newline="") as outfile:
    reader = csv.DictReader(infile)
    fieldnames = reader.fieldnames  # Preserve the original column headers

    writer = csv.DictWriter(outfile, fieldnames=fieldnames)
    writer.writeheader()

    for row in reader:
        # Clean the Description column
        row["Description"] = clean_jira_description(row.get("Description", ""))
        writer.writerow(row)

print(f"✅ Cleaned CSV saved as: {output_file}")