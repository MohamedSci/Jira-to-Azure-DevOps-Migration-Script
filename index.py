from src.logger import setup_logger
from src.migration import migrate

def main():
    setup_logger()
    migrate(
        default_fields_file="input/default_fields.csv",
        all_fields_file="input/all_fields.csv",
        output_file="output/azure_output.csv"
    )

if __name__ == "__main__":
    main()