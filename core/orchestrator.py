from typing import List, Dict, Any
from crawler.discovery import PassiveDiscovery
from agents.config_audit_agent import ConfigAuditAgent
from agents.auth_review_agent import AuthReviewAgent
from agents.input_validation_agent import InputValidationAgent
from core.adva import ADVAEngine
from knowledge_base.owasp_rag import OWASPKnowledgeBase


class Orchestrator:
    """
    Central Coordinator implementing the ReAct (Reason + Act) loop:
    1. Observe: Collect passive endpoint metadata & HTTP response headers.
    2. Analyze: Dispatch specialized sub-agents with XAI reasoning traces.
    3. Verify (ADVA): Perform differential baseline comparison to filter false positives.
    4. Enrich (RAG): Attach OWASP Top 10 / CWE remediation guidance.
    """

    def __init__(self, target_url: str, demo_mode: bool = True):
        self.target_url = target_url
        self.demo_mode = demo_mode
        self.discovery = PassiveDiscovery(target_url=target_url, demo_mode=demo_mode)
        self.adva = ADVAEngine(confidence_threshold=0.75)
        self.kb = OWASPKnowledgeBase()
        self.agents = [
            ConfigAuditAgent(),
            AuthReviewAgent(),
            InputValidationAgent(),
        ]

    def run_assessment(self) -> List[Dict[str, Any]]:
        # Step 1: Passive Discovery & Telemetry Collection
        telemetry = self.discovery.collect_baseline_telemetry()

        # Step 2: Multi-Agent Security Posture Analysis
        candidate_findings: List[Dict[str, Any]] = []
        for agent in self.agents:
            agent_results = agent.analyze(telemetry)
            candidate_findings.extend(agent_results)

        # Step 3: ADVA Differential Verification (False-Positive Reduction)
        verified_findings = self.adva.verify_findings(candidate_findings, telemetry)

        # Step 4: OWASP / CWE RAG Remediation Enrichment
        enriched_findings = [
            self.kb.enrich_finding(finding) for finding in verified_findings
        ]
        return enriched_findings
