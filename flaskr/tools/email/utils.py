from csv import reader


def extract_csv(file_path: str) -> tuple[list[str], list[dict[str, str]]]:
    """Extract a CSV into rows of dictionary"""
    with open(file_path, "r") as csv_file:
        csv_reader = reader(csv_file)
        header = None
        data = []
        for row in csv_reader:
            if header is None:
                header = row
                continue
            data.append(dict(zip(header, row)))
    return header, data
