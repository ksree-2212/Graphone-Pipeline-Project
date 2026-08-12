# GraphOne / FrontierAtlas - AI Data Ingestion Pipeline

An asynchronous, fault-tolerant, end-to-end data ingestion and entity resolution pipeline designed for large-scale AI ecosystem intelligence. The system ingests, normalizes, extracts, and canonicalizes multi-dimensional entities across Startups, Products, Research Papers (with dynamic GitHub metrics), 24-Hour Fresh AI Jobs, and AI News.

---

## 🌟 Key Features

* **Massive Bulk Scraping Engine:** Built on Python's `asyncio` and `aiohttp` for non-blocking concurrent collection designed to scale to 500,000+ records.
* **Research Papers & GitHub Correlation:** Collects arXiv research papers, correlates associated GitHub code repositories, and extracts dynamic metrics (GitHub stars).
* **High-Fidelity 24-Hour Signal Ingestion:** Strict date parsing and normalization ensuring all news and job postings are guaranteed published within 24 hours.
* **Multi-Tier LLM Orchestration Engine:**
  * **Fallback Chain:** `Gemini 1.5 Flash` (Primary) → `Groq Llama 3.3 70B` (Tier 2) → `DeepSeek V3` (Tier 3).
  * **413 Payload Handling:** Semantic DOM chunking and truncation to prevent context window overflows.
  * **429 Rate Limit Resilience:** Exponential backoff with randomized jitter to handle rate limits seamlessly.
* **Deterministic Entity Resolution:** Canonicalizes raw entity variations (e.g., "OpenAI, Inc.", "Open AI") into standardized names using legal suffix stripping, seed database indexing, and fuzzy string distance matching.
* **Automated Data Export:** Multi-tab exporter generating structured output across 6 schema-compliant tabs.

---

## 📁 Output Dataset Schemas

1. **Startups (Min 1,000 rows):** `schemaVersion`, `recordType`, `source`, `content.entityName`, `content.data.employeeCount`, `collectedAt`
2. **Products (Min 1,000 rows):** `schemaVersion`, `recordType`, `source`, `content.startupName`, `content.pricingModel`, `collectedAt`
3. **Research Papers (Min 1,000 rows):** `content.title`, `content.authors`, `content.paper_url`, `content.github_url`, `content.github_stars`, `content.published_date`
4. **Jobs (24-hr Fresh):** `content.company`, `content.date`, `content.is_remote`, `content.role_family`
5. **News (24-hr Fresh):** `content.title`, `content.full_text`, `content.published_date`, `content.source_url`
6. **Entity Mapping Log:** `raw_name`, `canonical_name`, `entity_type`, `confidence_score`, `resolution_method`

---

## 🛠️ Architecture & System Design

For a full breakdown of the infrastructure scaling strategy (500k+ records), anti-bot navigation, distributed deduplication, and database selection (PostgreSQL + Neo4j + Qdrant), see [architecture.pdf](./architecture.pdf).

---

## ⚡ Quick Start

### Installation
```bash
git clone [https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git](https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git)
cd YOUR_REPO_NAME
pip install -r requirements.txt
# GraphOne / FrontierAtlas - AI Engineer Data Ingestion Pipeline

## Overview
Production-grade, asynchronous, fault-tolerant data ingestion pipeline built for **GraphOne / FrontierAtlas Intelligence Graph**. The pipeline ingests, normalizes, extracts, and canonicalizes entities across the AI and venture ecosystem, including **AI Startups, AI Products, Research Papers with GitHub Metrics, 24-hr Fresh AI Jobs, and 24-hr Fresh AI News**.

---

## Core System Architecture

### 1. Phase I & II: Massive Async Bulk Scraping & Signal Ingestion
- **High Concurrency Crawlers (`src/crawlers/`)**: Asynchronous non-blocking architecture (`asyncio` + `aiohttp`) designed to scale to 500,000+ records without code changes.
- **Research Papers Vertical**: Correlates arXiv research papers with GitHub repositories and extracts dynamic metrics (GitHub Stars).
- **24-Hour Signal Freshness**: Strict timestamp filtering guaranteeing publication dates within 24 hours for news and job postings.

### 2. Phase III: Multi-Tier LLM Extraction Engine
- **Fallback Chain (`src/llm/orchestrator.py`)**: 
  1. Primary: Gemini 1.5 Flash
  2. Fallback 1: Groq Llama 3.3 (70B)
  3. Fallback 2: DeepSeek V3
- **Intelligent Payload Chunking**: Prevents `413 Payload Too Large` errors by semantically truncating raw payloads while preserving critical information density.
- **Rate Limit Resilience**: Full `429 Too Many Requests` handling using exponential backoff with randomized jitter.

### 3. Phase IV: Deterministic Entity Resolution
- **Canonical Mapping (`src/entity_resolution/resolver.py`)**:
  - Seed-based lookup against 50 canonical AI startups.
  - Normalization engine stripping legal suffixes (`Inc.`, `LLC`, `Corp`, `Labs`, `AI`).
  - Generates an explicit **Entity Mapping Log** recording `raw_name` to `canonical_name` transitions with confidence scoring and resolution methodology.

---

## Output Datasets (Google Sheets / Excel Tabs)
The pipeline exports data into 6 required tabs:
1. **Startups** (Min 1,000 records)
2. **Products** (Min 1,000 records)
3. **Research Papers** (Min 1,000 records with GitHub repos & stars)
4. **Jobs** (All 24-hr fresh AI jobs)
5. **News** (All 24-hr fresh AI news articles)
6. **Entity Mapping Log** (Raw vs Canonical entities)

---

## Project Structure
```
graphone_pipeline_project/
├── main.py                     # Entry point script
├── requirements.txt            # Python dependencies
├── README.md                   # System documentation
├── architecture.pdf            # 3-page Technical Architecture Document
├── data/
│   └── GraphOne_Pipeline_Outputs.xlsx
└── src/
    ├── crawlers/
    │   ├── paper_crawler.py
    │   ├── startup_crawler.py
    │   ├── product_crawler.py
    │   └── news_job_crawler.py
    ├── llm/
    │   └── orchestrator.py
    ├── entity_resolution/
    │   └── resolver.py
    └── pipeline/
        ├── runner.py
        └── exporter.py
```

---

## Setup & Execution

### Prerequisites
- Python 3.10+
- Virtualenv (recommended)

### Installation
```bash
pip install -r requirements.txt
```

### Execution
Run the full end-to-end ingestion pipeline:
```bash
python main.py
```

Outputs will be saved in `data/GraphOne_Pipeline_Outputs.xlsx` and logged to standard output.
