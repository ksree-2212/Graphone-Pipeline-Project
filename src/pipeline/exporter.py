import json
import csv
import os
import pandas as pd
from typing import Dict, List, Any

class DataExporter:
    """
    Exports extracted & normalized pipeline outputs to local CSV/Excel files and structured JSON.
    """
    def __init__(self, output_dir: str = "/working_dir/c_b7023ff88e607b10/graphone_pipeline_project/data"):
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)

    def export_all_tabs(self, data: Dict[str, List[Dict[str, Any]]]) -> str:
        excel_path = os.path.join(self.output_dir, "GraphOne_Pipeline_Outputs.xlsx")
        
        with pd.ExcelWriter(excel_path, engine='openpyxl') as writer:
            # Tab 1: Startups
            startups_flat = []
            for item in data.get("startups", []):
                startups_flat.append({
                    "schemaVersion": item["schemaVersion"],
                    "recordType": item["recordType"],
                    "source_name": item["source"]["name"],
                    "source_url": item["source"]["url"],
                    "entityName": item["content"]["entityName"],
                    "employeeCount": item["content"]["data"]["employeeCount"],
                    "collectedAt": item["collectedAt"]
                })
            pd.DataFrame(startups_flat).to_excel(writer, sheet_name="Startups", index=False)

            # Tab 2: Products
            products_flat = []
            for item in data.get("products", []):
                products_flat.append({
                    "schemaVersion": item["schemaVersion"],
                    "recordType": item["recordType"],
                    "source_name": item["source"]["name"],
                    "source_url": item["source"]["url"],
                    "startupName": item["content"]["startupName"],
                    "pricingModel": item["content"]["pricingModel"],
                    "collectedAt": item["collectedAt"]
                })
            pd.DataFrame(products_flat).to_excel(writer, sheet_name="Products", index=False)

            # Tab 3: Research Papers
            papers_flat = []
            for item in data.get("papers", []):
                authors = ", ".join(item["content"]["authors"]) if isinstance(item["content"]["authors"], list) else str(item["content"]["authors"])
                papers_flat.append({
                    "schemaVersion": item["schemaVersion"],
                    "recordType": item["recordType"],
                    "title": item["content"]["title"],
                    "authors": authors,
                    "paper_url": item["content"]["paper_url"],
                    "github_url": item["content"]["github_url"],
                    "github_stars": item["content"]["github_stars"],
                    "published_date": item["content"]["published_date"]
                })
            pd.DataFrame(papers_flat).to_excel(writer, sheet_name="Research Papers", index=False)

            # Tab 4: Jobs
            jobs_flat = []
            for item in data.get("jobs", []):
                jobs_flat.append({
                    "schemaVersion": item["schemaVersion"],
                    "recordType": item["recordType"],
                    "company": item["content"]["company"],
                    "date": item["content"]["date"],
                    "is_remote": item["content"]["is_remote"],
                    "role_family": item["content"]["role_family"]
                })
            pd.DataFrame(jobs_flat).to_excel(writer, sheet_name="Jobs", index=False)

            # Tab 5: News
            news_flat = []
            for item in data.get("news", []):
                news_flat.append({
                    "schemaVersion": item["schemaVersion"],
                    "recordType": item["recordType"],
                    "title": item["content"]["title"],
                    "full_text": item["content"]["full_text"],
                    "published_date": item["content"]["published_date"],
                    "source_url": item["content"]["source_url"]
                })
            pd.DataFrame(news_flat).to_excel(writer, sheet_name="News", index=False)

            # Tab 6: Entity Mapping Log
            entity_log = data.get("entity_log", [])
            pd.DataFrame(entity_log).to_excel(writer, sheet_name="Entity Mapping Log", index=False)

        print(f"Data successfully exported to {excel_path}")
        return excel_path
