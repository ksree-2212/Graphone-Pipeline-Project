import sys
import os
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable, PageBreak, KeepTogether
from reportlab.pdfgen import canvas

class NumberedCanvas(canvas.Canvas):
    """
    Two-pass canvas to dynamically display 'Page X of Y' page numbers.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_page_decorations(self, page_count):
        self.saveState()
        self.setFont("Helvetica", 9)
        self.setFillColor(HexColor("#4B5563")) # Slate gray
        
        # Header (Pages > 1)
        if self._pageNumber > 1:
            self.drawString(54, 750, "GraphOne / FrontierAtlas — System Architecture Document")
            self.setStrokeColor(HexColor("#E5E7EB"))
            self.setLineWidth(0.5)
            self.line(54, 742, 558, 742)

        # Footer (All pages)
        footer_text = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(558, 36, footer_text)
        self.drawString(54, 36, "CONFIDENTIAL — FOR TECHNICAL EVALUATION ONLY")
        self.setStrokeColor(HexColor("#E5E7EB"))
        self.setLineWidth(0.5)
        self.line(54, 48, 558, 48)
        
        self.restoreState()

def build_architecture_pdf(output_filename="architecture.pdf"):
    pdf_path = os.path.join("/working_dir/c_b7023ff88e607b10/graphone_pipeline_project", output_filename)
    doc = SimpleDocTemplate(
        pdf_path,
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=54,
        bottomMargin=54
    )

    styles = getSampleStyleSheet()
    
    # Custom Palette
    c_primary = HexColor("#1E3A8A")   # Navy Blue
    c_secondary = HexColor("#0D9488") # Teal
    c_dark = HexColor("#111827")      # Charcoal Body Text
    c_bg = HexColor("#F8FAFC")        # Light Gray Callout

    # Paragraph Styles
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=22,
        leading=26,
        textColor=c_primary,
        spaceAfter=6
    )

    subtitle_style = ParagraphStyle(
        'DocSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=12,
        leading=16,
        textColor=c_secondary,
        spaceAfter=15
    )

    h1_style = ParagraphStyle(
        'Heading1_Custom',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=14,
        leading=18,
        textColor=c_primary,
        spaceBefore=12,
        spaceAfter=6,
        keepWithNext=True
    )

    h2_style = ParagraphStyle(
        'Heading2_Custom',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=11,
        leading=15,
        textColor=c_secondary,
        spaceBefore=8,
        spaceAfter=4,
        keepWithNext=True
    )

    body_style = ParagraphStyle(
        'Body_Custom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9.5,
        leading=13.5,
        textColor=c_dark,
        spaceAfter=6
    )

    bullet_style = ParagraphStyle(
        'Bullet_Custom',
        parent=body_style,
        leftIndent=15,
        bulletIndent=5,
        spaceAfter=4
    )

    story = []

    # Title & Subtitle
    story.append(Paragraph("GraphOne / FrontierAtlas Intelligence Graph", title_style))
    story.append(Paragraph("Technical Architecture & Scale Strategy Document (Targeting 500,000+ Records)", subtitle_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=c_primary, spaceAfter=12))

    # Executive Summary Box
    summary_text = (
        "<b>Executive Summary:</b> This document outlines the architectural blueprint for GraphOne's autonomous, "
        "production-grade data ingestion pipeline. It addresses high-concurrency collection of 500,000+ entities "
        "(Startups, Products, Research Papers with GitHub metrics, Jobs, and News), robust multi-tier LLM fallback orchestration, "
        "distributed 24-hour freshness tracking, and unified graph-vector storage."
    )
    summary_table = Table([[Paragraph(summary_text, body_style)]], colWidths=[504])
    summary_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), c_bg),
        ('BOX', (0, 0), (-1, -1), 1, c_secondary),
        ('PADDING', (0, 0), (-1, -1), 8),
    ]))
    story.append(summary_table)
    story.append(Spacer(1, 10))

    # Section 1: Massive Bulk Acquisition at Scale (500k+)
    story.append(Paragraph("1. Scale Strategy: Acquiring 500,000+ Entities", h1_style))
    story.append(Paragraph(
        "To scale ingestion from initial thousands to over 500,000 records without manual intervention, "
        "we decouple web crawling from structured extraction through an asynchronous, event-driven architecture.",
        body_style
    ))

    story.append(Paragraph("Architectural Components:", h2_style))
    story.append(Paragraph("• <b>Distributed Async Crawler Pool:</b> Built on Python's <code>asyncio</code> + <code>aiohttp</code> / Playwright Async nodes, deployed across Kubernetes Pods. Scrapers run stateless worker loops reading targeted domains from a centralized Redis Queue.", bullet_style))
    story.append(Paragraph("• <b>Distributed Rate Limiting & Proxy Mesh:</b> Integrates BrightData / Smartproxy rotating IP networks with token-bucket rate limiters in Redis. Prevents IP bans and handles anti-bot measures (Cloudflare, Datadome) via TLS fingerprinting (curl_cffi) and browser-based stealth proxies.", bullet_style))
    story.append(Paragraph("• <b>Source Vertical Parallelization:</b> Dedicated workers partition work by vertical: arXiv / PapersWithCode API dumps for research papers, ProductHunt / Crunchbase sitemaps for startups and products, and RSS / Career portals for 24-hr signals.", bullet_style))

    # Scale Table
    scale_data = [
        [Paragraph("<b>Vertical</b>", body_style), Paragraph("<b>Target Volume</b>", body_style), Paragraph("<b>Primary Ingestion Source</b>", body_style), Paragraph("<b>Concurrency Mechanism</b>", body_style)],
        [Paragraph("Startups", body_style), Paragraph("150,000+", body_style), Paragraph("Crunchbase, YC, PitchBook", body_style), Paragraph("Async HTTP + Sitemap Walkers", body_style)],
        [Paragraph("Products", body_style), Paragraph("150,000+", body_style), Paragraph("ProductHunt, G2, App Store", body_style), Paragraph("GraphQL API + Async Workers", body_style)],
        [Paragraph("Research Papers", body_style), Paragraph("200,000+", body_style), Paragraph("arXiv OAI-PMH, PapersWithCode", body_style), Paragraph("Bulk S3 Dumps + GitHub REST API", body_style)]
    ]
    t_scale = Table(scale_data, colWidths=[90, 84, 170, 160])
    t_scale.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_primary),
        ('TEXTCOLOR', (0,0), (-1,0), HexColor("#FFFFFF")),
        ('GRID', (0,0), (-1,-1), 0.5, HexColor("#CBD5E1")),
        ('PADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(Spacer(1, 4))
    story.append(t_scale)
    story.append(Spacer(1, 12))

    # Section 2: Resilient Multi-Tier LLM Orchestration
    story.append(Paragraph("2. Resilient LLM Integration: Managing 413s & 429s", h1_style))
    story.append(Paragraph(
        "Extracting schema-compliant JSON from raw, unstructured web pages requires managing strict API quotas "
        "and token window limits. Our system employs a multi-tiered fallback pipeline with adaptive payload chunking.",
        body_style
    ))

    story.append(Paragraph("Handling Context Window Overflows (413 Payload Too Large):", h2_style))
    story.append(Paragraph("• <b>Semantic Truncation & DOM Distillation:</b> Raw HTML is stripped of scripts, styles, and boilerplate navigation using <code>BeautifulSoup4</code> and <code>html2text</code>. If payload exceeds tier limits, a density-preserving chunker retains 70% header/main content and 30% tail context.", bullet_style))
    story.append(Paragraph("• <b>Recursive Map-Reduce Chunking:</b> For massive articles or technical papers, text is split into 4k token overlapping windows, processed independently, and merged via a final synthesis pass.", bullet_style))

    story.append(Paragraph("Handling Rate Limits (429 Too Many Requests):", h2_style))
    story.append(Paragraph("• <b>Multi-Tier Fallback Chain:</b> Gemini 1.5 Flash (Primary) → Groq Llama 3.3 70B (Tier 2) → DeepSeek V3 (Tier 3). If primary tier returns 429 or times out, request cascades automatically.", bullet_style))
    story.append(Paragraph("• <b>Full Jitter Exponential Backoff:</b> Backoff time calculated as <code>Wait = Random(0, Min(Cap, Base * 2^attempt))</code> to prevent thundering herd problems across worker pods.", bullet_style))

    # LLM Table
    llm_data = [
        [Paragraph("<b>LLM Tier</b>", body_style), Paragraph("<b>Model</b>", body_style), Paragraph("<b>Context Window</b>", body_style), Paragraph("<b>Primary Role</b>", body_style)],
        [Paragraph("Primary", body_style), Paragraph("Gemini 1.5 Flash", body_style), Paragraph("1,000,000 Tokens", body_style), Paragraph("High-throughput bulk extraction", body_style)],
        [Paragraph("Fallback 1", body_style), Paragraph("Groq Llama 3.3 70B", body_style), Paragraph("128,000 Tokens", body_style), Paragraph("Low-latency fallback on Gemini 429", body_style)],
        [Paragraph("Fallback 2", body_style), Paragraph("DeepSeek V3", body_style), Paragraph("64,000 Tokens", body_style), Paragraph("High-reasoning final extraction", body_style)]
    ]
    t_llm = Table(llm_data, colWidths=[80, 120, 110, 194])
    t_llm.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_secondary),
        ('GRID', (0,0), (-1,-1), 0.5, HexColor("#CBD5E1")),
        ('PADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(Spacer(1, 4))
    story.append(t_llm)
    story.append(Spacer(1, 12))

    # Section 3: High-Fidelity Signal Ingestion & 24-Hour Freshness
    story.append(Paragraph("3. Freshness Tracking & Anti-Deduplication Engine", h1_style))
    story.append(Paragraph(
        "GraphOne guarantees real-time signal accuracy by validating that news and job postings are published within the last 24 hours.",
        body_style
    ))
    story.append(Paragraph("• <b>Bloom Filter + Redis Fingerprinting:</b> Every ingested item URL and content hash (SHA-256) is checked against a Redis Bloom Filter. If present, crawler skips processing immediately.", bullet_style))
    story.append(Paragraph("• <b>Date Normalization Engine:</b> Custom logic parses ISO dates, Unix timestamps, and relative strings ('3 hours ago', '1 day ago'). Items with publication dates older than 24 hours are dropped prior to LLM extraction.", bullet_style))
    story.append(Paragraph("• <b>Intelligent Content Difference Heuristics:</b> When strict publication meta tags are absent, a lightweight DOM hashing comparison checks for new semantic content blocks since the previous crawl pass.", bullet_style))

    story.append(Spacer(1, 10))

    # Section 4: Deterministic Entity Resolution
    story.append(Paragraph("4. Deterministic Entity Resolution Pipeline", h1_style))
    story.append(Paragraph(
        "Entity ambiguity (e.g. 'OpenAI', 'OpenAI Inc.', 'Open AI') compromises intelligence graph integrity. "
        "We implement a multi-stage deterministic canonicalization engine:",
        body_style
    ))
    story.append(Paragraph("1. <b>Legal Suffix Normalization:</b> Strip corporate suffixes (<code>Inc.</code>, <code>LLC</code>, <code>Corp</code>, <code>Labs</code>, <code>AI</code>) and standardize whitespace.", bullet_style))
    story.append(Paragraph("2. <b>Seed Database Index Lookup:</b> Match normalized strings against an in-memory seed index of 50+ known canonical AI organizations.", bullet_style))
    story.append(Paragraph("3. <b>Fuzzy Levenshtein & Jaro-Winkler Matching:</b> High-confidence fuzzy string matching (threshold > 0.88) clusters minor spelling variations.", bullet_style))
    story.append(Paragraph("4. <b>Audit Logging:</b> Every canonicalization event is recorded in the <i>Entity Mapping Log</i> with raw string, canonical output, confidence score, and method.", bullet_style))

    story.append(Spacer(1, 10))

    # Section 5: Storage Architecture & Primary Database Justification
    story.append(Paragraph("5. Storage Architecture: Graph & Vector Hybrid Model", h1_style))
    story.append(Paragraph(
        "Mapping multi-dimensional relationships between Startups, Founders, Products, Papers, and Jobs requires a dual-database storage strategy:",
        body_style
    ))
    story.append(Paragraph("• <b>Primary Relational DB (PostgreSQL + PostGIS):</b> Stores raw entity records, normalized schemas, audit logs, and transactional job/news signals with ACID guarantees.", bullet_style))
    story.append(Paragraph("• <b>Graph Database (Neo4j / Amazon Neptune):</b> Represents canonical nodes (Startup, Product, Paper, Founder) and edge relationships (<code>PRODUCES</code>, <code>AUTHORED_BY</code>, <code>HIRING_FOR</code>, <code>CITES</code>). Allows sub-millisecond graph traversal queries.", bullet_style))
    story.append(Paragraph("• <b>Vector Database (Qdrant / Pinecone):</b> Stores 1536-dimensional embeddings (e.g. OpenAI text-embedding-3-small) of full news text and paper abstracts to enable semantic search and automatic entity disambiguation.", bullet_style))

    # Storage Summary Table
    storage_data = [
        [Paragraph("<b>Storage Layer</b>", body_style), Paragraph("<b>Technology</b>", body_style), Paragraph("<b>Purpose & Data Models</b>", body_style)],
        [Paragraph("Primary Database", body_style), Paragraph("PostgreSQL 16", body_style), Paragraph("Structured entity records, JSONB schemas, system logs", body_style)],
        [Paragraph("Graph Database", body_style), Paragraph("Neo4j / Neptune", body_style), Paragraph("Complex entity-relationship mapping & graph queries", body_style)],
        [Paragraph("Vector Database", body_style), Paragraph("Qdrant Cloud", body_style), Paragraph("Semantic search, paper/news embeddings, similarity clustering", body_style)],
        [Paragraph("In-Memory Cache", body_style), Paragraph("Redis Enterprise", body_style), Paragraph("Bloom filters, deduplication hashes, distributed queue", body_style)]
    ]
    t_storage = Table(storage_data, colWidths=[110, 120, 274])
    t_storage.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_primary),
        ('TEXTCOLOR', (0,0), (-1,0), HexColor("#FFFFFF")),
        ('GRID', (0,0), (-1,-1), 0.5, HexColor("#CBD5E1")),
        ('PADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(Spacer(1, 4))
    story.append(t_storage)

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"Architecture PDF successfully built at: {pdf_path}")

if __name__ == "__main__":
    build_architecture_pdf()
