# ar0x — Autonomous AI-Assisted Web Security Auditing & Remediation Framework

## Overview
`ar0x` is a modular, multi-agent web security assessment and remediation framework designed as a graduation project architecture. It leverages local Small Language Models (via Ollama), a structured ReAct (Reason + Act) coordination loop, **ADVA (Automated Differential Verification Analysis)** for false-positive reduction, **Explainable AI (XAI)** reasoning traces, and **SARIF v2.1.0** report generation for CI/CD pipelines.

> **Safety & Compliance Note:** This framework provides the architectural skeleton, passive configuration auditing modules, OWASP/CWE knowledge base (RAG), differential verification logic, and SARIF reporting engine. It is strictly designed for authorized defensive security auditing, compliance verification, and remediation guidance.

## Project Structure
```text
ar0x/
├── README.md
├── requirements.txt
├── config/
│   └── settings.yaml              # Model, scope, and reporting settings
├── cli/
│   ├── __init__.py
│   └── main.py                    # CLI entrypoint
├── core/
│   ├── __init__.py
│   ├── orchestrator.py            # Central ReAct Coordinator & State Machine
│   ├── adva.py                    # Differential Verification & False-Positive Filter
│   └── mcp_client.py              # Model Context Protocol (MCP) telemetry interface
├── agents/
│   ├── __init__.py
│   ├── base_agent.py              # Abstract Agent with XAI reasoning trace
│   ├── config_audit_agent.py      # HTTP Security Headers & CORS Posture Agent
│   ├── auth_review_agent.py       # Session & Cookie Security Posture Agent
│   └── input_validation_agent.py  # Input Handling & CWE Architecture Review Agent
├── skills/
│   ├── __init__.py
│   ├── header_inspector.py        # Passive HTTP Header & Cookie Inspector
│   └── sarif_exporter.py          # SARIF v2.1.0 & XAI Report Generator
├── knowledge_base/
│   ├── __init__.py
│   ├── owasp_rag.py               # Local RAG engine for OWASP & CWE remediation
│   └── owasp_cwe_db.json          # Structured OWASP Top 10 & CWE knowledge base
├── crawler/
│   ├── __init__.py
│   └── discovery.py               # Scope-bounded passive endpoint discovery
└── tests/
    └── test_pipeline.py           # Unit tests for ADVA & SARIF generation
```

## Quick Start
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Run a demo security posture assessment and generate a SARIF report:
   ```bash
   python -m cli.main --target https://example.com --output report.sarif.json --demo
   ```
3. Run unit tests:
   ```bash
   python -m unittest discover -s tests
   ```
