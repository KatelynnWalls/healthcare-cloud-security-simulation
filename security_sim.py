"""Local healthcare cloud security simulation. Synthetic data only; no cloud deployment."""
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import List

@dataclass
class Event:
    action: str
    actor: str
    resource: str
    outcome: str
    timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

class HealthcareCloud:
    def __init__(self, public_storage=False, audit_enabled=True):
        self.public_storage = public_storage
        self.audit_enabled = audit_enabled
        self.records = {'patient-demo-001': 'SYNTHETIC: routine visit', 'patient-demo-002': 'SYNTHETIC: follow-up'}
        self.roles = {'clinician': {'read_record'}, 'auditor': {'read_audit'}, 'administrator': {'configure_storage', 'assign_role'}}
        self.users = {'doctor': 'clinician', 'compliance': 'auditor', 'ops': 'administrator', 'guest': 'none'}
        self.events: List[Event] = []
        self.attempts = 0

    def _record(self, action, actor, resource, allowed):
        self.attempts += 1
        if self.audit_enabled:
            self.events.append(Event(action, actor, resource, 'ALLOW' if allowed else 'DENY'))
        return allowed

    def read_record(self, actor, record_id):
        permitted = record_id in self.records and (self.public_storage or 'read_record' in self.roles.get(self.users.get(actor, 'none'), set()))
        self._record('read_record', actor, record_id, permitted)
        return self.records[record_id] if permitted else None

    def grant_role(self, actor, target, role):
        permitted = 'assign_role' in self.roles.get(self.users.get(actor, 'none'), set()) and role in self.roles
        self._record('grant_role', actor, target, permitted)
        if permitted:
            self.users[target] = role
        return permitted

    def set_public_storage(self, actor, value):
        permitted = 'configure_storage' in self.roles.get(self.users.get(actor, 'none'), set())
        self._record('configure_storage', actor, 'patient-records', permitted)
        if permitted:
            self.public_storage = bool(value)
        return permitted

    def findings(self):
        alerts = []
        if self.public_storage:
            alerts.append('STORAGE_PUBLIC')
        if self.users.get('guest') in ('clinician', 'administrator'):
            alerts.append('GUEST_PRIVILEGED')
        if not self.audit_enabled or len(self.events) != self.attempts:
            alerts.append('AUDIT_GAP')
        return alerts
