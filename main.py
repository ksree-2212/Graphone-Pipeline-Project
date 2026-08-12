import asyncio
import sys
from src.pipeline.runner import GraphOnePipelineRunner

async def main():
    print("Initializing GraphOne Production Data Ingestion Pipeline...")
    runner = GraphOnePipelineRunner(paper_count=1000, startup_count=1000, product_count=1000)
    result = await runner.run()
    
    print("\n--- Pipeline Execution Summary ---")
    for k, v in result["summary"].items():
        print(f"  {k}: {v}")
    print(f"\nLocal Output Excel File: {result['excel_path']}")

if __name__ == "__main__":
    asyncio.run(main())
