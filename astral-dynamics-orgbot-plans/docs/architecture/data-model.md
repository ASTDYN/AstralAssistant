# Data Model

## Identity rule

Discord ID is the technical primary identifier.

RSI handle / in-game name is the org-facing identity.

Discord username is stored only as a snapshot because it can change.

## Core entities

| Entity | Purpose |
|---|---|
| `User` | Technical identity, Discord link, RSI handle |
| `MemberProfile` | Membership status, rank, website role |
| `Application` | Recruit application |
| `Rank` | Rank labels `#1` through `#5` |
| `InterestTag` | Gameplay interest tags |
| `Operation` | Scheduled/admin-controlled operation |
| `OperationRsvp` | Member RSVP |
| `AdminNote` | Admin-only member notes |
| `Warning` | Time-limited warning |
| `Incident` | Time-limited incident record |
| `AuditLog` | Accountability trail |

## Demo users

The following are seed examples only:

| Discord username snapshot | In-game name / RSI handle |
|---|---|
| `Ziggiyzoo` | `Ziggiyzoo` |
| `metausername` | `Intergalactic IRS` |
