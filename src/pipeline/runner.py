import asyncio
import logging
from typing import Dict, Any, List

from src.crawlers.paper_crawler import ResearchPaperCrawler
from src.crawlers.startup_crawler import StartupCrawler
from src.crawlers.product_crawler import ProductCrawler
from src.crawlers.news_job_crawler import SignalCrawler
from src.llm.orchestrator import MultiTierLLMEngine
from src.entity_resolution.resolver import EntityResolver
from src.pipeline.exporter import DataExporter

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s")
logger = logging.getLogger("PipelineRunner")

class GraphOnePipelineRunner:
    """
    Main Orchestration Pipeline for GraphOne Intelligence Graph.
    Coordinates crawling, LLM structured extraction, entity resolution, and data export.
    """
    def __init__(self, paper_count: int = 1000, startup_count: int = 1000, product_count: int = 1000):
        self.paper_crawler = ResearchPaperCrawler(target_count=paper_count)
        self.startup_crawler = StartupCrawler(target_count=startup_count)
        self.product_crawler = ProductCrawler(target_count=product_count)
        self.signal_crawler = SignalCrawler()
        self.llm_engine = MultiTierLLMEngine()
        self.resolver = EntityResolver()
        self.exporter = DataExporter()

    async def run(self) -> Dict[str, Any]:
        logger.info("=== Starting GraphOne Ingestion & Processing Pipeline ===")

        # Phase I & II: Concurrent Async Scrape
        logger.info("Executing Phase I & II: Massive Async Bulk Scraping & Signal Ingestion...")
        papers_task = asyncio.create_task(self.paper_crawler.fetch_papers())
        startups_task = asyncio.create_task(self.startup_crawler.fetch_startups())
        products_task = asyncio.create_task(self.product_crawler.fetch_products())
        jobs_task = asyncio.create_task(self.signal_crawler.fetch_24h_jobs())
        news_task = asyncio.create_task(self.signal_crawler.fetch_24h_news())

        papers, raw_startups, raw_products, jobs, news = await asyncio.gather(
            papers_task, startups_task, products_task, jobs_task, news_task
        )

        logger.info(f"Scraped {len(papers)} Research Papers.")
        logger.info(f"Scraped {len(raw_startups)} Startups.")
        logger.info(f"Scraped {len(raw_products)} Products.")
        logger.info(f"Scraped {len(jobs)} 24-hr Jobs.")
        logger.info(f"Scraped {len(news)} 24-hr News items.")

        # Phase III: LLM Extraction Demonstration
        logger.info("Executing Phase III: LLM Multi-Tier Fallback & Chunking Engine...")
        sample_raw_text = "GraphOne Intelligence Platform: Ingesting 100,000s of entity records across frontier AI labs."
        llm_extraction = await self.llm_engine.extract_structured_json(sample_raw_text)

        # Phase IV: Entity Resolution
        logger.info("Executing Phase IV: Deterministic Entity Resolution...")
        entity_log = []
        resolved_startups = []
        resolved_products = []

        # Resolve Startups
        for item in raw_startups:
            raw_name = item["content"]["entityName"]
            res = self.resolver.resolve(raw_name, entity_type="STARTUP")
            entity_log.append(res)
            
            # Update item with canonical name
            item["content"]["entityName"] = res["canonical_name"]
            resolved_startups.append(item)

        # Resolve Products
        for item in raw_products:
            raw_sname = item["content"]["startupName"]
            res = self.resolver.resolve(raw_sname, entity_type="PRODUCT")
            entity_log.append(res)

            item["content"]["startupName"] = res["canonical_name"]
            resolved_products.append(item)

        logger.info(f"Entity Resolution complete. Processed {len(entity_log)} mapping log entries.")

        # Export Output Datasets
        pipeline_data = {
            "startups": resolved_startups,
            "products": resolved_products,
            "papers": papers,
            "jobs": jobs,
            "news": news,
            "entity_log": entity_log
        }

        excel_path = self.exporter.export_all_tabs(pipeline_data)

        logger.info("=== GraphOne Pipeline Execution Completed Successfully ===")
        return {
            "excel_path": excel_path,
            "summary": {
                "startups_count": len(resolved_startups),
                "products_count": len(resolved_products),
                "papers_count": len(papers),
                "jobs_count": len(jobs),
                "news_count": len(news),
                "entity_log_count": len(entity_log)
            }
        }
