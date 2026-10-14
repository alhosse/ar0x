# 🛡️ ar0x — Autonomous AI-Powered Web Security Auditing & Remediation Framework

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![LLM](https://img.shields.io/badge/LLM-Ollama%20%7C%20Qwen2.5--Coder-orange)
![Protocol](https://img.shields.io/badge/MCP-Model%20Context%20Protocol-green)
![Report](https://img.shields.io/badge/Output-SARIF%20v2.1.0-purple)

## 📌 Overview
**`ar0x`** is an autonomous, multi-agent web security auditing and remediation framework developed as a Senior Graduation Project. It simulates the analytical workflow of a human security engineer using a **ReAct (Reason + Act)** loop powered by local Large Language Models (via **Ollama**).

To overcome common AI limitations such as hallucinations and noisy scanner outputs, `ar0x` introduces:
1. **Multi-Agent Architecture:** Specialized sub-agents for configuration auditing, authentication/session review, and input validation architecture.
2. **ADVA (Automated Differential Verification Analysis):** A verification engine that compares candidate findings against baseline HTTP telemetry to eliminate false positives.
3. **Explainable AI (XAI) Traces:** Every finding includes a step-by-step reasoning chain explaining *why* an issue was flagged and *how* it was verified.
4. **Local RAG Knowledge Base:** Enriches verified findings with exact **OWASP Top 10** categories, **CWE** identifiers, and actionable code remediation snippets.
5. **SARIF v2.1.0 Reporting:** Generates standardized reports ready for direct integration into GitHub Advanced Security and CI/CD pipelines.

---

## ⚙️ What Does `ar0x` Actually Do? (Workflow Pipeline)

```text
[Target URL] 
     │
     ▼
1. [Passive Discovery Crawler] ──► Collects baseline HTTP status, headers, cookies & endpoints
     │
     ▼
2. [Central ReAct Orchestrator] ◄──► [Local LLM via Ollama (qwen2.5-coder:7b)]
     │
     ├──► Agent 1: ConfigAuditAgent      (Audits CSP, HSTS, X-Frame-Options, CORS)
     ├──► Agent 2: AuthReviewAgent       (Audits Session Cookies: Secure, HttpOnly, SameSite)
     └──► Agent 3: InputValidationAgent  (Audits MIME-sniffing & Content-Type controls)
     │
     ▼
3. [ADVA Differential Engine]  ──► Filters out false positives using confidence thresholds
     │
     ▼
4. [OWASP/CWE RAG Engine]      ──► Attaches remediation guidance & CWE mappings
     │
     ▼
5. [SARIF v2.1.0 Exporter]     ──► Outputs final report with XAI reasoning traces
```

---

## 🧠 LLM Integration (How to Connect Ollama)

`ar0x` is designed to run 100% locally for data privacy and zero API costs using **Ollama**.

### Step 1: Install & Start Ollama
Download and install Ollama from [ollama.com](https://ollama.com), or via Linux terminal:
```bash
curl -fsSL [https://ollama.com/install.sh](https://ollama.com/install.sh) | sh
ollama serve
```

### Step 2: Pull the Recommended Model
By default, `ar0x` uses `qwen2.5-coder:7b` (or you can use `llama3.1:8b` / `mistral`):
```bash
ollama pull qwen2.5-coder:7b
```

### Step 3: Configure `config/settings.yaml`
You can customize the LLM model, temperature, and local endpoint inside `config/settings.yaml`:
```yaml
llm:
  provider: "ollama"
  base_url: "[http://127.0.0.1:11434](http://127.0.0.1:11434)"
  model: "qwen2.5-coder:7b"
  temperature: 0.1
  timeout_seconds: 60
```

---

## 🚀 Installation & Setup

```bash
# 1. Clone the repository
git clone [https://github.com/YOUR_USERNAME/ar0x.git](https://github.com/YOUR_USERNAME/ar0x.git)
cd ar0x

# 2. (Optional) Create a virtual environment
python3 -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate

# 3. Install required dependencies
pip install -r requirements.txt
```

---

## 💻 Usage & CLI Commands

You can run `ar0x` from the root directory using `python -m cli.main`.

### CLI Arguments Reference

| Argument | Short | Description | Required | Default |
| :--- | :--- | :--- | :---: | :--- |
| `--target` | `-t` | Target URL within authorized assessment scope (e.g., `https://example.com`) | **Yes** | — |
| `--output` | `-o` | File path to save the generated SARIF v2.1.0 JSON report | No | `ar0x_report.sarif.json` |
| `--demo` | — | Run using offline simulated HTTP telemetry for quick testing & demos | No | `False` |
| `--help` | `-h` | Show help message and all available CLI options | No | — |

### Examples

**1. View CLI Help Menu:**
```bash
python -m cli.main --help
```

**2. Run Offline Demo Mode (Fast test without network requests):**
```bash
python -m cli.main --target [https://example.com](https://example.com) --output demo_report.sarif.json --demo
```

**3. Run Passive Security Posture Audit on an Authorized Target:**
```bash
python -m cli.main -t [https://testphp.vulnweb.com](https://testphp.vulnweb.com) -o audit_results.sarif.json
```

**4. Run Automated Unit Tests:**
```bash
python -m unittest discover -s tests
```

---

## 📊 Sample Output (XAI + SARIF v2.1.0)

When `ar0x` finishes an assessment, it generates a structured `.sarif.json` file containing the finding, CWE/OWASP mapping, ADVA verification status, and the **Explainable AI (XAI)** reasoning trace:

```json
{
  "ruleId": "AR0X-CFG-001",
  "level": "warning",
  "message": {
    "text": "Missing Content-Security-Policy (CSP) Header | Evidence: Missing response header: Content-Security-Policy"
  },
  "properties": {
    "agent": "ConfigAuditAgent",
    "confidence": 0.92,
    "adva_verified": true,
    "xai_reasoning": [
      "Observed HTTP response from [https://example.com](https://example.com).",
      "Header 'Content-Security-Policy' was absent in baseline response.",
      "Missing 'Content-Security-Policy' increases exposure to client-side risks; flagged for remediation."
    ],
    "remediation": "Define a strict Content-Security-Policy (CSP) header restricting script-src and object-src to trusted origins."
  }
}
```

---

## 📂 Project Structure
```text
ar0x/
├── README.md                          # Complete documentation, LLM setup & usage guide
├── requirements.txt                   # Python dependencies (httpx, pydantic, pyyaml, rich)
├── config/
│   └── settings.yaml                  # Ollama LLM configuration, ADVA thresholds & scope settings
├── cli/
│   └── main.py                        # Command-Line Interface (CLI) entrypoint
├── core/
│   ├── orchestrator.py                # Central ReAct Coordinator & State Machine
│   ├── adva.py                        # Automated Differential Verification Analysis (False-Positive Filter)
│   └── mcp_client.py                  # Model Context Protocol (MCP) read-only telemetry interface
├── agents/
│   ├── base_agent.py                  # Abstract Agent base class with XAI reasoning trace builder
│   ├── config_audit_agent.py          # HTTP Security Headers & CORS Posture Agent
│   ├── auth_review_agent.py           # Session & Cookie Security Posture Agent
│   └── input_validation_agent.py      # Input Handling & MIME-Sniffing Architecture Review Agent
├── skills/
│   ├── header_inspector.py            # Passive HTTP Header Inspector skill
│   └── sarif_exporter.py              # OASIS SARIF v2.1.0 & XAI Report Generator
├── knowledge_base/
│   ├── owasp_rag.py                   # Local RAG engine for OWASP Top 10 & CWE remediation
│   └── owasp_cwe_db.json              # Structured OWASP & CWE knowledge base
├── crawler/
│   └── discovery.py                   # Scope-bounded passive endpoint discovery
└── tests/
    └── test_pipeline.py               # Automated unit tests for ADVA & SARIF pipeline
```

## ⚖️ Safety & Ethical Compliance
This framework is strictly designed for **authorized defensive security auditing, academic research, compliance verification, and remediation guidance**. It performs passive configuration analysis and does not execute destructive or unauthorized active exploitation payloads.
