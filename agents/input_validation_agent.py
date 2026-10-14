from typing import Dict, Any, List
from agents.base_agent import BaseSecurityAgent


class InputValidationAgent(BaseSecurityAgent):
    """
    Reviews form/API metadata for input validation & Content-Type enforcement controls.
    Strictly passive and architectural (no active payload injection).
    """

    def __init__(self):
        super().__init__(name="InputValidationAgent")

    def analyze(self, telemetry: Dict[str, Any]) -> List[Dict[str, Any]]:
        findings: List[Dict[str, Any]] = []
        headers = {k.lower(): v for k, v in telemetry.get("headers", {}).items()}
        endpoint = telemetry.get("url", "/")

        if headers.get("x-content-type-options", "").lower() != "nosniff":
            findings.append(
                self.build_finding(
                    rule_id="AR0X-INP-001",
                    title="Missing X-Content-Type-Options nosniff Protection",
                    severity="note",
                    cwe_id="CWE-16",
                    owasp_category="A05:2021-Security Misconfiguration",
                    endpoint=endpoint,
                    confidence=0.85,
                    xai_reasoning=[
                        f"Checked MIME-sniffing protections on {endpoint}.",
                        "X-Content-Type-Options: nosniff is not enforced.",
                        "Browsers may MIME-sniff responses if Content-Type is ambiguous."
                    ],
                    evidence="X-Content-Type-Options header missing or not set to 'nosniff'."
                )
            )
        return findings
