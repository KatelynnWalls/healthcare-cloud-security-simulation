"""Executable local policy-as-code checks; not cloud infrastructure provisioning."""
import json,sys
from pathlib import Path

def check(path):
    cfg=json.loads(Path(path).read_text())
    findings=[]
    if cfg.get('storage',{}).get('public_access') is not False: findings.append('STORAGE_PUBLIC')
    if cfg.get('audit',{}).get('enabled') is not True: findings.append('AUDIT_GAP')
    if cfg.get('identities',{}).get('guest') != 'none': findings.append('GUEST_PRIVILEGED')
    return findings

if __name__=='__main__':
    path=sys.argv[1] if len(sys.argv)>1 else 'config/secure_baseline.json'
    issues=check(path)
    print('POLICY CHECK:', 'PASS' if not issues else 'FAIL: '+', '.join(issues))
    sys.exit(bool(issues))
