# MCP Agents 🚀

FastMCP-based Model Context Protocol servers providing various tools, resources, and prompts for AI assistants.

## Quick Start with uvx

The easiest way to run these MCP servers is using `uvx` (recommended):

```bash
# Run the default basic server
uvx @amajakai14/mcp-agents

# Or run specific servers
uvx @amajakai14/mcp-agents --script mcp-basic-server
uvx @amajakai14/mcp-agents --script mcp-advanced-server
```

## What is MCP?

The Model Context Protocol (MCP) is a standardized way to connect LLMs to tools and data. It provides:

- **Tools**: Functions that LLMs can call to perform actions (like API endpoints)
- **Resources**: Data that can be loaded into LLM context 
- **Prompts**: Reusable templates for LLM interactions

## Installation Options

### Option 1: Using uvx (Recommended)
```bash
# Install uvx if you haven't already
pip install uvx

# Run the default server
uvx @amajakai14/mcp-agents

# Or run specific servers
uvx @amajakai14/mcp-agents --script mcp-basic-server
uvx @amajakai14/mcp-agents --script mcp-advanced-server
```

### Option 2: Clone and Run Locally
```bash
# Clone the repository
git clone https://github.com/amajakai14/mcp-agents.git
cd mcp-agents

# Install dependencies
pip3 install -r requirements.txt

# Run the servers
python3 basic_mcp_server.py
python3 advanced_mcp_server.py
```

### Option 3: Install from PyPI (Future)
```bash
pip install mcp-agents
mcp-agents  # Run default server
mcp-basic-server    # Run basic server
mcp-advanced-server # Run advanced server
```

### Running the Servers

## Publishing to PyPI

To publish this package to PyPI so users can use `uvx @amajakai14/mcp-agents`:

1. **Build the package:**
   ```bash
   pip install build twine
   python -m build
   ```

2. **Upload to PyPI:**
   ```bash
   twine upload dist/*
   ```

3. **Or use GitHub Actions:** Create a release on GitHub and the workflow will automatically publish to PyPI.

## Testing Your MCP Server

1. **Run the basic server**:
   ```bash
   python3 basic_mcp_server.py
   ```

2. **Run the advanced server**:
   ```bash
   python3 advanced_mcp_server.py
   ```

## Available Servers

### Basic MCP Server (`basic_mcp_server.py`)

A simple server demonstrating fundamental MCP tools:

- `add_numbers(a, b)` - Add two numbers
- `multiply_numbers(a, b)` - Multiply two numbers  
- `get_current_time()` - Get current timestamp
- `create_file_content(filename, content)` - Create a file
- `list_files_in_directory(directory)` - List directory contents
- `calculate_factorial(n)` - Calculate factorial
- `format_json(data)` - Format JSON with indentation
- `word_count(text)` - Count words, characters, and lines

### Advanced MCP Server (`advanced_mcp_server.py`)

A comprehensive server showing tools, resources, and prompts:

**Tools:**
- `add_note(title, content, tags)` - Add a note
- `search_notes(query)` - Search through notes
- `add_todo(task, priority)` - Add a todo item
- `complete_todo(todo_id)` - Mark todo as completed
- `create_database_table(table_name, columns)` - Create SQLite table

**Resources:**
- `notes://all` - Get all notes as formatted text
- `todos://pending` - Get pending todo items
- `system://stats` - Get system statistics

**Prompts:**
- `note_summarizer(note_ids)` - Generate note summary prompt
- `task_prioritizer()` - Generate task prioritization prompt

## Using with LLM Applications

### Claude Desktop

Add this to your Claude Desktop configuration:

### Claude Desktop

Add this to your Claude Desktop configuration:

**Simple Configuration (Default - Basic Server):**
```json
{
  "mcpServers": {
    "mcp-agents": {
      "command": "uvx",
      "args": ["@amajakai14/mcp-agents"]
    }
  }
}
```

**Multiple Servers Configuration:**
```json
{
  "mcpServers": {
    "mcp-basic": {
      "command": "uvx",
      "args": ["@amajakai14/mcp-agents", "--script", "mcp-basic-server"]
    },
    "mcp-advanced": {
      "command": "uvx", 
      "args": ["@amajakai14/mcp-agents", "--script", "mcp-advanced-server"]
    }
  }
}
```

**For local installation:**
```json
{
  "mcpServers": {
    "mcp-agents": {
      "command": "python3",
      "args": ["/path/to/your/advanced_mcp_server.py"],
      "env": {}
    }
  }
}
```

### Other MCP Clients

See `client_example.py` for programmatic usage examples.

## Creating Your Own MCP Tools

Here's the basic pattern for creating MCP tools with FastMCP:

```python
from fastmcp import FastMCP

# Create server instance
mcp = FastMCP("My Server")

# Add a tool (function LLMs can call)
@mcp.tool
def my_tool(param1: str, param2: int) -> str:
    """Description of what this tool does."""
    return f"Processed {param1} with {param2}"

# Add a resource (data LLMs can access)
@mcp.resource("data://my-resource")
def my_resource() -> str:
    """Get some data."""
    return "This is my resource data"

# Add a prompt template
@mcp.prompt
def my_prompt(context: str) -> str:
    """Generate a prompt template."""
    return f"Please analyze this: {context}"

# Run the server
if __name__ == "__main__":
    mcp.run()
```

## Key Concepts

### Tools vs Resources vs Prompts

- **Tools**: Use `@mcp.tool` for functions that *do something* (create, update, calculate, etc.)
- **Resources**: Use `@mcp.resource("uri")` for functions that *provide data* (read, fetch, list, etc.)  
- **Prompts**: Use `@mcp.prompt` for functions that *generate prompt templates*

### Type Hints

Always use type hints - FastMCP uses them to generate proper schemas:

```python
@mcp.tool
def my_tool(text: str, count: int = 1) -> List[str]:
    """Tool with proper type hints."""
    return [text] * count
```

### Error Handling

Handle errors gracefully in your tools:

```python
@mcp.tool
def safe_tool(data: str) -> Dict[str, Any]:
    """A tool with proper error handling."""
    try:
        result = process_data(data)
        return {"status": "success", "result": result}
    except Exception as e:
        return {"status": "error", "message": str(e)}
```

## Deployment

### Local Development
```bash
python your_server.py
```

### FastMCP Cloud (Free)
Deploy to [FastMCP Cloud](https://fastmcp.cloud/) for free hosting.

### Custom Infrastructure
Use the built-in FastMCP deployment tools for your own servers.

## Learn More

- [FastMCP Documentation](https://gofastmcp.com)
- [MCP Specification](https://modelcontextprotocol.io)
- [FastMCP Examples](https://github.com/jlowin/fastmcp)
