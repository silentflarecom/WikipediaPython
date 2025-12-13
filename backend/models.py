from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class TermResponse(BaseModel):
    term: str
    en_summary: str
    en_url: str
    zh_summary: str
    zh_url: str

class BatchTaskCreate(BaseModel):
    terms: List[str]
    crawl_interval: int = 3

class BatchTaskResponse(BaseModel):
    task_id: int
    total_terms: int
    message: str

class TaskStatus(BaseModel):
    task_id: int
    status: str
    total_terms: int
    completed_terms: int
    failed_terms: int
    progress_percent: float
    created_at: str
    updated_at: str

class TermDetail(BaseModel):
    id: int
    task_id: int
    term: str
    status: str
    en_summary: Optional[str] = None
    en_url: Optional[str] = None
    zh_summary: Optional[str] = None
    zh_url: Optional[str] = None
    error_message: Optional[str] = None
    created_at: str
    updated_at: str

class TaskListItem(BaseModel):
    id: int
    status: str
    total_terms: int
    completed_terms: int
    failed_terms: int
    created_at: str
