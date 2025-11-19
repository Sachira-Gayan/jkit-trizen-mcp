# client.py
import requests
import uuid
import json

SERVER_URL = "http://127.0.0.1:8000"

def initialize_session():
    """Send JSON-RPC request to initialize MCP session and get sessionId."""
    payload = {
        "jsonrpc": "2.0",
        "id": str(uuid.uuid4()),
        "method": "session/initialize",
        "params": {
            "clientInfo": {
                "name": "PythonMCPClient",
                "version": "1.0"
            },
            "protocolVersion": "2024-11-05"
        }
    }
    header= {
        "Content-Type": "application/json",
        # Required by FastMCP
        "Accept": "application/json, text/event-stream"
    }
    response = requests.post(SERVER_URL, json=payload, headers=header)
    data = response.json()

    # Check if server returned an error
    if "error" in data:
        raise RuntimeError(f"MCP server error: {json.dumps(data['error'], indent=2)}")

    # Extract sessionId
    session_id = data.get("result", {}).get("sessionId")
    if not session_id:
        raise RuntimeError(f"Session ID not returned: {json.dumps(data, indent=2)}")

    print("Session initialized. sessionId:", session_id)
    return session_id

def mcp_call_tool(session_id):
    """Send JSON-RPC request to MCP server."""
    payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "tools/list",
        "params": {"sessionId": session_id}
    }
    header= {
        "Content-Type": "application/json",
        # Required by FastMCP
        "Accept": "application/json, text/event-stream"
    }
    resp = requests.post(SERVER_URL, json=payload,headers=header)
    return resp.json()


if __name__ == "__main__":
   # Call the post_smartdata tool
    sessionid = initialize_session()
    print("🔹 Calling 'post_smartdata' tool...")
    result = mcp_call_tool(sessionid)
    print("Response:", json.dumps(result, indent=2)) 

   
