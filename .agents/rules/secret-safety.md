---
description: Prevent committing, staging, or pushing secrets and credentials
trigger: always_on
---

# Secret & Credential Safety

1. **Never stage, commit, or push secrets**: API keys, access/refresh tokens, passwords,
   private keys, or service-account JSON must never enter version control.
   This includes `.env`, `.env.*`, `*.pem`, `*.key`, `*.p12`, `credentials.json`,
   `service-account*.json`, and `application_default_credentials.json`.

2. **Verify before every git write operation**: Run `git status` and `git diff --cached`
   and inspect the result before proposing or executing `git add`, `commit`, or `push`.
   If a secret-bearing file appears, stop and report it instead of proceeding.

3. **Templates only**: Commit `.env.example` with placeholder values
   (e.g. `GOOGLE_API_KEY=your-api-key-here`). Never commit the real `.env`.

4. **Placeholders in documentation**: Lab guides, READMEs, and code samples must use
   obvious placeholders (`<YOUR_PROJECT_ID>`, `your-api-key-here`), never real values
   copied from a working environment. Prefer `$ENV_VAR` references over literals.

5. **Never print secrets**: Do not echo secret values into terminal output, logs, or
   chat. When verifying a credential exists, assert on its presence or length,
   not its value (e.g. `[ -n "$API_KEY" ]`, not `echo "$API_KEY"`).

6. **If a secret was already committed**: Treat it as compromised. Report it immediately,
   advise rotating/revoking the credential first, and do not attempt history rewriting
   without explicit user approval.
