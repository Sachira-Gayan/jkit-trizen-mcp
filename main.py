
from http.server import BaseHTTPRequestHandler, HTTPServer
import socketserver
import json
import uuid
import threading
import time
import requests
from config import header

HOST = "0.0.0.0"
PORT = 8080

# Simple in-memory session store: session_id -> metadata
_sessions = {}
_sessions_lock = threading.Lock()

# Tool registry: method name -> callable
_tool_registry = {}

def tool(name):
    """Decorator to register a tool handler"""
    def decorator(fn):
        _tool_registry[name] = fn
        return fn
    return decorator

def make_json_response(result=None, error=None, id=None):
    resp = {"jsonrpc": "2.0"}
    if error is not None:
        resp["error"] = error
    else:
        resp["result"] = result
    resp["id"] = id
    return json.dumps(resp).encode("utf-8")

class ThreadedHTTPServer(socketserver.ThreadingMixIn, HTTPServer):
    daemon_threads = True

class MCPHandler(BaseHTTPRequestHandler):
    protocol_version = "HTTP/1.1"

    def _read_json(self):
        length = int(self.headers.get("Content-Length", 0))
        if length == 0:
            return None, "Empty body"
        raw = self.rfile.read(length)
        try:
            data = json.loads(raw.decode("utf-8"))
            return data, None
        except Exception as e:
            return None, f"Invalid JSON: {e}"

    def _send_json(self, payload, status=200):
        body = payload if isinstance(payload, (bytes,bytearray)) else json.dumps(payload).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_POST(self):
        request_json, err = self._read_json()
        if err:
            resp = make_json_response(error={"code": -32700, "message": err}, id=None)
            return self._send_json(resp, status=400)

        # Basic JSON-RPC fields
        method = request_json.get("method")
        req_id = request_json.get("id")
        params = request_json.get("params", {})

        # Dispatch core MCP methods
        if method == "session/initialize":
            client_info = params.get("clientInfo", {})
            protocol = params.get("protocolVersion", "1.0")
            session_id = str(uuid.uuid4())
            now = time.time()
            with _sessions_lock:
                _sessions[session_id] = {
                    "clientInfo": client_info,
                    "protocolVersion": protocol,
                    "created": now,
                    "lastSeen": now,
                }
            result = {
                "sessionId": session_id,
                "serverVersion": "minimal-mcp/0.1",
                "protocolVersion": protocol,
            }
            return self._send_json(make_json_response(result=result, id=req_id))

        if method == "session/terminate":
            session_id = params.get("sessionId")
            if not session_id:
                return self._send_json(make_json_response(error={"code": -32602, "message": "Missing sessionId"}, id=req_id), status=400)
            with _sessions_lock:
                popped = _sessions.pop(session_id, None)
            if popped is None:
                return self._send_json(make_json_response(error={"code": -32000, "message": "Unknown sessionId"}, id=req_id), status=404)
            return self._send_json(make_json_response(result={"terminated": True}, id=req_id))

        # Tool invocation: method names like "tool/mytool"
        if method and method.startswith("tool/"):
            tool_name = method.split("/", 1)[1]
            handler = _tool_registry.get(tool_name)
            if handler is None:
                return self._send_json(make_json_response(error={"code": -32601, "message": f"Tool '{tool_name}' not found"}, id=req_id), status=404)

            # Optionally validate session
            session_id = params.get("sessionId")
            if session_id:
                with _sessions_lock:
                    sess = _sessions.get(session_id)
                    if not sess:
                        return self._send_json(make_json_response(error={"code": -32000, "message": "Invalid sessionId"}, id=req_id), status=400)
                    sess["lastSeen"] = time.time()

            try:
                # call tool handler with params dict
                result = handler(params)
                return self._send_json(make_json_response(result=result, id=req_id))
            except Exception as e:
                return self._send_json(make_json_response(error={"code": -32001, "message": f"Tool error: {e}"}, id=req_id), status=500)

        # Unknown method
        return self._send_json(make_json_response(error={"code": -32601, "message": "Method not found"}, id=req_id), status=404)

    def log_message(self, format, *args):
        # Simple logging override to include thread name
        print("[%s] %s - - %s" % (threading.current_thread().name, self.client_address[0], format%args))

# Example tools
@tool("echo")
def tool_echo(params):
    # returns whatever was passed (safe for testing)
    return {"echo": params.get("message", ""), "receivedParams": params}

@tool("sum")
def tool_sum(params):
    numbers = params.get("numbers")
    if not isinstance(numbers, list):
        raise ValueError("numbers must be a list")
    total = 0
    for n in numbers:
        total += float(n)
    return {"sum": total}

@tool("get_device_list")
def get_device_list(params):
    url = params.get("url")
    data=params.get("data")
    response = requests.post(url, json=data,headers=header)
    response.raise_for_status()
    if response.status_code == 200:
        return {"content" : response.json()}
    else:
        return {"Error": "API call failed with status code", "StatusCode" : {response.status_code}}
    

def run_server(host=HOST, port=PORT):
    print(f"Starting minimal MCP server on {host}:{port}")
    server = ThreadedHTTPServer((host, port), MCPHandler)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("Shutting down...")
        server.shutdown()

if __name__ == "__main__":
    run_server()


