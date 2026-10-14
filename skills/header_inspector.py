from typing import Dict, List


REQUIRED_HEADERS = [
    {
        "header_name": "Content-Security-Policy",
        "rule_id": "AR0X-CFG-001",
        "title": "Missing Content-Security-Policy (CSP) Header",
        "severity": "warning",
        "cwe_id": "CWE-693",
    },
    {
        "header_name": "Strict-Transport-Security",
        "rule_id": "AR0X-CFG-002",
        "title": "Missing HTTP Strict-Transport-Security (HSTS) Header",
        "severity": "warning",
        "cwe_id": "CWE-319",
    },
    {
        "header_name": "X-Frame-Options",
        "rule_id": "AR0X-CFG-003",
        "title": "Missing Clickjacking Protection (X-Frame-Options)",
        "severity": "note",
        "cwe_id": "CWE-1021",
    },
]


def inspect_security_headers(headers: Dict[str, str]) -> List[Dict[str, str]]:
    normalized = {k.lower(): v for k, v in headers.items()}
    missing = []
    for item in REQUIRED_HEADERS:
        if item["header_name"].lower() not in normalized:
            missing.append(item)
    return missing
