# Term Corpus Generator

A lightweight, full-stack web application designed to generate bilingual (English & Chinese) corpus data for economic and general terms. Built with **FastAPI** and **Vue 3**.

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.9+-blue.svg)
![Vue](https://img.shields.io/badge/vue-3.x-green.svg)

## 🚀 Features

- **Instant Bilingual Search**: Input a term (e.g., "Inflation") and retrieve its summary in both English and Chinese simultaneously.
- **Wikipedia Integration**: Automatically fetches data from Wikipedia using the `wikipedia-api` library, leveraging language links for accurate cross-lingual mapping.
- **Dual-View Interface**: Clean, modern UI displaying English and Chinese definitions side-by-side.
- **Auto-Save to Markdown**: Every search result is automatically saved as a Markdown file in the backend's `output/` directory.
- **JSON Export**: One-click export of current search results to a JSON file from the frontend.

## 🛠️ Tech Stack

### Backend
- **FastAPI**: High-performance web framework for building APIs.
- **Wikipedia-API**: Python wrapper for Wikipedia's API.
- **Pydantic**: Data validation and settings management.
- **Uvicorn**: ASGI web server implementation.

### Frontend
- **Vue 3**: Progressive JavaScript framework.
- **Vite**: Next-generation frontend tooling.
- **TailwindCSS**: Utility-first CSS framework for rapid UI development.
- **Axios**: Promise based HTTP client.

## 📂 Project Structure

```text
WikipediaPython/
├── backend/
│   ├── main.py            # FastAPI application entry point
│   ├── requirements.txt   # Python dependencies
│   └── output/            # Generated Markdown files (auto-created)
├── frontend/
│   ├── src/
│   │   └── App.vue        # Main Vue component
│   ├── index.html         # HTML entry point (Tailwind CDN included)
│   ├── package.json       # Node.js dependencies
│   └── vite.config.js     # Vite configuration
└── README.md
```

## ⚡ Quick Start

### Prerequisites
- Python 3.9+
- Node.js & npm

### 1. Start the Backend
Navigate to the `backend` directory, install dependencies, and run the server.

```bash
cd backend
pip install -r requirements.txt
python main.py
```
*The backend API will run at `http://localhost:8000`*

### 2. Start the Frontend
Open a new terminal, navigate to the `frontend` directory, install dependencies, and start the development server.

```bash
cd frontend
npm install
npm run dev
```
*The frontend will typically run at `http://localhost:5173` (or another available port shown in the terminal).*

## 📖 Usage

1. Open your browser and go to the frontend URL (e.g., `http://localhost:5173`).
2. Enter a term in the search box (e.g., "Gross Domestic Product").
3. Click **Search** or press Enter.
4. View the English and Chinese summaries side-by-side.
5. Click **Export JSON** to download the data, or check the `backend/output/` folder for the Markdown file.

## 🔌 API Endpoints

### `GET /search`
Searches for a term and returns bilingual data.

**Query Parameters:**
- `term` (string): The term to search for.

**Response:**
```json
{
  "term": "Inflation",
  "en_summary": "In economics, inflation is...",
  "en_url": "https://en.wikipedia.org/wiki/Inflation",
  "zh_summary": "在经济学中，通货膨胀...",
  "zh_url": "https://zh.wikipedia.org/wiki/%E9%80%9A%E8%B4%A7%E8%86%A8%E8%83%80"
}
```

## 🗺️ Advanced Automation Roadmap

This project is being enhanced with advanced automation capabilities to transform it from a single-term search tool into a comprehensive, self-growing knowledge corpus system.

### 🎯 Planned Features

#### **Phase 1: Batch Import & Automated Crawling** ⭐ Priority
- **Batch Input Methods**: 
  - Paste multiple terms (one per line)
  - Upload CSV/TXT/Excel files with term lists
  - Categorized imports with custom tags
- **Automation Controls**:
  - Concurrent crawling with rate limiting (avoid Wikipedia blocking)
  - Real-time progress monitoring (completed/failed/total)
  - Automatic retry mechanism for failed requests
  - Configurable crawl intervals (e.g., 2-5 seconds between requests)
- **Results Management**:
  - Batch export to JSON/CSV
  - Category-based Markdown file generation
  - Failed terms tracking for manual review
  - Crawl history and statistics

#### **Phase 2: Intelligent Association Crawling**
- **Link Discovery Strategies**:
  - "See also" sections from Wikipedia pages
  - High-frequency internal links
  - Category tags exploration
  - Cross-language related articles
- **Crawl Depth Control**:
  - Configurable depth levels (1-3 layers)
  - Maximum terms per layer
  - Blacklist filtering for irrelevant terms
- **Knowledge Graph Visualization**:
  - Force-directed graph of term relationships
  - Topic clustering display

#### **Phase 3: Scheduled & Incremental Updates**
- **Scheduling Options**:
  - Daily/Weekly/Monthly automatic updates
  - Priority-based update queue
  - Monitor Wikipedia revision history API for changes
- **Version Control**:
  - Historical version tracking
  - Diff comparison between versions
  - Change notifications (email/webhook)

#### **Phase 4: Multi-Source Data Aggregation**
- **Extended Data Sources**:
  - Wikidata (structured knowledge base)
  - Baidu Baike (Chinese encyclopedia)
  - Britannica Encyclopedia
  - Academic paper abstracts (Google Scholar/arXiv)
  - Real-time financial data for economic terms
- **Data Fusion**:
  - Intelligent deduplication and merging
  - Source attribution and credibility scoring
  - Cross-source validation

#### **Phase 5: AI-Enhanced Corpus Generation**
- **AI Augmentation**:
  - Automatic summary optimization
  - Term definition standardization
  - Named entity recognition and tagging
  - Semantic relationship generation between terms
  - Multi-language translation quality checking
- **Intelligent Recommendations**:
  - Suggest missing terms based on existing corpus
  - Identify coverage gaps in the knowledge base

#### **Phase 6: Distributed Crawling Architecture** (For Large-Scale)
- **Distributed Components**:
  - Task queue: RabbitMQ + Celery
  - Distributed storage: MongoDB/PostgreSQL
  - Cache layer: Redis
  - Load balancing across worker nodes
- **Monitoring Dashboard**:
  - Real-time crawl status monitoring
  - Resource usage metrics
  - Error log aggregation

### 🏗️ Technical Architecture (Phase 1 Preview)

**Backend Enhancements**:
```
backend/
├── main.py              # Existing FastAPI main file
├── worker.py            # New: Background task worker (Celery/RQ)
├── models.py            # New: Database models
├── scheduler.py         # New: Batch crawl scheduler
├── database.py          # New: Database connection
└── utils/
    ├── rate_limiter.py  # Rate limiting control
    └── retry.py         # Retry logic
```

**Frontend Enhancements**:
```
frontend/src/
├── App.vue                    # Existing main component
└── components/
    ├── BatchImport.vue        # Batch import interface
    ├── ProgressMonitor.vue    # Progress tracking
    └── ResultsTable.vue       # Results data table
```

**Database Schema** (SQLite for Phase 1):
```sql
-- Batch tasks tracking
CREATE TABLE tasks (
    id INTEGER PRIMARY KEY,
    status TEXT,
    created_at TIMESTAMP,
    total_terms INTEGER,
    completed INTEGER
);

-- Individual terms
CREATE TABLE terms (
    id INTEGER PRIMARY KEY,
    task_id INTEGER,
    term TEXT,
    status TEXT,
    en_summary TEXT,
    zh_summary TEXT,
    created_at TIMESTAMP,
    updated_at TIMESTAMP
);
```

### 📈 Implementation Priority

1. **Immediate** (Phase 1): Batch crawling - 10x efficiency boost with minimal complexity
2. **Short-term** (Phases 2-3): Intelligent crawling and scheduling - transform into self-growing knowledge base
3. **Mid-term** (Phases 4-5): Multi-source and AI enhancement - professional-grade corpus quality
4. **Long-term** (Phase 6): Distributed architecture - only when corpus exceeds 10,000+ terms

---

*This roadmap reflects the evolution from a simple search tool to an enterprise-grade knowledge corpus management system.*
