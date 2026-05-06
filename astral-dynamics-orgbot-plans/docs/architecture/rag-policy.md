# RAG / Helpbot Policy

## KB layout

```text
kb/
├── org/
├── star-citizen/
└── admin-private/
```

## Trust levels

| Trust level | Example | Behavior |
|---|---|---|
| `official_org_policy` | rules, onboarding | answer directly |
| `org_lore` | AstralDynamics history | answer directly |
| `external_game_info` | wiki/game data | answer with patch caveat |
| `community_tip` | player advice | label as unofficial |
| `admin_private` | moderation docs | admin-only |

## Behavior rules

- Search only approved document sets.
- Do not expose admin-private documents to normal users.
- If unsure, say so.
- Prefer concise, source-backed answers.
- Keep patch-sensitive Star Citizen advice clearly labeled.
