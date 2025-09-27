"""
Advanced MCP Server demonstrating Tools, Resources, and Prompts

This example shows more advanced MCP features:
- Tools: Functions that perform actions
- Resources: Data that can be loaded into LLM context  
- Prompts: Reusable templates for LLM interactions
"""

from fastmcp import FastMCP
from fastmcp.resources import InMemoryResource
from fastmcp.prompts import Prompt
from typing import List, Dict, Any
import json
import sqlite3
import os
import tempfile

# Create the FastMCP server instance
mcp = FastMCP("Advanced MCP Server 🔥")

# In-memory storage for demo purposes
notes_db = []
todo_list = []

# =============================================================================
# TOOLS - Functions that perform actions
# =============================================================================

@mcp.tool
def add_note(title: str, content: str, tags: List[str] = None) -> Dict[str, Any]:
    """Add a new note to the notes database."""
    if tags is None:
        tags = []
    
    note = {
        "id": len(notes_db) + 1,
        "title": title,
        "content": content,
        "tags": tags,
        "created_at": "2025-09-27"  # In real app, use datetime.now()
    }
    notes_db.append(note)
    return {"status": "success", "note_id": note["id"], "message": f"Note '{title}' added successfully"}

@mcp.tool
def search_notes(query: str) -> List[Dict[str, Any]]:
    """Search notes by title, content, or tags."""
    results = []
    query_lower = query.lower()
    
    for note in notes_db:
        if (query_lower in note["title"].lower() or 
            query_lower in note["content"].lower() or 
            any(query_lower in tag.lower() for tag in note["tags"])):
            results.append(note)
    
    return results

@mcp.tool
def add_todo(task: str, priority: str = "medium") -> Dict[str, Any]:
    """Add a new task to the todo list."""
    if priority not in ["low", "medium", "high"]:
        return {"status": "error", "message": "Priority must be low, medium, or high"}
    
    todo = {
        "id": len(todo_list) + 1,
        "task": task,
        "priority": priority,
        "completed": False,
        "created_at": "2025-09-27"
    }
    todo_list.append(todo)
    return {"status": "success", "todo_id": todo["id"], "message": f"Task added: {task}"}

@mcp.tool
def complete_todo(todo_id: int) -> Dict[str, Any]:
    """Mark a todo item as completed."""
    for todo in todo_list:
        if todo["id"] == todo_id:
            todo["completed"] = True
            return {"status": "success", "message": f"Task {todo_id} marked as completed"}
    
    return {"status": "error", "message": f"Todo with id {todo_id} not found"}

@mcp.tool
def create_database_table(table_name: str, columns: Dict[str, str]) -> Dict[str, Any]:
    """Create a SQLite table with specified columns."""
    try:
        # Create a temporary database for demo
        db_path = tempfile.mktemp(suffix='.db')
        conn = sqlite3.connect(db_path)
        
        # Build CREATE TABLE statement
        column_defs = [f"{name} {data_type}" for name, data_type in columns.items()]
        create_sql = f"CREATE TABLE {table_name} ({', '.join(column_defs)})"
        
        conn.execute(create_sql)
        conn.commit()
        conn.close()
        
        return {
            "status": "success", 
            "message": f"Table '{table_name}' created successfully",
            "db_path": db_path,
            "sql": create_sql
        }
    except Exception as e:
        return {"status": "error", "message": f"Error creating table: {str(e)}"}

# =============================================================================
# RESOURCES - Data that can be loaded into LLM context
# =============================================================================

@mcp.resource("notes://all")
def get_all_notes() -> str:
    """Get all notes as a formatted text resource."""
    if not notes_db:
        return "No notes available."
    
    content = "# All Notes\n\n"
    for note in notes_db:
        content += f"## {note['title']} (ID: {note['id']})\n"
        content += f"**Tags:** {', '.join(note['tags']) if note['tags'] else 'None'}\n"
        content += f"**Created:** {note['created_at']}\n\n"
        content += f"{note['content']}\n\n"
        content += "---\n\n"
    
    return content

@mcp.resource("todos://pending")
def get_pending_todos() -> str:
    """Get all pending todo items as a formatted resource."""
    pending = [todo for todo in todo_list if not todo["completed"]]
    
    if not pending:
        return "No pending tasks."
    
    content = "# Pending Tasks\n\n"
    for todo in pending:
        content += f"- **{todo['task']}** (Priority: {todo['priority']}, ID: {todo['id']})\n"
    
    return content

@mcp.resource("system://stats")
def get_system_stats() -> str:
    """Get system statistics as a formatted resource."""
    completed_todos = len([t for t in todo_list if t["completed"]])
    pending_todos = len([t for t in todo_list if not t["completed"]])
    
    return f"""# System Statistics

## Notes
- Total notes: {len(notes_db)}
- Total tags used: {len(set(tag for note in notes_db for tag in note['tags']))}

## Todos  
- Completed tasks: {completed_todos}
- Pending tasks: {pending_todos}
- Total tasks: {len(todo_list)}

## Server Info
- Server name: Advanced MCP Server 🔥
- Available tools: {len(mcp._tools)}
- Available resources: {len(mcp._resources)}
"""

# =============================================================================
# PROMPTS - Reusable templates for LLM interactions
# =============================================================================

@mcp.prompt
def note_summarizer(note_ids: List[int]) -> str:
    """Generate a prompt to summarize specific notes."""
    if not note_ids:
        return "Please provide note IDs to summarize."
    
    notes_content = []
    for note_id in note_ids:
        note = next((n for n in notes_db if n["id"] == note_id), None)
        if note:
            notes_content.append(f"Note {note_id}: {note['title']}\n{note['content']}")
    
    if not notes_content:
        return "No valid notes found for the provided IDs."
    
    return f"""Please summarize the following notes:

{chr(10).join(notes_content)}

Provide a concise summary highlighting the key points from each note."""

@mcp.prompt  
def task_prioritizer() -> str:
    """Generate a prompt to help prioritize pending tasks."""
    pending = [todo for todo in todo_list if not todo["completed"]]
    
    if not pending:
        return "No pending tasks to prioritize."
    
    tasks_list = "\n".join([f"- {todo['task']} (Current priority: {todo['priority']})" 
                           for todo in pending])
    
    return f"""Help me prioritize these pending tasks:

{tasks_list}

Please suggest:
1. Which tasks should be high priority and why
2. Which tasks can be deferred  
3. Any tasks that could be combined or broken down
4. Recommended order of execution"""

def main():
    """Main entry point for the advanced MCP server."""
    print("Starting Advanced MCP Server...")
    print("\nAvailable Tools:")
    print("- add_note: Add a new note")
    print("- search_notes: Search through notes")
    print("- add_todo: Add a todo item")
    print("- complete_todo: Mark a todo as completed")
    print("- create_database_table: Create a SQLite table")
    
    print("\nAvailable Resources:")
    print("- notes://all: Get all notes")
    print("- todos://pending: Get pending todos") 
    print("- system://stats: Get system statistics")
    
    print("\nAvailable Prompts:")
    print("- note_summarizer: Generate summary prompt for notes")
    print("- task_prioritizer: Generate task prioritization prompt")
    
    mcp.run()

if __name__ == "__main__":
    main()
