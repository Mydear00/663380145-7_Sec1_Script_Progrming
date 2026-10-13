import csv
from .utils import ensure_directory_exists


def load_csv(file_path):
    with open(
        file_path, "r", encoding="utf-8-sig", newline=""
    ) as file:
        return list(csv.DictReader(file))


def aggregate_csv(
    data, group_by_field, aggregate_field, operation="sum"
):
    if not data:
        return []

    grouped = {}

    for row in data:
        group_value = row.get(group_by_field, "")
        raw_value = row.get(aggregate_field, 0)

        try:
            number = float(raw_value)
        except (TypeError, ValueError):
            raise ValueError(
                f"Field '{aggregate_field}' must be numeric: {raw_value!r}"
            )

        grouped.setdefault(group_value, []).append(number)

    results = []

    for group_value, values in grouped.items():
        if operation == "sum":
            result_value = sum(values)
            result_field = f"Total_{aggregate_field}"
        elif operation == "average":
            result_value = sum(values) / len(values)
            result_field = f"Average_{aggregate_field}"
        elif operation == "min":
            result_value = min(values)
            result_field = f"Min_{aggregate_field}"
        elif operation == "max":
            result_value = max(values)
            result_field = f"Max_{aggregate_field}"
        elif operation == "count":
            result_value = len(values)
            result_field = f"Count_{aggregate_field}"
        else:
            raise ValueError(
                f"Unsupported aggregation operation: {operation}"
            )

        results.append({
            group_by_field: group_value,
            result_field: round(result_value, 2)
        })

    return results


def save_csv(data, file_path, fieldnames=None):
    if fieldnames is None:
        fieldnames = list(data[0].keys()) if data else []

    ensure_directory_exists(file_path)

    with open(
        file_path, "w", encoding="utf-8-sig", newline=""
    ) as file:
        if not fieldnames:
            return

        writer = csv.DictWriter(
            file, fieldnames=fieldnames, extrasaction="ignore"
        )
        writer.writeheader()

        for row in data:
            writer.writerow({
                field: row.get(field, "") for field in fieldnames
            })
