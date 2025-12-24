from schema import COLUMNS

def print_header():
    print("Copy and paste these columns into your Google Sheet (Row 1):")
    print(",".join(COLUMNS))

if __name__ == "__main__":
    print_header()
