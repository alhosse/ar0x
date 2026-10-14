import argparse
import json
import sys
from pathlib import Path

from core.orchestrator import Orchestrator
from skills.sarif_exporter import SARIFExporter


def parse_args():
    parser = argparse.ArgumentParser(
        prog="ar0x",
        description="ar0x — Multi-Agent Web Security Auditing & SARIF Reporting Framework"
    )
    parser.add_argument(
        "-t", "--target",
        required=True,
        help="Target URL within authorized assessment scope (e.g., https://example.com)"
    )
    parser.add_argument(
        "-o", "--output",
        default="ar0x_report.sarif.json",
        help="Output path for the SARIF v2.1.0 report"
    )
    parser.add_argument(
        "--demo",
        action="store_true",
        help="Run using simulated HTTP telemetry for offline testing and demonstration"
    )
    return parser.parse_args()


def main():
    args = parse_args()
    print("=" * 65)
    print(" [ar0x] Autonomous AI-Assisted Web Security Auditing Framework")
    print("=" * 65)
    print(f"[*] Target Scope : {args.target}")
    print(f"[*] Execution    : {'Offline Demo Mode' if args.demo else 'Passive Audit Mode'}")

    orchestrator = Orchestrator(target_url=args.target, demo_mode=args.demo)
    verified_findings = orchestrator.run_assessment()

    exporter = SARIFExporter(tool_name="ar0x", version="1.0.0")
    sarif_doc = exporter.generate_sarif(verified_findings)

    output_path = Path(args.output)
    output_path.write_text(json.dumps(sarif_doc, indent=2, ensure_ascii=False), encoding="utf-8")

    print(f"\n[+] Verified Findings : {len(verified_findings)}")
    print(f"[+] SARIF Report Saved: {output_path.resolve()}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
