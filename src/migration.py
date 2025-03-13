from .file_handler import read_csv, write_csv
from .data_processor import process_all_fields, process_default_fields

def migrate(default_fields_file, all_fields_file, output_file):
    # Read input files
    default_fields_data = read_csv(default_fields_file)
    all_fields_data = read_csv(all_fields_file)

    # Process data
    processed_all_fields = process_all_fields(all_fields_data)
    results = process_default_fields(default_fields_data, processed_all_fields)

    # Write output file
    fieldnames = [
        "Work Item Type", "Title", "Assigned To", "Created By", "Priority",
        "State", "Created Date", "Changed Date", "Description"
    ]
    write_csv(output_file, fieldnames, results)