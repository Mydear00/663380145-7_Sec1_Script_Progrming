from pathlib import Path
import sys
from dotenv import load_dotenv
from src.config_parser import ConfigParser
from src.communication_agent import CommunicationAgent
from src.utils import ensure_directory_exists, setup_logging

logger = setup_logging(__name__)

def main():
    base_dir = Path(__file__).resolve().parent
    load_dotenv(base_dir / ".env")
    for folder in ["data/attachments", "data/reports", "data/incoming_attachments", "reports", "configs"]:
        ensure_directory_exists(base_dir / folder)
    config_path = base_dir / "configs" / "comm_pipeline_config.json"
    try:
        config = ConfigParser(config_path).load_config()
        logger.info("Starting workflow. DRY_RUN is enabled by default; no real messages will be sent.")
        agent = CommunicationAgent(config, base_dir)
        agent.run()
        logger.info("Workflow finished.")
    except Exception as exc:
        logger.exception("Could not run workflow: %s", exc)
        sys.exit(1)

if __name__ == "__main__":
    main()
