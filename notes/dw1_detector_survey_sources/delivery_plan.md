# Corrective email: frozen draft and gated delivery plan

Status: **NOT SENT**. No delivery command, dry run, authenticated mail state, or
send attempt was used while preparing this candidate.

## Frozen copy

The human-readable draft is `../dw1_detector_survey_email.md`. The mechanically
deliverable subject and body are `delivery_subject.txt` and `delivery_body.txt`.
The body is byte-for-byte the draft after its subject line and first blank line;
the subject file is byte-for-byte the text following `Subject: `. Candidate hashes
are recorded in `candidate_manifest.md`.

The prose is intentionally listenable: it starts and ends with explicit memo
boundaries, expands the technical metrics on first use, uses paragraphs instead
of tables or bullets, and avoids hashes, repository paths, or citation syntax.

## Hard gate

Delivery is forbidden until both conditions are durable:

1. a fresh one-shot evaluator independently evaluates the exact candidate
   documentation commit and external integrity ledger and returns final PASS; and
2. the manager explicitly authorizes sending this exact subject/body pair after
   seeing that PASS.

A reviewer PASS inside this package is necessary but is not the one-shot evaluator
PASS and does not authorize delivery.

## Mechanical delivery after authorization only

From the survey source directory, the authorized operator runs exactly once:

```text
/home/sichangheagent/.config/bin/email_me.py --manager-human \
  --subject-file delivery_subject.txt --message-file delivery_body.txt
```

The operator must preserve the command exit status and non-secret delivery receipt
or message identifier beside this plan, then confirm that the sent subject and
body hashes match the candidate manifest. If the command's outcome is ambiguous,
do not retry automatically; report the ambiguity to the manager to avoid a
duplicate correction.

Until the two hard-gate conditions are met, the only valid action is to leave the
draft frozen and unsent.
