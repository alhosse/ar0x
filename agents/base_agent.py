from abc import ABC, abstractmethod
from typing import Dict, Any, List


class BaseSecurityAgent(ABC):
    """Abstract base class for ar0x sub-agents with XAI logging."""

    def __init__(self, name: str):
        self.name = name

    @abstractmethod
    def analyze(self, telemetry: Dict[str, Any]) -> List[Dict[str, Any]]:
        raise NotImplementedError

    def build_finding(
        self,
        rule_id: str,
        title: str,
        severity: str,
        cwe_id: str,
        owasp_category: str,
        endpoint: str,
        confidence: float,
        xai_reasoning: List[str],
        evidence: str,
    ) -> Dict[str, Any]:
        return {
            "agent": self.name,
            "rule_id": rule_id,
            "title": title,
            "severity": severity,
            "cwe_id": cwe_id,
            "owasp_category": owasp_category,
            "endpoint": endpoint,
            "confidence": confidence,
            "xai_reasoning": xai_reasoning,
            "evidence": evidence,
        }
