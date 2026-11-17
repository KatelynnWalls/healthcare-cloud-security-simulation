# Healthcare Cloud Security Simulation

A local Python 3 standard-library-only educational simulation of three cloud-security risks. **No cloud infrastructure is deployed, and no real patient information is used.** This is not a HIPAA compliance certification.

## Run

From the project directory:

```bash
python -m unittest discover -s tests -v
```

The tests verify storage exposure and remediation, least-privilege authorization, privilege escalation denial, audit event completeness, and audit-gap detection. `security_sim.py` is an executable policy simulation, **not Terraform or cloud infrastructure-as-code**.

## Conceptual architecture

External actor -> authorization gate -> synthetic patient record store; all access attempts -> audit event store -> findings evaluator. Administrator can configure simulated storage and assign roles; clinician reads records; auditor cannot read patient records; guest has no assigned privileges.

## Scope and limitations

An intentionally public storage setting demonstrates an unsafe state; a guest read succeeds in that unsafe test to illustrate the exposure. This is a simulation of a misconfiguration, not a vulnerability in a live system. Tests are unit tests of in-memory behavior, not cloud integration, penetration, load, encryption, or regulatory compliance tests. The simulator is not a substitute for a deployed cloud application, provider security controls, or independent audit.


## Executable local policy configuration (not cloud IaC)
Run `python validate_config.py config/secure_baseline.json` (expected exit 0), or `python validate_config.py config/insecure_example.json` (expected nonzero). These JSON files define a **local simulated baseline**, not Terraform, cloud resources, or deployment to a cloud provider.

## Publishing the repository
Create a new GitHub repository, upload the contents of `healthcare_cloud_sim/` (not the containing ZIP), and copy the resulting URL into the thesis artifact statement. No repository URL is claimed until you create one. Do not upload real patient data, credentials, or secrets.


## Executable local policy configuration (not cloud IaC)
Run `python validate_config.py config/secure_baseline.json` (expected exit 0), or `python validate_config.py config/insecure_example.json` (expected nonzero). These JSON files define a **local simulated baseline**, not Terraform, cloud resources, or deployment to a cloud provider.

## Publishing the repository
Create a new GitHub repository, upload the contents of `healthcare_cloud_sim/` (not the containing ZIP), and copy the resulting URL into the thesis artifact statement. No repository URL is claimed until you create one. Do not upload real patient data, credentials, or secrets.
