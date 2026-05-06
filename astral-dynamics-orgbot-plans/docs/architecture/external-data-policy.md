# External Data Policy

## Approved sources

### Star Citizen Wiki / StarCitizen.tools

Use for:

- gameplay reference
- beginner help
- ships/items/locations if needed later
- patch-sensitive game information

Rules:

- cache responses
- show source labels when answering
- treat data as patch-sensitive
- do not use wiki data as proof of identity

### SENTRY

Optional and disabled by default.

Possible uses:

- public RSI handle lookup
- public citizen/org profile enrichment
- public org membership hints

Rules:

- treat as third-party
- do not treat as official authentication
- do not block registration if unavailable
- allow manual override

### RSI public pages

Disabled by default.

Rules:

- do not scrape login-protected pages
- do not collect RSI credentials
- do not impersonate a user session
- do not automate in a way that violates RSI terms

## Prohibited for V1

- RSI login scraping
- password collection
- automated harvesting of other users
- dependence on unofficial data for access control
