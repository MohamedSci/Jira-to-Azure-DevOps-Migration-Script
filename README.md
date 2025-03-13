# Jira to Azure DevOps Migration Script 🚀

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![License](https://img.shields.io/badge/License-MIT-green)
![Status](https://img.shields.io/badge/Status-Production%20Ready-brightgreen)

A **robust and efficient Python script** to migrate issues from Jira to Azure DevOps, ensuring **data integrity**, **formatting consistency**, and **seamless integration**. This script automates the migration process, saving time and effort for teams transitioning between platforms.

---

## Table of Contents

1. [Features](#features)
2. [Installation](#installation)
3. [Usage](#usage)
4. [Output](#output)
5. [Contributing](#contributing)
6. [License](#license)
7. [Support](#support)

---

## Features ✨

### Data Enrichment & Cleansing
- **Formats Jira descriptions** to be more structured and readable.
- Converts Jira markdown syntax to a format compatible with Azure DevOps.
- Ensures all rows are processed without loss of information.

### Priority Mapping
- Translates Jira priorities (`Lowest`, `Low`, `Medium`, `High`, `Highest`) to Azure DevOps priority levels (`1`, `2`, `3`, `4`).

### Attachment Extraction & Processing
- Dynamically detects all attachment columns in the source CSV file.
- Extracts valid attachment URLs while filtering out timestamps, IDs, and filenames.
- Consolidates multiple attachments for each issue and embeds them into the refined description.

### Jira Issue Tracking Link
- Automatically embeds the original Jira issue link in the Azure DevOps description for reference.

### Date Formatting
- Converts Jira timestamps to ISO 8601 format, ensuring compatibility with Azure DevOps.

### Optimized for Large-Scale Migration
- Supports **300+ issues** while maintaining high performance.
- Utilizes efficient CSV parsing and streaming to prevent memory issues.

---

## Installation 🛠️

### Prerequisites
- Python 3.8 or higher.
- Required Python libraries: `chardet`, `csv`, `re`, `datetime`, `logging`.

### Steps
1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/jira-to-azure-devops-migration.git
   cd jira-to-azure-devops-migration
   ```

2. Install dependencies:
   ```bash
   pip install chardet
   ```

3. Place your input files (`default_fields.csv` and `all_fields.csv`) in the `new_convert-jira-to-devops` directory.

---

## Usage 🚀

1. Run the script:
   ```bash
   python migrate.py
   ```

2. Check the output file (`azure_output.csv`) in the `new_convert-jira-to-devops` directory.

### Example Input Files

#### `default_fields.csv`
| Issue key | Summary     | Assignee | Reporter | Priority | Status   | Created           | Updated           |
|-----------|-------------|----------|----------|----------|----------|-------------------|-------------------|
| PROJ-123  | Test issue  | John Doe | Jane Doe | High     | Open     | 11/Mar/25 1:31 PM | 11/Mar/25 1:31 PM |

#### `all_fields.csv`
| Issue key | Description          | Environment | Attachment                                                                 |
|-----------|----------------------|-------------|----------------------------------------------------------------------------|
| PROJ-123  | Test issue           | Production  | 11/Mar/25 1:31 PM;712020:ae3212cd-e1d6-4083-bc70-ddd6dfebfad6;cash receipt report.mp4;https://microtec.atlassian.net/rest/api/3/attachment/content/16380 |

---

## Output 📂

The script generates a cleaned and formatted CSV file (`azure_output.csv`) containing:

| Work Item Type | Title      | Assigned To | Created By | Priority | State | Created Date           | Changed Date           | Description                                                                                                                                                                                                 |
|----------------|------------|-------------|------------|----------|-------|------------------------|------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Bug            | Test issue | John Doe    | Jane Doe   | 3        | Open  | 2025-03-11T13:31:00    | 2025-03-11T13:31:00    | ### Description\nTest issue\n\n### Environment\nProduction\n\n### Original Issue\n[View in Jira](https://microtec.atlassian.net/browse/PROJ-123)\n\n### Attachments\nhttps://microtec.atlassian.net/rest/api/3/attachment/content/16380 |

---

## Contributing 🤝

We welcome contributions! Here’s how you can help:

1. Fork the repository.
2. Create a new branch:
   ```bash
   git checkout -b feature/your-feature-name
   ```
3. Commit your changes:
   ```bash
   git commit -m "Add your feature"
   ```
4. Push to the branch:
   ```bash
   git push origin feature/your-feature-name
   ```
5. Open a pull request.

---

## License 📜

This project is licensed under the **Apache 2.0 License**. See the [LICENSE](LICENSE.txt) file for details.

---

## Support 💬

For questions, issues, or feature requests, please:

- Open an issue on [GitHub](https://github.com/MohamedSci/Jira-to-Azure-DevOps-Migration-Script.git).
- Email us at [muhammedsaidsyed215@gmail.com](mailto:muhammedsaidsyed215@gmail.com).

---