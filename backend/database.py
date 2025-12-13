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
        
        # Create term_associations table
        await db.execute("""
            CREATE TABLE IF NOT EXISTS term_associations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                source_term_id INTEGER,
                target_term TEXT,
                association_type TEXT,
                weight REAL DEFAULT 1.0,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (source_term_id) REFERENCES terms(id)
            )
        """)

        # Add columns to existing tables if they don't exist
        # We use a helper to add columns safely
        await add_column_if_not_exists(db, "batch_tasks", "max_depth", "INTEGER DEFAULT 1")
        await add_column_if_not_exists(db, "terms", "depth_level", "INTEGER DEFAULT 0")
        await add_column_if_not_exists(db, "terms", "source_term_id", "INTEGER")
        
        # Create indexes
        await db.execute("""
            CREATE INDEX IF NOT EXISTS idx_task_id ON terms(task_id)
        """)
        
        await db.execute("""
            CREATE INDEX IF NOT EXISTS idx_status ON terms(status)
        """)
        
        await db.execute("""
            CREATE INDEX IF NOT EXISTS idx_source_term ON term_associations(source_term_id)
        """)
        
        await db.commit()

async def add_column_if_not_exists(db, table, column, definition):
    """Helper to add a column if it doesn't already exist"""
    try:
        await db.execute(f"ALTER TABLE {table} ADD COLUMN {column} {definition}")
        print(f"Added column {column} to {table}")
    except Exception as e:
        # Ignore error if column already exists
        pass

async def create_batch_task(total_terms: int, crawl_interval: int = 3, max_depth: int = 1) -> int:
    """Create a new batch task and return its ID"""
    async with aiosqlite.connect(DATABASE_FILE) as db:
        cursor = await db.execute("""
            INSERT INTO batch_tasks (status, total_terms, crawl_interval, max_depth)
            VALUES (?, ?, ?, ?)
        """, ("pending", total_terms, crawl_interval, max_depth))
        await db.commit()
        return cursor.lastrowid

async def add_terms_to_task(task_id: int, terms: list, depth_level: int = 0, source_term_id: int = None):
    """Add terms to a batch task"""
    async with aiosqlite.connect(DATABASE_FILE) as db:
        await db.executemany("""
            INSERT INTO terms (task_id, term, status, depth_level, source_term_id)
            VALUES (?, ?, ?, ?, ?)
        """, [(task_id, term, "pending", depth_level, source_term_id) for term in terms])
        # Update total terms count in batch_tasks
        if depth_level > 0:
            await db.execute("""
                UPDATE batch_tasks 
                SET total_terms = total_terms + ? 
                WHERE id = ?
            """, (len(terms), task_id))
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

async def save_term_associations(source_term_id: int, associations: list):
    """Save associations for a term
    associations: list of dicts with keys 'target_term', 'association_type', 'weight'
    """
    async with aiosqlite.connect(DATABASE_FILE) as db:
        await db.executemany("""
            INSERT INTO term_associations (source_term_id, target_term, association_type, weight)
            VALUES (?, ?, ?, ?)
        """, [(source_term_id, a['target_term'], a['association_type'], a.get('weight', 1.0)) for a in associations])
        await db.commit()

async def get_term_associations(term_id: int) -> list:
    """Get all associations for a term"""
    async with aiosqlite.connect(DATABASE_FILE) as db:
        db.row_factory = aiosqlite.Row
        cursor = await db.execute("""
            SELECT * FROM term_associations WHERE source_term_id = ?
        """, (term_id,))
        rows = await cursor.fetchall()
        return [dict(row) for row in rows]
