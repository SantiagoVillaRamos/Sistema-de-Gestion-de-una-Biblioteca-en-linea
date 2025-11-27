# Security Best Practices Guide

## 🔐 Secrets Management

### 1. Environment Variables
- **NEVER** commit `.env` files to version control.
- Use `.env.example` as a template for required variables.
- In production, ensure `ENVIRONMENT=production` is set to enforce strict security checks.

### 2. Generating Strong Secrets
Use Python's `secrets` module to generate cryptographically strong keys:

```bash
# Generate 32-byte URL-safe key (for JWT_SECRET_KEY)
python -c "import secrets; print(secrets.token_urlsafe(32))"

# Generate strong password
python -c "import secrets; print(secrets.token_urlsafe(16))"
```

### 3. Secret Rotation Policy
- **JWT Secret**: Rotate every 90 days.
  - *Procedure*: Update `JWT_SECRET_KEY` in `.env` and restart backend. Note: This invalidates all existing tokens.
- **Database Password**: Rotate every 180 days.
  - *Procedure*: Change password in DB, then update `POSTGRES_PASSWORD` in `.env`.

---

## 🛡️ Development vs. Production

### Development
- Defaults are allowed but will trigger warnings.
- `seed_data.py` can use default passwords (`Admin@1234`) if env vars are missing.

### Production
- **Strict Mode**: Application will **fail to start** if:
  - `JWT_SECRET_KEY` is missing.
  - `POSTGRES_PASSWORD` is missing.
- **Seed Data**: Do NOT run `seed_data.py` in production.

---

## 🚨 Incident Response

If a secret is compromised:
1. **Identify** which secret leaked.
2. **Revoke** the secret immediately (change in provider).
3. **Rotate** to a new secret in `.env`.
4. **Restart** the application.
5. **Audit** logs for unauthorized access during the exposure window.
