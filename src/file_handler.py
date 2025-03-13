import csv
import chardet

def detect_encoding(file_path):
    with open(file_path, "rb") as file:
        raw_data = file.read()
        result = chardet.detect(raw_data)
        return result["encoding"]

def read_csv(file_path):
    encoding = detect_encoding(file_path)
    with open(file_path, mode="r", encoding=encoding) as file:
        return list(csv.DictReader(file))

def write_csv(file_path, fieldnames, data):
    with open(file_path, mode="w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)