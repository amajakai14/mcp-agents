"""
Basic MCP Server with Tools using FastMCP

This example demonstrates how to create MCP tools that LLMs can use.
Tools are functions that perform actions (similar to POST endpoints).
"""

from fastmcp import FastMCP
from typing import List
import json
import os
import datetime

# Create the FastMCP server instance
mcp = FastMCP("Demo Tools Server 🚀")

@mcp.tool
def add_numbers(a: int, b: int) -> int:
    """Add two numbers together."""
    return a + b

@mcp.tool
def multiply_numbers(a: float, b: float) -> float:
    """Multiply two numbers together."""
    return a * b

@mcp.tool
def get_current_time() -> str:
    """Get the current date and time."""
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

@mcp.tool
def create_file_content(filename: str, content: str) -> str:
    """Create a file with the specified content."""
    try:
        with open(filename, 'w') as f:
            f.write(content)
        return f"Successfully created file: {filename}"
    except Exception as e:
        return f"Error creating file: {str(e)}"

@mcp.tool
def list_files_in_directory(directory: str = ".") -> List[str]:
    """List all files in a given directory."""
    try:
        files = os.listdir(directory)
        return files
    except Exception as e:
        return [f"Error listing directory: {str(e)}"]

@mcp.tool
def calculate_factorial(n: int) -> int:
    """Calculate the factorial of a number."""
    if n < 0:
        raise ValueError("Factorial is not defined for negative numbers")
    if n == 0 or n == 1:
        return 1
    
    result = 1
    for i in range(2, n + 1):
        result *= i
    return result

@mcp.tool
def format_json(data: str) -> str:
    """Format a JSON string with proper indentation."""
    try:
        parsed = json.loads(data)
        return json.dumps(parsed, indent=2, sort_keys=True)
    except json.JSONDecodeError as e:
        return f"Invalid JSON: {str(e)}"

@mcp.tool
def word_count(text: str) -> dict:
    """Count words, characters, and lines in a text."""
    lines = text.split('\n')
    words = text.split()
    characters = len(text)
    
    return {
        "words": len(words),
        "characters": characters,
        "lines": len(lines),
        "characters_no_spaces": len(text.replace(' ', ''))
    }

if __name__ == "__main__":
    def main():
    """Main entry point for the MCP server."""
    print("Starting Basic MCP Tools Server...")
    print("Available tools:")
    for tool_name, tool_func in [
        ("add_numbers", add_numbers),
        ("multiply_numbers", multiply_numbers), 
        ("get_current_time", get_current_time),
        ("create_file_content", create_file_content),
        ("list_files_in_directory", list_files_in_directory),
        ("calculate_factorial", calculate_factorial),
        ("format_json", format_json),
        ("word_count", word_count)
    ]:
        doc = tool_func.__doc__ or "No description"
        print(f"- {tool_name}: {doc.strip()}")
    print()
    
    app.run()

# Run the server
if __name__ == "__main__":
    main()
