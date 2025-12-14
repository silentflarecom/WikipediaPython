# Setup Instructions

## First-Time Setup

### 1. Install Dependencies

**Backend:**
```bash
cd backend
pip install -r requirements.txt
```

**Frontend:**
```bash
cd frontend
npm install
```

### 2. Configure User-Agent

⚠️ **IMPORTANT**: Before running the application, you MUST configure your own User-Agent to comply with Wikipedia's policies.

Wikipedia requires all API users to identify themselves with a User-Agent string that includes:
- Your project/bot name
- Contact information (email or GitHub URL)

**How to set your User-Agent:**

1. Start the application (see Running the Application below)
2. Navigate to the **Manage** page in the UI
3. Find the **System Configuration** section
4. Update the **User Agent** field with your information:
   ```
   YourProjectName/1.0 (your-email@example.com)
   ```
   or
   ```
   YourProjectName/1.0 (https://github.com/YourUsername/YourRepo)
   ```
5. Click **Save Settings**

**Why this matters:**
- Wikipedia can contact you if there are issues with your requests
- It helps Wikipedia track API usage patterns
- It's required by [Wikipedia's User-Agent Policy](https://meta.wikimedia.org/wiki/User-Agent_policy)

### 3. Running the Application

**Start Backend:**
```bash
cd backend
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

**Start Frontend:**
```bash
cd frontend
npm run dev
```

**Access the application:**
- Frontend: http://localhost:5173
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

## Project Structure

```
WikipediaPython/
├── backend/
│   ├── main.py           # FastAPI application
│   ├── database.py       # Database operations
│   ├── scheduler.py      # Batch crawling logic
│   ├── models.py         # Pydantic models
│   └── requirements.txt  # Python dependencies
├── frontend/
│   └── src/
│       ├── App.vue
│       └── components/
│           ├── BatchImport.vue
│           ├── TaskManager.vue
│           ├── ResultsTable.vue
│           └── ...
└── README.md
```

## Privacy & Data

- The database file (`corpus.db`) is gitignored by default
- No personal data is collected or transmitted
- All Wikipedia API requests use your configured User-Agent
- You can export and backup your data anytime via the Manage page

## Support

For issues or questions:
1. Check the [main README](README.md) for feature documentation
2. Review [Wikipedia's API documentation](https://www.mediawiki.org/wiki/API:Main_page)
3. Open an issue on GitHub

---

**Note**: This is an educational project. Please use it responsibly and in compliance with Wikipedia's policies.
