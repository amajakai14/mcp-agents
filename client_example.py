"""
MCP Client Example - How to connect to and use your MCP server

This shows how to connect to your MCP server from another Python application
or from LLM applications like Claude Desktop.
"""

import asyncio
from fastmcp import Client

async def test_mcp_server():
    """Test the MCP server by calling its tools."""
    # Connect to your local MCP server
    # When running, your server will be available at stdio or a specific URL
    
    print("Testing MCP Server Connection...")
    
    # Example of how a client would connect (when server is running)
    # async with Client("stdio:python advanced_mcp_server.py") as client:
    #     
    #     # Call a tool
    #     result = await client.call_tool(
    #         name="add_note",
    #         arguments={
    #             "title": "My First Note",
    #             "content": "This is a test note created via MCP",
    #             "tags": ["test", "mcp"]
    #         }
    #     )
    #     print(f"Tool result: {result}")
    #     
    #     # Get a resource
    #     resource = await client.get_resource("notes://all")
    #     print(f"Resource content: {resource}")
    #     
    #     # Get a prompt
    #     prompt = await client.get_prompt("note_summarizer", arguments={"note_ids": [1]})
    #     print(f"Generated prompt: {prompt}")
    
    print("Note: Uncomment the client code above when server is running")

# Claude Desktop Configuration
CLAUDE_CONFIG = {
    "mcpServers": {
        "mcp-agents": {
            "command": "python",
            "args": ["/Users/means/repository/mcp-agents/advanced_mcp_server.py"],
            "env": {}
        }
    }
}

if __name__ == "__main__":
    print("MCP Client Configuration Example")
    print("=" * 50)
    print()
    print("To use with Claude Desktop, add this to your config:")
    print(CLAUDE_CONFIG)
    print()
    asyncio.run(test_mcp_server())
