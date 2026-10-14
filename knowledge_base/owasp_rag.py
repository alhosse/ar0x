import json
from pathlib import Path
from typing import Dict, Any


class OWASPKnowledgeBase:
    """Retrieves structured OWASP & CWE remediation guidance for verified findings."""

    def __init__(self):
        db_path = Path(__file__).parent / "owasp_cwe_db.json"
        self.db: Dict[str, Dict[str, str]] = json.loads(db_path.read_text(encoding="utf-8"))

    def enrich_finding(self, finding: Dict[str, Any]) -> Dict[str, Any]:
        cwe_id = finding.get("cwe_id", "")
        entry = self.db.get(cwe_id, {})
        finding["cwe_name"] = entry.get("cwe_name", "General Security Configuration")
        finding["remediation"] = entry.get(
            "remediation",
            "Review OWASP ASVS and apply defense-in-depth configuration hardening."
        )
        return finding
