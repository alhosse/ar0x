from typing import Dict, Any, List
from agents.base_agent import BaseSecurityAgent


class AuthReviewAgent(BaseSecurityAgent):
    """Passively audits session cookies and authentication transport protections."""

    def __init__(self):
        super().__init__(name="AuthReviewAgent")

    def analyze(self, telemetry: Dict[str, Any]) -> List[Dict[str, Any]]:
        findings: List[Dict[str, Any]] = []
        headers = {k.lower(): v for k, v in telemetry.get("headers", {}).items()}
        endpoint = telemetry.get("url", "/")
        set_cookie = headers.get("set-cookie", "")

        if set_cookie:
            cookie_lower = set_cookie.lower()
            missing_flags = []
            if "httponly" not in cookie_lower:
                missing_flags.append("HttpOnly")
            if "secure" not in cookie_lower:
                missing_flags.append("Secure")
            if "samesite" not in cookie_lower:
                missing_flags.append("SameSite")

            if missing_flags:
                findings.append(
                    self.build_finding(
                        rule_id="AR0X-AUTH-001",
                        title="Session Cookie Missing Hardening Attributes",
                        severity="warning",
                        cwe_id="CWE-614",
                        owasp_category="A07:2021-Identification and Authentication Failures",
                        endpoint=endpoint,
                        confidence=0.90,
                        xai_reasoning=[
                            f"Inspected Set-Cookie header on {endpoint}.",
                            f"Detected missing defensive attributes: {', '.join(missing_flags)}.",
                            "Recommend enforcing Secure, HttpOnly, and SameSite=Strict/Lax on session identifiers."
                        ],
                        evidence=f"Set-Cookie header lacked: {', '.join(missing_flags)}"
                    )
                )
        return findings
