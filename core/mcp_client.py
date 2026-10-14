from typing import Dict, Any


class MCPTelemetryClient:
    """
    Model Context Protocol (MCP) Client Stub.
    Provides a standardized JSON-RPC style interface for querying read-only
    proxy history or configuration states from external security tools.
    """

    def __init__(self, server_name: str = "burp-mcp-readonly"):
        self.server_name = server_name

    def get_proxy_metadata_summary(self, target_host: str) -> Dict[str, Any]:
        return {
            "mcp_server": self.server_name,
            "target_host": target_host,
            "mode": "read_only_telemetry",
            "observed_endpoints": ["/", "/login", "/api/v1/profile"],
        }
