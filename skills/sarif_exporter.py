from typing import List, Dict, Any


class SARIFExporter:
    """Exports verified security findings in OASIS SARIF v2.1.0 format."""

    def __init__(self, tool_name: str = "ar0x", version: str = "1.0.0"):
        self.tool_name = tool_name
        self.version = version

    def generate_sarif(self, findings: List[Dict[str, Any]]) -> Dict[str, Any]:
        rules = []
        results = []
        seen_rules = set()

        for f in findings:
            rule_id = f["rule_id"]
            if rule_id not in seen_rules:
                seen_rules.add(rule_id)
                rules.append({
                    "id": rule_id,
                    "name": f["title"].replace(" ", ""),
                    "shortDescription": {"text": f["title"]},
                    "help": {
                        "text": f.get("remediation", "Apply OWASP recommended secure configuration.")
                    },
                    "properties": {
                        "cwe": f.get("cwe_id"),
                        "owasp": f.get("owasp_category"),
                    }
                })

            results.append({
                "ruleId": rule_id,
                "level": f.get("severity", "warning"),
                "message": {
                    "text": f"{f['title']} | Evidence: {f['evidence']}"
                },
                "locations": [
                    {
                        "physicalLocation": {
                            "artifactLocation": {
                                "uri": f.get("endpoint", "/")
                            }
                        }
                    }
                ],
                "properties": {
                    "agent": f.get("agent"),
                    "confidence": f.get("confidence"),
                    "adva_verified": f.get("adva_verified", False),
                    "xai_reasoning": f.get("xai_reasoning", []),
                    "remediation": f.get("remediation", ""),
                }
            })

        return {
            "$schema": "https://json.schemastore.org/sarif-2.1.0.json",
            "version": "2.1.0",
            "runs": [
                {
                    "tool": {
                        "driver": {
                            "name": self.tool_name,
                            "version": self.version,
                            "informationUri": "https://owasp.org/www-project-top-ten/",
                            "rules": rules,
                        }
                    },
                    "results": results,
                }
            ]
        }
