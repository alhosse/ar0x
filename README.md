# 🛡️ ar0x — Autonomous AI-Powered Web Security Auditing & Remediation Framework

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![LLM](https://img.shields.io/badge/LLM-Gemini%20%7C%20OpenAI%20%7C%20Claude%20%7C%20Ollama-orange)
![Protocol](https://img.shields.io/badge/MCP-Model%20Context%20Protocol-green)
![Report](https://img.shields.io/badge/Output-SARIF%20v2.1.0-purple)

## 📌 Overview
**`ar0x`** is an autonomous, multi-agent web security auditing and remediation framework developed as a Senior Graduation Project. It simulates the analytical workflow of a human security engineer using a **ReAct (Reason + Act)** loop powered by a **Model-Agnostic LLM Engine** (supporting Cloud APIs like **Google Gemini, OpenAI, Anthropic Claude, Groq**, as well as 100% local execution via **Ollama**).

### Key Architectural Pillars
1. **Multi-Agent Architecture:** Specialized sub-agents for configuration auditing, authentication/session review, and input validation architecture.
2. **Model-Agnostic LLM Engine:** Seamlessly switch between cloud frontier models (for deep reasoning) and local SLMs (for strict data privacy and offline auditing).
3. **ADVA (Automated Differential Verification Analysis):** Compares candidate findings against baseline HTTP telemetry invariants to eliminate false positives.
4. **Explainable AI (XAI) Traces:** Every finding includes a step-by-step reasoning chain explaining *why* an issue was flagged and *how* it was verified.
5. **Local RAG Knowledge Base:** Enriches verified findings with exact **OWASP Top 10** categories, **CWE** identifiers, and actionable code remediation snippets.
6. **SARIF v2.1.0 Reporting:** Generates standardized reports ready for direct integration into GitHub Advanced Security and CI/CD pipelines.

---

## ⚙️ Architecture & Workflow Pipeline

```text
[Target URL] 
     │
     ▼
1. [Passive Discovery Crawler] ──► Collects baseline HTTP status, headers, cookies & endpoints
     │
     ▼
2. [Central ReAct Orchestrator] ◄──► [Unified Multi-Provider LLM Engine]
     │                                 ├─ Cloud : Gemini / OpenAI / Claude / Groq
     │                                 └─ Local : Ollama (Qwen2.5-Coder / Llama3)
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

## 🧠 Multi-Provider LLM Integration (Cloud & Local)

`ar0x` is completely model-agnostic. You can connect it to **any Cloud LLM API** or run it **locally offline** by adjusting `config/settings.yaml` or exporting an environment variable.

### Supported LLM Providers

| Provider | Type | Example Models | API Key Env Variable |
| :--- | :---: | :--- | :--- |
| **Google Gemini** | Cloud API | `gemini-2.5-flash`, `gemini-2.5-pro` | `GEMINI_API_KEY` |
| **OpenAI** | Cloud API | `gpt-4o`, `gpt-4o-mini` | `OPENAI_API_KEY` |
| **Anthropic** | Cloud API | `claude-3-5-sonnet-latest` | `ANTHROPIC_API_KEY` |
| **Groq / OpenRouter** | Cloud API | `llama-3.3-70b-versatile`, `deepseek-chat` | `AR0X_API_KEY` |
| **Ollama** | Local (Offline) | `qwen2.5-coder:7b`, `llama3.1:8b`, `mistral` | *None Required* |

### Option A: Using Cloud LLMs (Gemini / OpenAI / Claude / Groq)
1. Export your API key in the terminal:
   ```bash
   # Example for Google Gemini:
   export GEMINI_API_KEY="your-api-key-here"

   # Or for OpenAI / Groq:
   export OPENAI_API_KEY="sk-your-api-key-here"
   ```
2. Update `config/settings.yaml`:
   ```yaml
   llm:
     provider: "gemini"            # or "openai", "anthropic", "groq"
     model: "gemini-2.5-flash"     # or "gpt-4o-mini", "claude-3-5-sonnet-latest"
     temperature: 0.1
   ```

### Option B: Using Local LLMs via Ollama (100% Offline & Private)
1. Start Ollama and pull your preferred model:
   ```bash
   ollama serve
   ollama pull qwen2.5-coder:7b
   ```
2. Update `config/settings.yaml`:
   ```yaml
   llm:
     provider: "ollama"
     base_url: "[http://127.0.0.1:11434](http://127.0.0.1:11434)"
     model: "qwen2.5-coder:7b"
     temperature: 0.1
   ```

---

## 🚀 Installation & Setup

```bash
# 1. Clone the repository
git clone [https://github.com/YOUR_USERNAME/ar0x.git](https://github.com/YOUR_USERNAME/ar0x.git)
cd ar0x

# 2. (Optional) Create and activate a virtual environment
python3 -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate

# 3. Install required dependencies
pip install -r requirements.txt
```

---

## 💻 Usage & CLI Commands

Run `ar0x` from the project root directory using `python -m cli.main`.

### CLI Arguments Reference

| Argument | Short | Description | Required | Default |
| :--- | :--- | :--- | :---: | :--- |
| `--target` | `-t` | Target URL within authorized assessment scope (e.g., `https://example.com`) | **Yes** | — |
| `--output` | `-o` | File path to save the generated SARIF v2.1.0 JSON report | No | `ar0x_report.sarif.json` |
| `--demo` | — | Run using offline simulated HTTP telemetry for quick testing & demos | No | `False` |
| `--help` | `-h` | Show help message and all available CLI options | No | — |

### Execution Examples

**1. View CLI Help Menu:**
```bash
python -m cli.main --help
```

**2. Run Offline Demo Mode (Fast verification without active network requests):**
```bash
python -m cli.main --target [https://example.com](https://example.com) --output demo_report.sarif.json --demo
```

**3. Run Passive Security Posture Audit on an Authorized Target:**
```bash
python -m cli.main -t [https://example.com](https://example.com) -o audit_results.sarif.json
```

**4. Run Automated Unit Tests:**
```bash
python -m unittest discover -s tests
```

---

## 📊 Sample Output (XAI + SARIF v2.1.0)

`ar0x` generates a standardized `.sarif.json` report containing the finding, CWE/OWASP mapping, ADVA verification status, and the **Explainable AI (XAI)** reasoning trace:

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
├── README.md                          # Complete documentation, Multi-LLM setup & usage guide
├── requirements.txt                   # Python dependencies (httpx, pydantic, pyyaml, rich)
├── config/
│   └── settings.yaml                  # Multi-LLM provider configuration, ADVA thresholds & scope
├── cli/
│   └── main.py                        # Command-Line Interface (CLI) entrypoint
├── core/
│   ├── orchestrator.py                # Central ReAct Coordinator & State Machine
│   ├── llm_client.py                  # Unified Multi-Provider LLM Client (Gemini, OpenAI, Claude, Ollama)
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
