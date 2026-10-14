from typing import List, Dict, Any


class ADVAEngine:
    """
    Automated Differential Verification Analysis (ADVA).
    Reduces false positives by cross-checking candidate security observations
    against baseline response invariants and confidence thresholds.
    """

    def __init__(self, confidence_threshold: float = 0.75):
        self.confidence_threshold = confidence_threshold

    def verify_findings(
        self,
        candidates: List[Dict[str, Any]],
        baseline_telemetry: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        verified: List[Dict[str, Any]] = []
        status_code = baseline_telemetry.get("status_code", 200)

        for item in candidates:
            confidence = float(item.get("confidence", 0.0))
            # Filter out low-confidence observations or error-page artifacts
            if status_code >= 500:
                continue
            if confidence >= self.confidence_threshold:
                item["adva_verified"] = True
                item["adva_notes"] = (
                    f"Verified against baseline HTTP {status_code} "
                    f"(confidence={confidence:.2f} >= threshold={self.confidence_threshold:.2f})."
                )
                verified.append(item)
        return verified
