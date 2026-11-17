import unittest
from security_sim import HealthcareCloud

class SecurityTests(unittest.TestCase):
    def setUp(self):
        self.cloud = HealthcareCloud()

    def test_authorized_clinician_reads_synthetic_record(self):
        self.assertIn('SYNTHETIC', self.cloud.read_record('doctor', 'patient-demo-001'))
    def test_guest_cannot_read_private_storage(self):
        self.assertIsNone(self.cloud.read_record('guest', 'patient-demo-001'))
    def test_public_storage_exposure_detected(self):
        cloud = HealthcareCloud(public_storage=True)
        self.assertIn('STORAGE_PUBLIC', cloud.findings())
        self.assertIsNotNone(cloud.read_record('guest', 'patient-demo-001'))
    def test_storage_remediation(self):
        cloud = HealthcareCloud(public_storage=True)
        self.assertTrue(cloud.set_public_storage('ops', False))
        self.assertNotIn('STORAGE_PUBLIC', cloud.findings())
        self.assertIsNone(cloud.read_record('guest', 'patient-demo-001'))
    def test_nonadmin_cannot_change_storage(self):
        self.assertFalse(self.cloud.set_public_storage('doctor', True))
        self.assertFalse(self.cloud.public_storage)
    def test_nonadmin_cannot_escalate_privileges(self):
        self.assertFalse(self.cloud.grant_role('guest', 'guest', 'administrator'))
        self.assertEqual(self.cloud.users['guest'], 'none')
    def test_excessive_privilege_detected(self):
        self.assertTrue(self.cloud.grant_role('ops', 'guest', 'clinician'))
        self.assertIn('GUEST_PRIVILEGED', self.cloud.findings())
    def test_audit_records_allow_and_deny(self):
        self.cloud.read_record('doctor', 'patient-demo-001')
        self.cloud.read_record('guest', 'patient-demo-001')
        self.assertEqual([e.outcome for e in self.cloud.events], ['ALLOW', 'DENY'])
        self.assertEqual(self.cloud.attempts, len(self.cloud.events))
    def test_missing_audit_logging_detected(self):
        cloud = HealthcareCloud(audit_enabled=False)
        cloud.read_record('guest', 'patient-demo-001')
        self.assertIn('AUDIT_GAP', cloud.findings())
    def test_audit_event_fields(self):
        self.cloud.read_record('guest', 'patient-demo-001')
        event = self.cloud.events[0]
        self.assertTrue(all([event.action, event.actor, event.resource, event.outcome, event.timestamp]))
    def test_unknown_identity_denied(self):
        self.assertIsNone(self.cloud.read_record('unknown', 'patient-demo-001'))
    def test_auditor_cannot_read_patient_record(self):
        self.assertIsNone(self.cloud.read_record('compliance', 'patient-demo-001'))

if __name__ == '__main__': unittest.main()
