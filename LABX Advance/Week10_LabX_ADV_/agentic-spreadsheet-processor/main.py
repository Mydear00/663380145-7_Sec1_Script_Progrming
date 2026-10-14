import os
from src.config_parser import ConfigParser
from src.spreadsheet_agent import SpreadsheetAgent
from src.utils import setup_logging

logger = setup_logging("main")

def main():
    root = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.join(root, "configs", "example_spreadsheet_config.json")
    try:
        config = ConfigParser(config_path).load_config()
        # Resolve relative paths against project root, not the current terminal folder.
        config["input_file"] = os.path.join(root, config["input_file"])
        config["output_file"] = os.path.join(root, config["output_file"])
        output_path = SpreadsheetAgent(config).run()
        print(f"\nสำเร็จ! สร้างรายงานที่: {output_path}")
    except (FileNotFoundError, ValueError, OSError) as exc:
        logger.exception("ไม่สามารถทำงานได้: %s", exc)
        raise SystemExit(1)

if __name__ == "__main__":
    main()
