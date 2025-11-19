import json
import requests
import uuid

url="http://localhost:8000/mcp"
PORT = 8000

def initialize_session():

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
    response = requests.post(url, json=payload, headers=header)
    data = response.json()
    session_id = data["result"]["sessionId"]
    if not session_id:
       return RuntimeError(f"Session ID not returned: {json.dumps(data, indent=2)}")
    else:
        print(session_id)
        return session_id
    