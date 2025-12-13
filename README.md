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
