# User Flows

## New member registration

```text
User joins Discord
  -> bot may post welcome/start-here message
  -> user runs /register
  -> user enters RSI handle / in-game name
  -> bot stores Discord ID as technical identity
  -> bot stores Discord username as snapshot only
  -> profile is created
```

## Application flow

```text
User runs /apply
  -> enters RSI handle
  -> enters timezone
  -> selects interests
  -> answers how they found the org
  -> optionally states whether already in RSI org
  -> application status is SUBMITTED
  -> admin reviews applicant-list
  -> admin approves, rejects, or sets trial
```

## Operation flow

```text
Admin runs /op create
  -> operation is created as DRAFT or SCHEDULED
  -> members run /op list or /op view
  -> members run /op join or /op leave
  -> admin runs /op roster
  -> admin runs /op brief
  -> admin starts/completes/cancels operation
```

## Helpbot flow

```text
User asks /ask
  -> bot searches approved KB documents
  -> bot answers with source/trust label
  -> if unsure, bot says it does not know
  -> admin-private docs are excluded unless requestor is admin and command is admin-only
```
