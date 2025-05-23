import json
import os
from dataclasses import dataclass
from typing import Any
import httpx
from mcp.server.fastmcp import FastMCP

from tabulate import tabulate

mcp = FastMCP("gabi", "Provides read-only access to a postgres database via Gabi")


@dataclass
class Config:
    gabi_endpoint: str
    gabi_token: str


config = Config(os.environ.get("GABI_ENDPOINT", ""), os.environ.get("GABI_TOKEN", ""))


def validate_config():
    if not config.gabi_endpoint:
        raise ValueError("GABI_ENDPOINT environment variable is not set.")
    if not config.gabi_token:
        raise ValueError("GABI_TOKEN environment variable is not set.")

    # ensure the endpoint is a valid URL, starting with https:// and not ending with /
    config.gabi_endpoint = config.gabi_endpoint.rstrip("/")
    if not config.gabi_endpoint.startswith("https://"):
        config.gabi_endpoint = "https://" + config.gabi_endpoint

    print(f"Started with GABI_ENDPOINT: {config.gabi_endpoint}")


async def make_request(
    gabi_path: str, data: dict[str, str] | None = None, timeout: float = 30.0
) -> dict[str, Any] | None:
    async with httpx.AsyncClient() as client:
        try:
            headers = {
                "Authorization": f"Bearer {config.gabi_token}",
                "Accept": "application/json",
            }
            url = f"{config.gabi_endpoint}{gabi_path}"
            if data:
                response = await client.post(
                    url,
                    headers=headers,
                    timeout=timeout,
                    json=data,
                )
            else:
                response = await client.get(
                    url,
                    headers=headers,
                    timeout=timeout,
                )
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            print(f"HTTP error: {e.response.status_code} - {e.response.text}")
            print(e)
            return None
        except Exception as e:
            print(e)
            return None


@mcp.tool()
async def check() -> str:
    """
    Run a healthcheck on Gabi to see if the server is reachable and ready and if we have permissons.
    Returns a JSON string with the result of the healthcheck.
    A successful healthcheck will return {"status": "OK"}.
    """
    data = await make_request("/healthcheck")
    if data:
        return json.dumps(data)
    return f"Failed call healthcheck on the gabi instance {config.gabi_endpoint}. Check the logs for more details."


@mcp.tool()
async def query(query: str) -> str:
    """
    Run a SQL query via a Gabi instance.
    Only read queries are allowed. INSERT, UPDATE, DELETE are not allowed.
    params:
        - query: The SQL query to run.
    returns: The result of the query in a tabulated format. This result must then be provided to the user.
    """
    data = await make_request("/query", {"query": query})
    if data:
        if "result" not in data:
            return f"No result found: {data}"
        return tabulate(data["result"])
    return f"Failed to run the query on the gabi instance {config.gabi_endpoint}. Check the logs for more details."


if __name__ == "__main__":
    validate_config()
    mcp.run(transport="stdio")
