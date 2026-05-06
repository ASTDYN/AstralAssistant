# Retention Policy

## Defaults

| Data type | Retention |
|---|---:|
| Warnings | 30 days |
| Incidents | 60 days |
| Admin notes | 90 days |
| Audit logs | 365 days recommended |
| Application private notes | 90 days |

## Behavior

Expired data should not necessarily be hard-deleted immediately.

Recommended behavior:

- warning expired -> hidden from default member view
- incident expired -> hidden from default member view, retained if audit requires
- admin note expired -> archived or redacted
- audit log -> retained longer for accountability

## Implementation

Add retention config in `libs/config/src/retention.config.ts`.

Add later script:

```text
scripts/apply-retention.ts
```
