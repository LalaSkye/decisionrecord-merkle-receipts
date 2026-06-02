# decisionrecord-merkle-receipts

Tamper-evident receipt proofs for bounded decision records.

---

A minimal Python demonstrator for tamper-evident DecisionRecord receipts using Merkle inclusion proofs.

## What it does

It shows one thing, clearly:

- A decision is recorded.
- The record is hashed.
- Hashes are committed into a Merkle root.
- A receipt proves a record belongs to that committed set.
- If a record is changed, verification breaks.

That is the whole object. Record in. Proof out. Tamper breaks it.

## Why it exists

Some logs can be edited without the alteration being obvious.

This shows a small, inspectable way to make that visible:
if a recorded decision is altered, the proof fails.

You can run it and see the stop yourself.

## The pieces

- DecisionRecord — a single recorded decision.
- Hash — a fixed fingerprint of that record.
- Merkle root — one value that commits to a whole set of records.
- Inclusion proof — shows a record is inside that set.
- Tamper detection — change a record, the proof fails.
- Replayable custody — anyone can re-check the same evidence later.

## Repository layout

```
decisionrecord-merkle-receipts/
├── README.md
├── src/
│   └── merkle_receipt.py
├── examples/
│   └── mock_decision_records.json
├── tests/
│   └── test_merkle_receipt.py
├── receipts/
│   └── sample_receipt.json
├── docs/
│   └── CLAIM_BOUNDARY.md
└── LICENSE
```

## How to read it

1. Start with this README.
2. Read docs/CLAIM_BOUNDARY.md to see what is and is not being claimed.
3. Look at examples/mock_decision_records.json for sample input.
4. Look at receipts/sample_receipt.json for sample output.
5. Run the tests to watch tamper detection break verification.

## Claim boundary

This repository demonstrates receipt mechanics only.

It does not claim:

- production readiness
- certification
- TrinityOS validation
- quantum readiness
- external adoption
- governance enforcement

Full detail in docs/CLAIM_BOUNDARY.md.

## License

See LICENSE.
