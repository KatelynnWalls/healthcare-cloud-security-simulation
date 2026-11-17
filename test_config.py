import unittest
from pathlib import Path
from validate_config import check
ROOT=Path(__file__).resolve().parents[1]
class ConfigurationTests(unittest.TestCase):
    def test_secure_baseline_passes(self): self.assertEqual(check(ROOT/'config/secure_baseline.json'),[])
    def test_insecure_example_detected(self): self.assertEqual(set(check(ROOT/'config/insecure_example.json')),{'STORAGE_PUBLIC','AUDIT_GAP'})
