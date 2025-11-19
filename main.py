from fastmcp import FastMCP
from config import header
import requests
from Auth import get_accessToken

app = FastMCP("http-client-server",stateless_http=True)

# ------------------------------
# HTTP GET Tool
# ------------------------------
result = None
@app.tool
async def get_token() -> dict:
    
    result=get_accessToken()
    return {"result":{result}}
 
    

@app.tool()
async def http_get(url: str) -> dict:
    """
    Perform an HTTP GET request and return the response text.
    """
  
    response = requests.get(url)
         
    if response.status_code == 200:
        return response.json()
    else :
         return {"Error": "API call failed with status code", "StatusCode" : {response.status_code}}


# ------------------------------
# HTTP POST Tool
# ------------------------------
@app.tool()
async def get_device_list(url: str, data: dict) -> dict:
    """
    Perform an HTTP POST request with JSON body.
    """
    
    
        
    response = requests.post(url, json=data,headers=header)
    response.raise_for_status()
    if response.status_code == 200:
        return response.json()
    else:
        return {"Error": "API call failed with status code", "StatusCode" : {response.status_code}}


# ------------------------------
# Call any API (headers + query)
# ------------------------------
@app.tool()
async def http_request(
    url: str,
    method: str = "GET",
    headers: dict = None,
    params: dict = None,
    json_body: dict = None,
) -> str:
    """
    A flexible tool for GET/POST/PATCH/DELETE etc.
    """
    
    response = requests.request(
            method=method.upper(),
            url=url,
            headers=headers,
            params=params,
            json=json_body
    )
    response.raise_for_status()
    return response.text


if __name__ == "__main__":
    app.run(transport="http",host="localhost",port=8000)
