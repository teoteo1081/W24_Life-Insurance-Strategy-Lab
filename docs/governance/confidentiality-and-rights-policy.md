# Confidentiality, Intellectual Property & Source Rights Policy (Public Governance Rules)

**Scope:** Applies to all contributors and AI assistants working in `W24_Life-Insurance-Strategy-Lab`.

---

## 1. Core Distinction: Usage Permission vs. Public Redistribution Rights

1. **Repository Visibility Does Not Grant Third-Party IP Rights:** Setting a Git repository to `PUBLIC` governs access to repository hosting, **not** legal permission to redistribute third-party copyrighted documents, internal circulars, proprietary methodologies, or private prompts.
2. **Access ≠ Redistribution:** Receiving a document for internal review, sales-force communication, or personal research does **not** automatically authorize public redistribution on the internet.
3. **Explicit Classification Required:** Every external source tracked or referenced in `knowledge/sources/source-registry.csv` MUST carry an explicit `Redistribution_Rights_Status`:
   - `PUBLIC_DISTRIBUTION_AUTHORIZED` — Verified public domain, official government publication, or documented written redistribution license.
   - `RESTRICTED_INTERNAL` — Document explicitly marked internal/confidential/restricted by the issuer.
   - `LICENSED_WITH_CONDITIONS` — Redistributable only under explicit documented terms/attribution.
   - `PERMISSION_UNKNOWN` — Issuer redistribution rights have not been legally verified; do **not** assume public rights.

---

## 2. Prohibited Content in Public Commits

Contributors and AI agents MUST NEVER commit or stage into a public repository:
- Third-party private skills, proprietary instruction sets, private prompts, or paraphrased reconstructions sufficient to reproduce protected third-party methodologies.
- Personal conversations, private review exchanges, or unauthorized attribution of private knowledge providers.
- Credentials, API keys, tokens, private keys, passwords, or customer/agent Personally Identifiable Information (PII).
- Non-portable local workstation paths (`file://` URIs pointing to local drives or OS user directories) that leak local user paths or break reproducibility on other machines.
- Sensitive audit evidence containing confidential third-party details (store restricted audit reports outside the public repository).

---

## 3. Code License & Attribution Boundary

- Any future open-source license added to this repository applies **only** to original code, schemas, documentation, and synthetic models authored by the repository owner — **never** to third-party issuer documents or government circulars.
- For external portfolio sharing where third-party document rights are `RESTRICTED_INTERNAL` or `PERMISSION_UNKNOWN`, prefer **synthetic/anonymized datasets** or **official public legal URLs** paired with `Source_ID` references rather than redistributing third-party binaries.

---

## 4. Pre-Commit Staging Hygiene Gate

Before creating any commit, run `python scripts/run_checks.py` (which invokes `scripts/validate_repo.py`) to verify:
- Zero local workstation paths or secret patterns in tracked text files.
- Valid `Redistribution_Rights_Status` values in `knowledge/sources/source-registry.csv`.
- No unreviewed sensitive artifacts in staging.
