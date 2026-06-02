# CLAIM_BOUNDARY

## Purpose

This file states exactly what this repository claims,
and exactly what it does not.

It is here so the work cannot be mis-read as more than it is.

## What this repository IS

- A minimal demonstrator.
- It shows tamper-evident receipts for DecisionRecords using Merkle inclusion proofs.
- It is meant to be read, run, and inspected by a person.
- Its one job: prove a recorded decision belongs to a committed set, and prove that tampering breaks verification.

## What this repository IS NOT

This repository does not claim:

- production readiness
- certification (of any kind)
- TrinityOS validation
- quantum readiness
- external adoption
- governance enforcement
- security guarantees for real-world deployment
- legal or regulatory compliance

## Scope

- Scope: demonstration only.
- Audience: a reader who wants to see the mechanic work and see the stop.
- Status: illustrative. Not a service. Not a product.

## What "proof" means here

"Proof" in this repository means:

- a receipt shows a record is included in a committed set, and
- a changed record fails that check.

It does not mean formal proof, audit, or assurance of any wider system.

## Standard techniques

This repository uses standard cryptographic and software concepts for demonstration purposes and does not claim ownership over Merkle trees, hashing, inclusion proofs, or tamper-evident logging as general techniques.

## If this changes

Any future claim beyond this boundary is a separate decision.

It must be made explicitly, by a human, and recorded as a scope event.
Nothing in this file grants that upgrade.
