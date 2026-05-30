"""MCP server for the mac-mini-agent listen server.

Speaks MCP (for Claude.ai / Desktop / Code), as a counterpart to the `direct`
CLI. Each owns its own copy of `client.py` (the listen HTTP layer) so the two
can evolve independently.

Exposes the listen API as MCP tools over streamable-HTTP on 127.0.0.1:7601.
Cloudflare Access is the auth gate in front of this; there is no auth here.
"""

import os

import yaml
from mcp.server.fastmcp import FastMCP
from mcp.server.transport_security import TransportSecuritySettings

from agent_mcp import client

# The local listen FastAPI server. Defaults to loopback; overridable for dev.
LISTEN_URL = os.environ.get("LISTEN_URL", "http://127.0.0.1:7600")

# Public hostname this MCP is reached at through the Cloudflare tunnel. The MCP
# SDK's streamable-HTTP transport has DNS-rebinding protection that only allows
# localhost Host headers by default, so requests proxied in with this Host get
# 421'd unless we allowlist it. Keep the protection on; just add our host.
PUBLIC_HOST = os.environ.get("MCP_PUBLIC_HOST", "jobs.moto-meru.com")
_security = TransportSecuritySettings(
    allowed_hosts=[PUBLIC_HOST, "127.0.0.1:7601", "localhost:7601"],
    allowed_origins=[f"https://{PUBLIC_HOST}", "http://127.0.0.1:7601"],
)

mcp = FastMCP(
    "mac-mini-agent", host="127.0.0.1", port=7601, transport_security=_security
)


@mcp.tool()
def submit_job(prompt: str) -> dict:
    """Submit a new agent job to the Mac. Returns the new job's id and status.

    The prompt is the task the on-device Claude agent will carry out using the
    steer (GUI) and drive (terminal) tools, e.g. "open Safari and read the top
    Hacker News headline".
    """
    return client.start_job(LISTEN_URL, prompt)


@mcp.tool()
def get_job(job_id: str) -> dict:
    """Get the full current state of one job (status, prompt, timing, summary)."""
    return yaml.safe_load(client.get_job(LISTEN_URL, job_id))


@mcp.tool()
def list_jobs(archived: bool = False) -> list:
    """List all jobs (id, status, prompt, created_at). Set archived=True for archived jobs."""
    data = yaml.safe_load(client.list_jobs(LISTEN_URL, archived=archived))
    return (data or {}).get("jobs") or []


@mcp.tool()
def stop_job(job_id: str) -> dict:
    """Stop a running job by id. Kills the worker process and marks it stopped."""
    return client.stop_job(LISTEN_URL, job_id)


@mcp.tool()
def clear_jobs() -> dict:
    """Archive all current jobs. Returns how many were archived."""
    return client.clear_jobs(LISTEN_URL)


def main() -> None:
    """Console entry point: run the MCP server over streamable-HTTP."""
    mcp.run(transport="streamable-http")


if __name__ == "__main__":
    main()
