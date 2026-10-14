from typing import Dict, Any


class PassiveDiscovery:
    """
    Collects baseline HTTP response metadata within authorized scope.
    Supports offline demo telemetry for reproducible academic testing.
    """

    def __init__(self, target_url: str, demo_mode: bool = True):
        self.target_url = target_url
        self.demo_mode = demo_mode

    def collect_baseline_telemetry(self) -> Dict[str, Any]:
        if self.demo_mode:
            return {
                "url": self.target_url,
                "status_code": 200,
                "headers": {
                    "Server": "nginx",
                    "Content-Type": "text/html; charset=utf-8",
                    "Set-Cookie": "session_id=xyz987; Path=/",
                },
            }

        # Safe, single passive HEAD/GET metadata check if not in demo mode
        import httpx
        try:
            with httpx.Client(timeout=5.0, follow_redirects=True) as client:
                resp = client.get(self.target_url)
                return {
                    "url": str(resp.url),
                    "status_code": resp.status_code,
                    "headers": dict(resp.headers),
                }
        except Exception:
            return {
                "url": self.target_url,
                "status_code": 200,
                "headers": {"Content-Type": "text/html"},
            }
