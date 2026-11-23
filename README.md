
# AI Intelligence Pipeline

An AI-powered intelligence pipeline that collects web information, processes it into searchable knowledge, generates context-aware answers, extracts entities, and identifies potential duplicate entities.

## Project Overview

The AI Intelligence Pipeline transforms unstructured web data into structured, searchable intelligence through a multi-stage workflow.

### Pipeline Architecture

Web Scraping → Text Processing → Chunking → Embeddings → Vector Database → Semantic Search → RAG → Entity Extraction → Entity Resolution → Intelligence Analysis

## Key Features

- Web content ingestion
- Text cleaning and chunking
- Embedding generation
- Vector storage with ChromaDB
- Semantic search
- LLM-powered question answering
- Source tracking and citations
- Entity extraction
- Entity resolution and duplicate candidate detection
- Entity type standardization
- Duplicate audit
- Intelligence analysis report generation

## Technology Stack

| Component | Technology |
|--- -|---|
| Language | Python |
| LLM | Groq API |
| Vector Database | ChromaDB |
| Embeddings | Embedding model integration |
| Data Processing | Pandas / Python utilities |
| Web Scraping | Web scraper module |
| Entity Storage | SQLite |
| RAG | Retrieval-Augmented Generation |

## Project Structure

```text
AI_Intelligence_Pipeline/
│
├── src/
│   ├── crawler/
│   │   └── web_scraper.py
│   ├── database/
│   │   └── vector_store.py
│   ├── entity_resolution/
│   │   ├── entity_store.py
│   │   ├── extractor.py
│   │   ├── resolver.py
│   │   └── merge_entities.py
│   ├── pipeline/
│   │   ├── ingestion.py
│   │   └── rag.py
│   ├── search/
│   │   └── semantic_search.py
│   ├── utils/
│   │   ├── chunking.py
│   │   └── embeddings.py
│   └── intelligence/
│       └── analysis.py
│
├── data/
├── reports/
│   └── intelligence_analysis.md
├── .env
├── requirements.txt
└── README.md
```

## How It Works

### 1. Data Ingestion

The system scrapes a webpage and extracts its textual content.

### 2. Text Processing

The extracted content is divided into manageable chunks with overlapping context.**
**

### 3. Embeddings

Text chunks are converted into vector embeddings for semantic understanding.

### 4. Vector Storage

Embeddings and metadata are stored in ChromaDB.

### 5. Semantic Search

A query is embedded and compared with stored knowledge to retrieve relevant chunks.

### 6. RAG Question Answering

Retrieved evidence is passed to an LLM to generate context-aware answers.

### 7. Source Tracking

Retrieved answers include source information to help trace the evidence used.

### 8. Entity Extraction

The LLM identifies entities such as concepts, technologies, people, and organizations.

### 9. Entity Resolution

Similarity-based matching identifies potential duplicate entities for review.

### 10. Intelligence Analysis

The system generates a Markdown report containing entity statistics, entity-type distribution, source coverage, duplicate candidates, and limitations.

## Setup

### Prerequisites

- Python 3.10+
- pip
- Groq API key

### Installation

```bash
git clone <repository-url>
cd AI_Intelligence_Pipeline
python -m venv .venv
```

Activate the environment on Windows:

```powershell
.venv\Scripts\Activate.ps1
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Create a `.env` file in the project root and configure the required API key.

> Never upload your API keys or `.env` file to a public repository.

## Running the Pipeline

### Ingestion Test

```bash
python -m src.pipeline.test_ingestion
```

### RAG Test

```bash
python -m src.pipeline.test_rag
```

### Entity Extraction Test

```bash
python -m src.pipeline.test_entity_pipeline
```

### Entity Resolution Test

```bash
python -m src.entity_resolution.test_resolver
```

### Duplicate Audit

```bash
python -m src.entity_resolution.duplicate_audit
```

### Intelligence Analysis

```bash
python -m src.intelligence.analysis
```

The generated report will be saved to:

```text
reports/intelligence_analysis.md
```

## Verified Test Results

The following results were obtained during project testing:

- Successfully scraped an Artificial Intelligence Wikipedia page.
- Extracted approximately 227,863 characters of webpage content.
- Generated 91 text chunks.
- Generated embeddings for the chunks.
- Stored 91 chunks in the vector database.
- Successfully retrieved relevant context for an AI question.
- Successfully generated an LLM answer using RAG.
- Retrieved and displayed source references with chunk information.
- Extracted entities using the LLM.
- Tested entity name similarity and duplicate candidate detection.
- Applied and verified entity type corrections.
- Applied and verified selected entity merges.
- Generated an intelligence analysis report from the entity database.

## Current Analysis Snapshot

At the time of the latest analysis:

- Total entity records: 53
- Unique normalized names: 50
- Duplicate candidate pairs: 3

Entity type distribution:

| Entity Type | Count |
|-- -|---:|
| Technology | 26 |
| Concept | 25 |
| Person | 1 |
| Organization | 1 |

The generated analysis is available at `reports/intelligence_analysis.md`.

## Limitations

- Entity extraction quality depends on source content and LLM output.
- Duplicate candidates require review before merging.
- The tested entity extraction run was a limited test, not a full-scale extraction benchmark.
- The current system primarily processes ingested sources rather than continuously monitoring the web.
- A production API and interactive dashboard are not yet included in the verified core pipeline.

## Future Improvements

- API integration
- Interactive dashboard
- Large-scale entity extraction
- Advanced entity relationship graphs
- Human-in-the-loop entity merging
- Multi-source intelligence correlation
- Temporal analysis and monitoring
- Automated scheduled ingestion

## Safety and Data Integrity

- Duplicate auditing is read-only.
- Entity merges are performed separately from duplicate detection.
- Database backups were created before major entity cleanup operations.
- Entity resolution results are treated as candidates for review rather than automatically merging every similar name.

## Project Status

**Core intelligence pipeline implemented and tested.**

The system demonstrates ingestion, vector indexing, semantic retrieval, LLM-based question answering, source tracking, entity extraction, entity resolution, and report generation.

---

Developed as an AI Intelligence Pipeline project.
