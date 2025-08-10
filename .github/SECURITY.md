# Security Policy

## Supported Versions

We actively support the following versions of the BFSI Wealth 360 Analytics Platform:

| Version | Supported          |
| ------- | ------------------ |
| 1.x.x   | :white_check_mark: |

## Reporting a Vulnerability

We take security seriously. If you discover a security vulnerability, please follow these steps:

### 🔒 For Security Issues

**DO NOT** create a public GitHub issue for security vulnerabilities.

Instead, please contact us directly:

📧 **Email:** deepjyoti.dev@snowflake.com
🔐 **Subject:** [SECURITY] Wealth 360 Analytics Vulnerability Report

### 📋 What to Include

Please provide:

1. **Description** of the vulnerability
2. **Steps to reproduce** the issue
3. **Potential impact** assessment
4. **Suggested fix** (if available)
5. **Your contact information** for follow-up

### ⏱️ Response Timeline

- **Acknowledgment:** Within 48 hours
- **Initial Assessment:** Within 5 business days
- **Fix Timeline:** Varies by severity (High: 7 days, Medium: 30 days, Low: 90 days)
- **Public Disclosure:** After fix is deployed and tested

### 🛡️ Security Best Practices

For users of this platform:

#### Snowflake Configuration
- Use **role-based access control** (RBAC)
- Enable **multi-factor authentication** (MFA)
- Regularly **rotate credentials**
- Monitor **query history** and access logs

#### Local Development
- Keep **secrets.toml** in `.gitignore`
- Use **environment variables** for credentials
- Regularly **update dependencies**
- Enable **pre-commit hooks** for security scanning

#### Deployment
- Deploy in **Streamlit in Snowflake** for zero-credential architecture
- Use **network policies** to restrict access
- Enable **audit logging** for compliance
- Regular **security reviews** of deployed applications

### 🏆 Recognition

We appreciate security researchers who help improve our platform. With your permission, we'll acknowledge your contribution in our security advisories.

---

Thank you for helping keep the BFSI Wealth 360 Analytics Platform secure! 🛡️
