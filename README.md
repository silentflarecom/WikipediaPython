# Term Corpus Generator

A lightweight, full-stack web application designed to generate **multilingual corpus data** for economic and general terms. Built with **FastAPI** and **Vue 3**.

Supports **20+ languages** including English, Traditional Chinese, Simplified Chinese, Japanese, Korean, Spanish, French, German, Russian, and more.

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.9+-blue.svg)
![Vue](https://img.shields.io/badge/vue-3.x-green.svg)

## 📖 Quick Start

**⚠️ IMPORTANT**: Before running this application, you must configure your own User-Agent. See **[SETUP.md](SETUP.md)** for detailed installation and configuration instructions.

**TL;DR:**
1. Install dependencies (Python + Node.js)
2. Start backend and frontend servers
3. **Configure User-Agent in the Manage page** (required by Wikipedia API)
4. Start crawling!

## 🚀 Features

- **Instant Multilingual Search**: Input a term (e.g., "Inflation") and retrieve its summary in 20+ languages simultaneously.
- **Wikipedia Integration**: Automatically fetches data from Wikipedia using the `wikipedia-api` library, leveraging language links for accurate cross-lingual mapping.
- **Multi-Language Interface**: Clean, modern UI displaying multiple language definitions with flags and labels.
- **Auto-Save to Markdown**: Every search result is automatically saved as a Markdown file in the backend's `output/` directory.
- **JSON Export**: One-click export of current search results to a JSON file from the frontend.

### ⚡ New Features (v2.0)

- **📚 Batch Import & Automation**: Crawl hundreds of terms automatically via text input or file upload (CSV/TXT).
- **🇨🇳 Smart Chinese Conversion**: Automatically converts Traditional Chinese (Wikipedia default) to Simplified Chinese using `zhconv`.
- **📊 Real-time Monitoring**: Dashboard to track crawling progress, success/failure rates, and current status.
- **💾 Database Persistence**: Uses SQLite to store crawl history, allowing you to resume tasks or export data anytime.
- **📥 Robust Export**: Download results as valid JSON files or UTF-8 encoded CSVs (Excel compatible).

### 🌐 New Features (v2.1 - Intelligent Association Crawling)

- **🕸️ Knowledge Graph Visualization**: Interactive D3.js force-directed graph showing term relationships.
- **🎯 Depth-Controlled Crawling**: Configure crawl depth (1-3 levels) to automatically discover related terms from "See Also" and internal links.
- **📊 Association Tracking**: Stores term relationships (links, categories) in database for graph generation.
- **�️ Multi-Format Export**: Export knowledge graphs as PNG (high-res), SVG (editable), or JSON (data).
- **🎯 Smart Label Display**: Only shows labels for root and first-layer nodes to reduce visual clutter.

### 🌍 New Features (v2.2 - Multilingual Expansion)

- **🌐 20+ Language Support**: Crawl Wikipedia content in 20+ languages including Traditional Chinese (繁體中文), Japanese (日本語), Korean (한국어), Spanish, French, German, Russian, and more.
- **🇹🇼 Traditional Chinese**: Added Traditional Chinese support with automatic variant conversion using `zhconv`.
- **📝 Dynamic Language Selection**: Choose target languages before each crawl from an intuitive multi-select interface.
- **🔄 Auto-Translation Discovery**: Uses Wikipedia's language links to find corresponding articles across all selected languages.
- **📊 Multi-Language Display**: View all translations side-by-side in the results table with language-specific flags and labels.

### 🛠️ New Features (v2.3 - Data Management & Quality Control)

- **💾 Database Backup & Restore**: 
  - Download complete database backups (`.db` files)
  - Upload and restore from previous backups with safety checks
  - Automatic backup before restore operations
- **📤 Enhanced Export Formats**:
  - **JSON**: Complete metadata including ID, status, timestamps, depth_level, and all translations
  - **JSONL**: Machine learning ready format with dynamic language columns
  - **CSV/TSV**: Excel-compatible with ID column and all selected languages
  - **TMX**: Professional translation memory format for CAT tools
  - **TXT**: Human-readable multilingual format
- **🧹 Data Quality Tools**:
  - Quality analysis dashboard showing completion rates and issues
  - Clean data wizard to remove failed/incomplete entries
  - Filter and view problematic terms
- **🌐 English UI**: Complete interface localization (UI in English, content in selected languages)
- **⚙️ System Configuration**:
  - Editable User-Agent settings (required by Wikipedia API)
  - Settings persist across sessions
  - No server restart required

## 🛠️ Tech Stack

### Backend
- **FastAPI**: High-performance web framework.
- **SQLite + aiosqlite**: Async database for managing batch tasks.
- **Wikipedia-API**: Official MediaWiki API wrapper.
- **zhconv**: Advanced Traditional-to-Simplified Chinese conversion.
- **Pydantic**: Data validation.

### Frontend
- **Vue 3 + Vite**: Lightning fast frontend.
- **TailwindCSS**: Utility-first styling.
- **D3.js**: Knowledge graph visualization.
- **Axios**: HTTP client.

## ⚖️ Compliance & Best Practices

This tool is designed to strictly adhere to [Wikipedia's User-Agent Policy](https://meta.wikimedia.org/wiki/User-Agent_policy) and API Usage Guidelines:
 
1.  **Official API**: Uses the standard MediaWiki API endpoints, not screen scraping.
2.  **User-Agent**: 
    - ⚠️ **You MUST configure your own User-Agent** before using this tool
    - Access the **Manage** page → **System Configuration** to set your User-Agent
    - Must include your project name and contact information (email or GitHub URL)
    - Example: `YourProject/1.0 (your-email@example.com)` or `YourProject/1.0 (https://github.com/YourUsername/YourRepo)`
    - See [SETUP.md](SETUP.md) for detailed instructions
3.  **Rate Limiting**: Enforces a configurable delay (default 3s) between requests used in batch mode to prevent server overload.
4.  **Sequential Processing**: Batch tasks are processed serially to maintain a low concurrency footprint.
5.  **Privacy**: Database files are gitignored by default. No personal data is collected or transmitted.

## 🗺️ Advanced Automation Roadmap

### 🎯 Planned Features

#### **Phase 1: Batch Import & Automated Crawling** ✅ COMPLETED
- **Batch Input Methods**: 
  - Paste multiple terms (one per line) ✅
  - Upload CSV/TXT files ✅
- **Automation Controls**:
  - Concurrent crawling with rate limiting ✅
  - Real-time progress monitoring ✅
  - Automatic retry mechanism ✅
- **Results Management**:
  - Batch export to JSON/CSV (Simplified Chinese support) ✅
  - Database persistence ✅

#### **Phase 2: Intelligent Association Crawling** ✅ COMPLETED
- **Link Discovery Strategies**:
  - "See also" sections from Wikipedia pages ✅
  - High-frequency internal links (via Associations) ✅
  - Category tags exploration ✅
  - Cross-language related articles (via langlinks) ✅
- **Crawl Depth Control**:
  - Configurable depth levels (1-3 layers) ✅
  - Maximum terms per layer ✅
  - Blacklist filtering for irrelevant terms (Basic filtering implemented) ✅
- **Knowledge Graph Visualization**:
  - Force-directed graph of term relationships ✅
  - Topic clustering display (via Force Layout) ✅
  - **Multi-format export: PNG, SVG, JSON** ✅
  - Smart full-graph capture (ignores zoom state) ✅

#### **Phase 3: Corpus Quality & Data Management** ✅ COMPLETED
- **Term Deduplication**:
  - Detect duplicate terms before batch crawling ✅
  - UI warning for existing terms with skip/force options ✅
  - Global duplicate check across all tasks ✅
- **Data Quality Control**:
  - Automatic quality analysis (missing translations, short summaries) ✅
  - Quality report dashboard ✅
  - Data cleaning tools (remove failed/low-quality entries) ✅
- **Batch Task Management**:
  - View all historical batch tasks ✅
  - Delete/archive old tasks ✅
  - Merge multiple tasks into unified corpus (Partial: export-based merging possible)

#### **Phase 4: Advanced Export & Persistence** ✅ COMPLETED
- **Multi-Format Export**:
  - JSONL (one JSON object per line) - ML training ready ✅
  - TMX (Translation Memory eXchange) - CAT tool compatible ✅
  - TSV (Tab-separated values) - Excel/Pandas friendly ✅
  - TXT (Plain text bilingual pairs) - Simple readable format ✅
  - ~~Parquet (Optional) - Big data processing~~ (Not implemented - not needed for current scale)
- **Data Persistence**:
  - Database backup/restore functionality ✅
  - Complete data reset with confirmation ✅
  - Export entire corpus as portable file ✅

#### **Phase 5: Multilingual Wikipedia Expansion** ✅ COMPLETED
- **Multi-Language Support**:
  - Support for 20+ Wikipedia languages ✅
  - Traditional Chinese (zh-tw) and Simplified Chinese (zh) ✅
  - Dynamic language selection per task ✅
  - Automatic variant conversion (zhconv) ✅
- **Language Detection & Linking**:
  - Use Wikipedia langlinks for translation discovery ✅
  - Store translations in structured JSON format ✅
  - Multi-language display in results table ✅

#### **Phase 6: System Configuration & Compliance** ✅ COMPLETED
- **User-Agent Configuration**:
  - Editable User-Agent in UI (Manage page) ✅
  - Persistent settings storage in database ✅
  - Wikipedia API compliance ✅

#### **Phase 7: Corpus Statistics & Analytics** (Future Enhancement)
- **Statistics Dashboard**:
  - Total terms / bilingual pairs count ✅ (Basic stats implemented)
  - Character count (EN/ZH separately)
  - Average summary length
  - Database size metrics ✅ (Implemented)
  - Knowledge graph node/edge counts ✅ (Implemented)
- **Coverage Analysis**:
  - Success rate visualization
  - Missing translation tracking
  - Domain distribution (if tagged)

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

**Database Schema** (Current Implementation):
```sql
-- Batch tasks tracking
CREATE TABLE batch_tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    status TEXT NOT NULL,
    total_terms INTEGER DEFAULT 0,
    completed_terms INTEGER DEFAULT 0,
    failed_terms INTEGER DEFAULT 0,
    max_depth INTEGER DEFAULT 1,
    target_languages TEXT DEFAULT 'en,zh',  -- Comma-separated language codes
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Individual terms
CREATE TABLE terms (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    task_id INTEGER,
    term TEXT NOT NULL,
    status TEXT NOT NULL,
    en_summary TEXT,
    en_url TEXT,
    zh_summary TEXT,
    zh_url TEXT,
    translations TEXT,  -- JSON string: {"lang": {"summary": "...", "url": "..."}}
    error_message TEXT,
    depth_level INTEGER DEFAULT 0,
    source_term_id INTEGER,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (task_id) REFERENCES batch_tasks(id)
);

-- Term associations (for knowledge graph)
CREATE TABLE term_associations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    source_term_id INTEGER,
    target_term TEXT,
    association_type TEXT,
    weight REAL DEFAULT 1.0,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (source_term_id) REFERENCES terms(id)
);

-- System settings (User-Agent, etc.)
CREATE TABLE system_settings (
    key TEXT PRIMARY KEY,
    value TEXT,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

### 📈 Implementation Status

**✅ Completed Phases:**
1. **Phase 1** (v2.0): Batch Import & Automated Crawling - Core automation infrastructure
2. **Phase 2** (v2.1): Intelligent Association Crawling & Knowledge Graph - Self-growing knowledge base
3. **Phase 3** (v2.2): Corpus Quality & Data Management - Quality control and task management
4. **Phase 4** (v2.3): Advanced Export & Persistence - Professional export formats and backup/restore
5. **Phase 5** (v2.2): Multilingual Wikipedia Expansion - 20+ language support
6. **Phase 6** (v2.3): System Configuration & Compliance - User-Agent settings and API compliance

**🎯 Future Enhancements (Phase 7+):**
- Advanced statistics and analytics dashboard
- Character-level corpus analysis
- Domain tagging and classification
- Distributed crawling architecture (for 10,000+ terms scale)

---

## 📝 Recent Updates

### v2.3 - Data Management & System Settings (December 2025)
- ✅ Complete database backup and restore functionality
- ✅ Enhanced export with full metadata (JSON, JSONL, CSV, TSV, TMX, TXT)
- ✅ Data quality analysis and cleaning tools
- ✅ System configuration panel for User-Agent settings
- ✅ Complete English UI localization
- ✅ Privacy protection: Removed personal info from default configs
- ✅ Added .gitignore for database and sensitive files
- ✅ Created SETUP.md with User-Agent configuration guide

### v2.2 - Multilingual Expansion (December 2025)
- ✅ Support for 20+ Wikipedia languages
- ✅ Traditional Chinese (繁體中文) with automatic conversion
- ✅ Dynamic language selection per crawl task
- ✅ Multi-language results display with flags
- ✅ Translations stored in structured JSON format

### v2.1 - Knowledge Graph (Previous Release)
- ✅ Interactive D3.js force-directed graph visualization
- ✅ Depth-controlled intelligent association crawling
- ✅ Multi-format graph export (PNG, SVG, JSON)

---

*This project has evolved from a simple bilingual search tool to a comprehensive multilingual knowledge corpus management system supporting 20+ languages.*

