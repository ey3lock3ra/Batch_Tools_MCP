# uvicorn mcp:app --host 0.0.0.0 --port 8000 --reload
from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
from typing import Dict, Any
import json

app = FastAPI()

@app.get("/tools")
def list_tools():
    """Expose tools for discovery."""

    with open("tools_documentation/tools_schema.json", "r") as f:
        tools = json.load(f)

    return {"tools": [{'tool_name': tool_data['tool_name'], 'description': tool_data['description']} for tool_data in tools.values()]}

@app.get("/tool/{tool_name}")
async def invoke_tool(tool_name: str):
    """Run a specific tool given its name and user input."""

    if tool_name is None:
        raise HTTPException(status_code=404, detail="Tool not found")

    with open('tools_documentation/tools_schema.json', 'r') as f:
        data = json.load(f)

    tool_data = data.get(tool_name)
    if tool_data is None:
        raise HTTPException(status_code=404, detail=f"Tool '{tool_name}' not found")
    
    return tool_data