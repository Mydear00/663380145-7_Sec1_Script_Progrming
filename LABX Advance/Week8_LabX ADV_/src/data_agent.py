from datetime import datetime
from pathlib import Path

from . import conversion_tasks, csv_tasks, json_tasks
from .utils import (
    load_json_file,
    resolve_project_path,
    save_json_file,
    timestamp,
)


class DataAgent:
    def __init__(self, config, project_dir):
        self.config = config
        self.project_dir = Path(project_dir).resolve()
        self.data_store = {}
        self.audit_log = []

    def log(self, task_type, status, message, **details):
        entry = {
            "timestamp": timestamp(),
            "task_type": task_type,
            "status": status,
            "message": message,
        }

        if details:
            entry["details"] = details

        self.audit_log.append(entry)

        print(
            f"[{entry['timestamp']}] "
            f"[{status.upper()}] {task_type}: {message}"
        )

    def get_path(self, path):
        return resolve_project_path(self.project_dir, path)

    def require_data(self, key):
        if key not in self.data_store:
            raise KeyError(
                f"Data key '{key}' does not exist in data_store"
            )
        return self.data_store[key]

    def execute_task(self, task):
        task_type = task.get("type", "unknown")
        output_key = task.get("output_key")

        try:
            if task_type == "load_csv":
                path = self.get_path(task["file_path"])
                result = csv_tasks.load_csv(path)
                self.data_store[output_key] = result
                self.log(
                    task_type, "success",
                    f"Loaded {len(result)} CSV rows"
                )

            elif task_type == "aggregate_csv":
                result = csv_tasks.aggregate_csv(
                    self.require_data(task["input_key"]),
                    task["group_by_field"],
                    task["aggregate_field"],
                    task.get("operation", "sum"),
                )
                self.data_store[output_key] = result
                self.log(
                    task_type, "success",
                    f"Created {len(result)} groups"
                )

            elif task_type == "save_csv":
                path = self.get_path(task["file_path"])
                csv_tasks.save_csv(
                    self.require_data(task["input_key"]),
                    path,
                    task.get("fieldnames"),
                )
                self.log(
                    task_type, "success", f"Saved CSV to {path}"
                )

            elif task_type == "csv_to_json":
                result = conversion_tasks.csv_to_json(
                    self.require_data(task["input_key"])
                )
                self.data_store[output_key] = result
                self.log(
                    task_type, "success",
                    f"Converted {len(result)} rows to JSON"
                )

            elif task_type == "save_json":
                path = self.get_path(task["file_path"])
                save_json_file(
                    self.require_data(task["input_key"]),
                    path,
                    indent=task.get("indent", 4),
                )
                self.log(
                    task_type, "success", f"Saved JSON to {path}"
                )

            elif task_type == "load_json":
                path = self.get_path(task["file_path"])
                result = load_json_file(path)
                self.data_store[output_key] = result
                self.log(
                    task_type, "success", f"Loaded JSON from {path}"
                )

            elif task_type == "update_json":
                result = json_tasks.update_json_data(
                    self.require_data(task["input_key"]),
                    task.get("updates", []),
                )
                self.data_store[output_key] = result
                self.log(
                    task_type, "success",
                    f"Applied {len(task.get('updates', []))} updates"
                )

            elif task_type == "query_json":
                result = json_tasks.query_json_data(
                    self.require_data(task["input_key"]),
                    task["path"],
                )
                self.data_store[output_key] = result
                self.log(
                    task_type, "success",
                    f"Queried path {task['path']}",
                    result=result,
                )

            else:
                raise ValueError(
                    f"Unsupported task type: {task_type}"
                )

        except Exception as error:
            self.log(task_type, "error", str(error))
            if self.config.get("stop_on_error", True):
                raise

    def generate_audit_report(self):
        reports_dir = self.project_dir / "reports"
        reports_dir.mkdir(parents=True, exist_ok=True)

        filename = (
            "audit_report_"
            + datetime.now().strftime("%Y%m%d_%H%M%S")
            + ".json"
        )
        report_path = reports_dir / filename

        report = {
            "project": self.config.get(
                "project_name", "Agentic Data Processor"
            ),
            "generated_at": timestamp(),
            "task_count": len(self.audit_log),
            "success_count": sum(
                item["status"] == "success"
                for item in self.audit_log
            ),
            "error_count": sum(
                item["status"] == "error"
                for item in self.audit_log
            ),
            "audit_log": self.audit_log,
        }

        save_json_file(report, report_path, indent=4)
        print(f"\\nAudit report saved: {report_path}")
        return report_path

    def run(self):
        tasks = self.config.get("tasks", [])

        print("=" * 60)
        print(self.config.get(
            "project_name", "Agentic Data Processor"
        ))
        print("=" * 60)

        for index, task in enumerate(tasks, start=1):
            print(f"\\nTask {index}/{len(tasks)}")
            self.execute_task(task)

        return self.generate_audit_report()
