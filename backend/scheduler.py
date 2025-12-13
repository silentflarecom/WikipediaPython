import asyncio
import wikipediaapi
from typing import Dict, Callable
from database import (
    update_task_status, 
    update_term_status, 
    update_task_counters,
    get_pending_terms,
    get_task_status
)

# Global dictionary to track running tasks
running_tasks: Dict[int, asyncio.Task] = {}

class BatchCrawler:
    def __init__(self, task_id: int, crawl_interval: int = 3):
        self.task_id = task_id
        self.crawl_interval = crawl_interval
        self.should_stop = False
        
        # Initialize Wikipedia API instances
        self.wiki_en = wikipediaapi.Wikipedia(
            user_agent='TermCorpusGenerator/1.0 (contact@example.com)',
            language='en'
        )
        self.wiki_zh = wikipediaapi.Wikipedia(
            user_agent='TermCorpusGenerator/1.0 (contact@example.com)',
            language='zh'
        )
    
    async def crawl_single_term(self, term: str) -> Dict:
        """Crawl a single term from Wikipedia"""
        try:
            # Mark as crawling
            await update_term_status(self.task_id, term, "crawling")
            
            # Get English page (synchronous call, but shouldn't block too long)
            await asyncio.sleep(0)  # Yield control
            page_en = self.wiki_en.page(term)
            
            if not page_en.exists():
                raise Exception(f"Term '{term}' not found in English Wikipedia")
            
            # Get English data
            en_summary = page_en.summary[0:1000] + "..." if len(page_en.summary) > 1000 else page_en.summary
            en_url = page_en.fullurl
            
            # Get Chinese data via langlinks
            zh_summary = "Translation not found."
            zh_url = ""
            
            langlinks = page_en.langlinks
            if 'zh' in langlinks:
                zh_title = langlinks['zh'].title
                page_zh = self.wiki_zh.page(zh_title)
                
                if page_zh.exists():
                    zh_summary = page_zh.summary[0:1000] + "..." if len(page_zh.summary) > 1000 else page_zh.summary
                    zh_url = page_zh.fullurl
            
            result = {
                "term": term,
                "en_summary": en_summary,
                "en_url": en_url,
                "zh_summary": zh_summary,
                "zh_url": zh_url
            }
            
            # Save to Markdown
            await self.save_to_markdown(result)
            
            # Update database with success
            await update_term_status(
                self.task_id, term, "completed",
                en_summary, en_url, zh_summary, zh_url
            )
            
            return result
            
        except Exception as e:
            # Update database with failure
            error_msg = str(e)
            await update_term_status(
                self.task_id, term, "failed",
                error_message=error_msg
            )
            raise e
    
    async def save_to_markdown(self, result: Dict):
        """Save result to Markdown file"""
        import os
        
        OUTPUT_DIR = "output"
        os.makedirs(OUTPUT_DIR, exist_ok=True)
        
        filename = f"{result['term'].replace(' ', '_')}.md"
        filepath = os.path.join(OUTPUT_DIR, filename)
        
        try:
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(f"# {result['term']}\n\n")
                f.write(f"## English\n{result['en_summary']}\n\n[Link]({result['en_url']})\n\n")
                f.write(f"## Chinese\n{result['zh_summary']}\n\n")
                if result['zh_url']:
                    f.write(f"[Link]({result['zh_url']})\n")
        except Exception as e:
            print(f"Error saving Markdown file: {e}")
    
    async def run(self):
        """Run the batch crawling process"""
        try:
            # Update task status to running
            await update_task_status(self.task_id, "running")
            
            # Get all pending terms
            pending_terms = await get_pending_terms(self.task_id)
            
            for term_record in pending_terms:
                if self.should_stop:
                    await update_task_status(self.task_id, "cancelled")
                    break
                
                term = term_record['term']
                
                try:
                    await self.crawl_single_term(term)
                    print(f"✓ Successfully crawled: {term}")
                except Exception as e:
                    print(f"✗ Failed to crawl {term}: {str(e)}")
                
                # Update task counters
                await update_task_counters(self.task_id)
                
                # Wait for the specified interval before next request
                if term_record != pending_terms[-1]:  # Don't wait after the last term
                    await asyncio.sleep(self.crawl_interval)
            
            # Mark task as completed if not cancelled
            if not self.should_stop:
                await update_task_status(self.task_id, "completed")
                print(f"✓ Task {self.task_id} completed successfully")
        
        except Exception as e:
            print(f"✗ Error in batch crawler: {str(e)}")
            await update_task_status(self.task_id, "failed")
        
        finally:
            # Remove from running tasks
            if self.task_id in running_tasks:
                del running_tasks[self.task_id]
    
    def stop(self):
        """Signal the crawler to stop"""
        self.should_stop = True


async def start_batch_crawl(task_id: int, crawl_interval: int = 3):
    """Start a batch crawl task in the background"""
    if task_id in running_tasks:
        raise Exception(f"Task {task_id} is already running")
    
    crawler = BatchCrawler(task_id, crawl_interval)
    task = asyncio.create_task(crawler.run())
    running_tasks[task_id] = task
    
    return crawler


async def cancel_batch_crawl(task_id: int):
    """Cancel a running batch crawl task"""
    if task_id not in running_tasks:
        raise Exception(f"Task {task_id} is not running")
    
    task = running_tasks[task_id]
    task.cancel()
    
    try:
        await task
    except asyncio.CancelledError:
        pass
    
    await update_task_status(task_id, "cancelled")


async def retry_failed_terms(task_id: int, crawl_interval: int = 3):
    """Retry all failed terms in a task"""
    # Reset failed terms to pending
    from database import get_failed_terms
    import aiosqlite
    
    failed_terms = await get_failed_terms(task_id)
    
    if not failed_terms:
        return 0
    
    async with aiosqlite.connect("corpus.db") as db:
        for term_record in failed_terms:
            await db.execute("""
                UPDATE terms
                SET status = 'pending', error_message = NULL, updated_at = CURRENT_TIMESTAMP
                WHERE id = ?
            """, (term_record['id'],))
        await db.commit()
    
    # Start crawling again
    await start_batch_crawl(task_id, crawl_interval)
    
    return len(failed_terms)
