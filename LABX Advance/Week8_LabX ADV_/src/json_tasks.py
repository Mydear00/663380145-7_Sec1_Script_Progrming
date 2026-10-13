from copy import deepcopy
from .utils import save_json_file


def find_list_item_by_id(items, item_id):
    for item in items:
        if (
            isinstance(item, dict)
            and str(item.get("id")) == str(item_id)
        ):
            return item
    return None


def get_parent_and_key(data, path):
    if not path:
        return None, None

    parts = path.split(".")
    current = data

    for part in parts[:-1]:
        if isinstance(current, list):
            if part.isdigit():
                index = int(part)
                if index < 0 or index >= len(current):
                    raise IndexError(f"List index out of range: {part}")
                current = current[index]
            else:
                current = find_list_item_by_id(current, part)
                if current is None:
                    raise KeyError(f"Item ID not found: {part}")

        elif isinstance(current, dict):
            if part not in current:
                current[part] = {}
            current = current[part]

        else:
            raise TypeError(
                f"Cannot navigate through path component: {part}"
            )

    return current, parts[-1]


def update_json_data(data, updates):
    updated_data = deepcopy(data)

    for update in updates:
        path = update.get("path", "")
        value = update.get("value")
        operation = update.get("operation", "set")

        if operation == "add_to_list" and path == "":
            if not isinstance(updated_data, list):
                raise TypeError(
                    "Root data must be a list for add_to_list"
                )
            updated_data.append(deepcopy(value))
            continue

        parent, key = get_parent_and_key(updated_data, path)

        if operation == "set":
            if isinstance(parent, dict):
                parent[key] = deepcopy(value)
            elif isinstance(parent, list) and key.isdigit():
                index = int(key)
                if index < 0 or index >= len(parent):
                    raise IndexError(
                        f"List index out of range: {index}"
                    )
                parent[index] = deepcopy(value)
            else:
                raise TypeError(f"Cannot set value at path: {path}")

        elif operation == "add_to_list":
            if isinstance(parent, dict):
                target = parent.setdefault(key, [])
            elif isinstance(parent, list) and key.isdigit():
                target = parent[int(key)]
            else:
                raise TypeError(f"Invalid list path: {path}")

            if not isinstance(target, list):
                raise TypeError(f"Target is not a list: {path}")

            target.append(deepcopy(value))

        else:
            raise ValueError(
                f"Unsupported operation: {operation}"
            )

    return updated_data


def query_json_data(data, path):
    if path == "":
        return data

    current = data

    for part in path.split("."):
        if isinstance(current, list):
            if part.isdigit():
                current = current[int(part)]
            else:
                current = find_list_item_by_id(current, part)
                if current is None:
                    raise KeyError(f"Item ID not found: {part}")

        elif isinstance(current, dict):
            if part not in current:
                raise KeyError(f"Key not found: {part}")
            current = current[part]

        else:
            raise TypeError(
                f"Cannot continue query through {type(current).__name__}"
            )

    return current


def save_json(data, file_path, indent=4):
    save_json_file(data, file_path, indent=indent)
