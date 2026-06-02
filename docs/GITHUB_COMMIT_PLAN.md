# GITHUB COMMIT PLAN

Status: PREPARED ONLY. No repo. No push. Waiting on final GitHub authority.

## Repo

- Name: decisionrecord-merkle-receipts
- Subtitle / description: Tamper-evident receipt proofs for bounded decision records.
- Visibility: HUMAN decides (public / private) at push time.

## File list (GitHub-ready)

```
decisionrecord-merkle-receipts/
├── .gitignore
├── README.md
├── docs/
│   ├── CLAIM_BOUNDARY.md
│   ├── LICENSE_RECOMMENDATION.md   (recommendation; remove before push if desired)
│   └── GITHUB_COMMIT_PLAN.md       (this file; internal, optional to include)
├── examples/
│   └── mock_decision_records.json
├── receipts/
│   └── sample_receipt.json
├── src/
│   └── merkle_receipt.py
└── tests/
    └── test_merkle_receipt.py
```

Note: LICENSE is NOT present. A LICENSE file is added only after the human
names MIT / Apache-2.0 / no licence yet.

## Suggested commit sequence (single initial commit)

Plain, honest history. One commit is enough for a demonstrator.

```
commit 1
  message: "Initial commit: tamper-evident DecisionRecord receipt demonstrator"
  body:
    Minimal Python demonstrator for Merkle inclusion-proof receipts.
    Workspace build. Demonstrator only. See docs/CLAIM_BOUNDARY.md.
    No production, certification, TrinityOS, or quantum claim.
  includes: all files in the list above
```

If you prefer staged history instead of one commit:

```
commit 1  docs: README + CLAIM_BOUNDARY
commit 2  feat: merkle_receipt demonstrator + example records
commit 3  test: receipt verification + tamper detection
commit 4  chore: sample receipt + gitignore
```

## Pre-push checklist (human-gated)

- [ ] Licence chosen and LICENSE file drafted (or "no licence yet" accepted)
- [ ] Decide whether to include docs/LICENSE_RECOMMENDATION.md and this plan
- [ ] Decide repo visibility (public / private)
- [ ] Confirm no public claim / production claim is added to README
- [ ] Final GitHub authority granted by HUMAN

## Boundary (unchanged)

- no public claim
- no production claim
- no TrinityOS validation
- no quantum claim
- no push until final GitHub authority
