from typing import Dict, Any, List
from agents.base_agent import BaseSecurityAgent
from skills.header_inspector import inspect_security_headers


class ConfigAuditAgent(BaseSecurityAgent):
    """Evaluates HTTP security headers, TLS enforcement, and CORS posture."""

    def __init__(self):
        super().__init__(name="ConfigAuditAgent")

    def analyze(self, telemetry: Dict[str, Any]) -> List[Dict[str, Any]]:
        findings: List[Dict[str, Any]] = []
        headers = telemetry.get("headers", {})
        endpoint = telemetry.get("url", "/")

        missing_headers = inspect_security_headers(headers)
        for hdr in missing_headers:
            findings.append(
                self.build_finding(
                    rule_id=hdr["rule_id"],
                    title=hdr["title"],
                    severity=hdr["severity"],
                    cwe_id=hdr["cwe_id"],
                    owasp_category="A05:2021-Security Misconfiguration",
                    endpoint=endpoint,
                    confidence=0.92,
                    xai_reasoning=[
                        f"Observed HTTP response from {endpoint}.",
                        f"Header '{hdr['header_name']}' was absent in baseline response.",
                        f"Missing '{hdr['header_name']}' increases exposure to client-side risks; flagged for remediation."
                    ],
                    evidence=f"Missing response header: {hdr['header_name']}"
                )
            )
        return findings
