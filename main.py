from fastmcp import FastMCP
import httpx
from config import header
app = FastMCP("azure-mcp-server",stateless_http=True)


@app.tool()
async def trizen_smarthome(url: str, data: dict) -> dict:
    """
    Perform an HTTP POST request with JSON body.
    """
    async with httpx.AsyncClient() as client:
        response = await client.post(url, json=data,headers=header)
        response.raise_for_status()
        data = response.json()
        return data


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
) -> dict:
    """
    A flexible tool for GET/POST/PATCH/DELETE etc.
    """
    async with httpx.AsyncClient() as client:
        response = await client.request(
            method=method.upper(),
            url=url,
            headers=headers,
            params=params,
            json=json_body
        )
        response.raise_for_status()
        return response


if __name__ == "__main__":
    app.run(transport="http",host="0.0.0.0")
