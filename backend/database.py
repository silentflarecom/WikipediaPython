import aiosqlite
import os
from datetime import datetime

DATABASE_FILE = "corpus.db"

async def init_database():
    """Initialize the database with required tables"""
    async with aiosqlite.connect(DATABASE_FILE) as db:
        # Create batch_tasks table
        await db.execute("""
            CREATE TABLE IF NOT EXISTS batch_tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                status TEXT NOT NULL,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                total_terms INTEGER NOT NULL,
                completed_terms INTEGER DEFAULT 0,
                failed_terms INTEGER DEFAULT 0,
                crawl_interval INTEGER DEFAULT 3
            )
        """)
        
        # Create terms table
        await db.execute("""
            CREATE TABLE IF NOT EXISTS terms (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                task_id INTEGER,
                term TEXT NOT NULL,
                status TEXT NOT NULL,
                en_summary TEXT,
                en_url TEXT,
                zh_summary TEXT,
                zh_url TEXT,
                error_message TEXT,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (task_id) REFERENCES batch_tasks(id)
            )
        """)
        
        # Create indexes
        await db.execute("""
            CREATE INDEX IF NOT EXISTS idx_task_id ON terms(task_id)
        """)
        
        await db.execute("""
            CREATE INDEX IF NOT EXISTS idx_status ON terms(status)
        """)
        
        await db.commit()

async def create_batch_task(total_terms: int, crawl_interval: int = 3) -> int:
    """Create a new batch task and return its ID"""
    async with aiosqlite.connect(DATABASE_FILE) as db:
        cursor = await db.execute("""
            INSERT INTO batch_tasks (status, total_terms, crawl_interval)
            VALUES (?, ?, ?)
        """, ("pending", total_terms, crawl_interval))
        await db.commit()
        return cursor.lastrowid

async def add_terms_to_task(task_id: int, terms: list):
    """Add terms to a batch task"""
    async with aiosqlite.connect(DATABASE_FILE) as db:
        await db.executemany("""
            INSERT INTO terms (task_id, term, status)
            VALUES (?, ?, ?)
        """, [(task_id, term, "pending") for term in terms])
        await db.commit()

async def update_task_status(task_id: int, status: str):
    """Update the status of a batch task"""
    async with aiosqlite.connect(DATABASE_FILE) as db:
        await db.execute("""
            UPDATE batch_tasks
            SET status = ?, updated_at = CURRENT_TIMESTAMP
            WHERE id = ?
        """, (status, task_id))
        await db.commit()

async def update_term_status(task_id: int, term: str, status: str, 
                            en_summary: str = None, en_url: str = None,
                            zh_summary: str = None, zh_url: str = None,
                            error_message: str = None):
    """Update the status and data of a term"""
    async with aiosqlite.connect(DATABASE_FILE) as db:
        await db.execute("""
            UPDATE terms
            SET status = ?, en_summary = ?, en_url = ?, zh_summary = ?, zh_url = ?,
                error_message = ?, updated_at = CURRENT_TIMESTAMP
            WHERE task_id = ? AND term = ?
        """, (status, en_summary, en_url, zh_summary, zh_url, error_message, task_id, term))
        await db.commit()

async def update_task_counters(task_id: int):
    """Update completed and failed counters for a task"""
    async with aiosqlite.connect(DATABASE_FILE) as db:
        cursor = await db.execute("""
            SELECT 
                COUNT(CASE WHEN status = 'completed' THEN 1 END) as completed,
                COUNT(CASE WHEN status = 'failed' THEN 1 END) as failed
            FROM terms
            WHERE task_id = ?
        """, (task_id,))
        row = await cursor.fetchone()
        
        if row:
            await db.execute("""
                UPDATE batch_tasks
                SET completed_terms = ?, failed_terms = ?, updated_at = CURRENT_TIMESTAMP
                WHERE id = ?
            """, (row[0], row[1], task_id))
            await db.commit()

async def get_task_status(task_id: int) -> dict:
    """Get the status of a batch task"""
    async with aiosqlite.connect(DATABASE_FILE) as db:
        db.row_factory = aiosqlite.Row
        cursor = await db.execute("""
            SELECT * FROM batch_tasks WHERE id = ?
        """, (task_id,))
        row = await cursor.fetchone()
        
        if row:
            return dict(row)
        return None

async def get_task_terms(task_id: int, status_filter: str = None) -> list:
    """Get all terms for a task, optionally filtered by status"""
    async with aiosqlite.connect(DATABASE_FILE) as db:
        db.row_factory = aiosqlite.Row
        
        if status_filter:
            cursor = await db.execute("""
                SELECT * FROM terms WHERE task_id = ? AND status = ?
                ORDER BY id
            """, (task_id, status_filter))
        else:
            cursor = await db.execute("""
                SELECT * FROM terms WHERE task_id = ?
                ORDER BY id
            """, (task_id,))
        
        rows = await cursor.fetchall()
        return [dict(row) for row in rows]

async def get_all_tasks() -> list:
    """Get all batch tasks"""
    async with aiosqlite.connect(DATABASE_FILE) as db:
        db.row_factory = aiosqlite.Row
        cursor = await db.execute("""
            SELECT * FROM batch_tasks
            ORDER BY created_at DESC
        """)
        rows = await cursor.fetchall()
        return [dict(row) for row in rows]

async def get_pending_terms(task_id: int) -> list:
    """Get all pending terms for a task"""
    return await get_task_terms(task_id, "pending")

async def get_failed_terms(task_id: int) -> list:
    """Get all failed terms for a task"""
    return await get_task_terms(task_id, "failed")
