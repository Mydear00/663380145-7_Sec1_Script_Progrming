from pathlib import Path

from src.config_parser import ConfigParser
from src.data_agent import DataAgent


def main():
    project_dir = Path(__file__).resolve().parent
    config_path = (
        project_dir / "configs" / "data_pipeline_config.json"
    )

    try:
        config = ConfigParser(config_path).load_config()
        agent = DataAgent(config, project_dir)
        report_path = agent.run()

        print("\\nWorkflow completed successfully!")
        print(f"Audit report: {report_path}")

        if "queried_product_brand" in agent.data_store:
            print(
                "Queried product brand: "
                f"{agent.data_store['queried_product_brand']}"
            )

    except Exception as error:
        print(f"\\nWorkflow failed: {error}")
        raise SystemExit(1)


if __name__ == "__main__":
    main()
