import uuid
import requests
import json
from msal import ConfidentialClientApplication

MCP_SERVER_URL = "http://localhost:8000/mcp"   # Change if deployed on Azure




TENANT_ID = "704e1a5a-f6a7-4fae-be42-e1a81a3412e7"
CLIENT_ID = "f659c2ba-4303-48be-bc57-8a6427b6f237"
REDIRECT_URI = "http://localhost:8000/mcp"


CLIENT_ID = "029a88ac-a2a7-48dc-999a-e48cee57866d"
CLIENT_SECRET = "zNp8Q~dMQ5cvIFdiMLHn2ojDZAJaTLPt1~qqwaf2"
TENANT_ID = "f6bf0d68-8c3c-4a25-a5d8-661cec987ce2"
AUTHORITY = f"https://login.microsoftonline.com/{TENANT_ID}"
SCOPE = ["https://graph.microsoft.com/.default"]  # or your API scope

result = None 

def get_accessToken():


    app = ConfidentialClientApplication(
    client_id=CLIENT_ID,
    client_credential=CLIENT_SECRET,
    authority=AUTHORITY
    )

# Acquire token
    result = app.acquire_token_for_client(scopes=SCOPE)

    if "access_token" in result:
        access_token = result["access_token"]
        return access_token # print partial for debug

    
    
    else:
        return("Error acquiring token:", result.get("error_description"))
    
    

# ----------------------------
# JSON-RPC Helper
# ----------------------------
def rpc_call(method: str, params: dict = None):
    body = {
        "jsonrpc": "2.0",
        "id": str(uuid.uuid4()),
        "method": method,
        "params": params
    }

    response = requests.post(
        MCP_SERVER_URL,
        json=body,
        headers={"Accept": "application/json,text/event-stream"}
    )

    
    result = response.json()

    if "error" in result:
        raise Exception(f"MCP Error: {result['error']}")

    return result


# ----------------------------
# 1. Initialize Session
# ----------------------------
def initialize_session():
    params = {
        "clientInfo": {"name": "PythonMCPClient", "version": "1.0"},
        "protocolVersion": "2024-11-05"
    }

    result = rpc_call("session/initialize", params)
    return result


# ----------------------------
# 2. List Tools
# ----------------------------
def list_tools():
    
    result = rpc_call("tools/list")

    for t in result["result"]["tools"]:
        print("  -", t["name"])
    return result


# ----------------------------
# 3. Call MCP Tool
# ----------------------------
def call_tool(tool_name: str, arguments: dict = None):
    params = {
        "name": tool_name,
        "arguments": arguments 
    }

    result = rpc_call("tools/call", params)

    output = result["result"]["tool"]["output"]
    return output


# ----------------------------
# MAIN EXECUTION
# ----------------------------
if __name__ == "__main__":


    call_tool(
        "get_device_list",
        {
            "url": "https://api3.hilife.sg/hilife_v3/smarthome/device/list",
            "data": {"hilifeUnit": "Tri-Zen Residencies2Block4608Unit"}
        }
    )

    
