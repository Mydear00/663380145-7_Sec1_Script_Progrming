import csv
import json
from .utils import ensure_directory_exists


def csv_to_json(data, output_path=None):
    converted_data = [
        {str(key): value for key, value in row.items()}
        for row in data
    ]

    if output_path:
        ensure_directory_exists(output_path)

        with open(output_path, "w", encoding="utf-8") as file:
            json.dump(
                converted_data,
                file,
                indent=4,
                ensure_ascii=False
            )

    return converted_data


def json_to_csv(data, output_path, fieldnames=None):
    if isinstance(data, dict):
        rows = [data]
    elif isinstance(data, list):
        rows = data
    else:
        raise TypeError("JSON data must be a dictionary or list")

    normalized = []

    for row in rows:
        if not isinstance(row, dict):
            row = {"value": row}

        normalized_row = {}

        for key, value in row.items():
            if isinstance(value, (dict, list)):
                normalized_row[key] = json.dumps(
                    value, ensure_ascii=False
                )
            else:
                normalized_row[key] = value

        normalized.append(normalized_row)

    if fieldnames is None:
        fieldnames = list(normalized[0].keys()) if normalized else []

    ensure_directory_exists(output_path)

    with open(
        output_path, "w", encoding="utf-8-sig", newline=""
    ) as file:
        if fieldnames:
            writer = csv.DictWriter(
                file, fieldnames=fieldnames, extrasaction="ignore"
            )
            writer.writeheader()
            writer.writerows(normalized)

    return output_path
