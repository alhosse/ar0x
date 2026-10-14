import unittest
from core.orchestrator import Orchestrator
from skills.sarif_exporter import SARIFExporter


class TestAr0xPipeline(unittest.TestCase):
    def test_demo_assessment_and_sarif(self):
        orchestrator = Orchestrator(target_url="https://example.com", demo_mode=True)
        findings = orchestrator.run_assessment()
        self.assertTrue(len(findings) > 0)
        for finding in findings:
            self.assertTrue(finding.get("adva_verified"))
            self.assertIn("remediation", finding)

        exporter = SARIFExporter()
        sarif = exporter.generate_sarif(findings)
        self.assertEqual(sarif["version"], "2.1.0")
        self.assertTrue(len(sarif["runs"][0]["results"]) > 0)


if __name__ == "__main__":
    unittest.main()
