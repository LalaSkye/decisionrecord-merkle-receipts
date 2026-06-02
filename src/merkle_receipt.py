"""
merkle_receipt.py

A minimal demonstrator for tamper-evident DecisionRecord receipts
using Merkle inclusion proofs.

One job:
  - prove a recorded decision belongs to a committed set
  - prove that tampering breaks verification

This is a demonstrator only. See docs/CLAIM_BOUNDARY.md.
No production claim. No certification. No governance enforcement.
"""

from __future__ import annotations

import hashlib
import json
from typing import Any, Dict, List


# ----------------------------------------------------------------------
# Hashing
# ----------------------------------------------------------------------

def _sha256(data: bytes) -> str:
    """Return the hex SHA-256 of raw bytes."""
    return hashlib.sha256(data).hexdigest()


def hash_record(record: Dict[str, Any]) -> str:
    """
    Fixed fingerprint of a single DecisionRecord.

    The record is serialised with sorted keys and no incidental
    whitespace so the same record always hashes to the same value.
    """
    canonical = json.dumps(record, sort_keys=True, separators=(",", ":"))
    return _sha256(canonical.encode("utf-8"))


def _hash_pair(left: str, right: str) -> str:
    """Hash two child hashes (hex strings) into their parent hash."""
    return _sha256((left + right).encode("utf-8"))


# ----------------------------------------------------------------------
# Merkle tree
# ----------------------------------------------------------------------

def build_levels(leaf_hashes: List[str]) -> List[List[str]]:
    """
    Build all levels of the Merkle tree, bottom-up.

    levels[0] is the leaves. levels[-1] is a single-element list
    holding the root. If a level has an odd number of nodes, the
    last node is duplicated (a common, simple convention).

    An empty input is rejected: there is nothing to commit to.
    """
    if not leaf_hashes:
        raise ValueError("cannot build a Merkle tree over an empty set")

    levels: List[List[str]] = [list(leaf_hashes)]
    while len(levels[-1]) > 1:
        current = levels[-1]
        nxt: List[str] = []
        for i in range(0, len(current), 2):
            left = current[i]
            right = current[i + 1] if i + 1 < len(current) else current[i]
            nxt.append(_hash_pair(left, right))
        levels.append(nxt)
    return levels


def merkle_root(leaf_hashes: List[str]) -> str:
    """One value that commits to the whole ordered set of leaves."""
    return build_levels(leaf_hashes)[-1][0]


def inclusion_proof(leaf_hashes: List[str], index: int) -> List[Dict[str, str]]:
    """
    Produce the inclusion proof (audit path) for the leaf at `index`.

    The proof is the list of sibling hashes needed to walk from the
    leaf up to the root, each tagged with the side it sits on.
    """
    if index < 0 or index >= len(leaf_hashes):
        raise IndexError("leaf index out of range")

    levels = build_levels(leaf_hashes)
    proof: List[Dict[str, str]] = []
    idx = index
    for level in levels[:-1]:
        is_right = idx % 2 == 1
        if is_right:
            sibling_idx = idx - 1
            side = "left"
        else:
            sibling_idx = idx + 1 if idx + 1 < len(level) else idx
            side = "right"
        proof.append({"side": side, "hash": level[sibling_idx]})
        idx //= 2
    return proof


def verify_proof(leaf_hash: str, proof: List[Dict[str, str]], root: str) -> bool:
    """
    Recompute the root from a leaf hash and its proof.

    Returns True only if the recomputed root matches the committed root.
    If the leaf was tampered with, leaf_hash changes and this returns False.
    """
    computed = leaf_hash
    for step in proof:
        if step["side"] == "left":
            computed = _hash_pair(step["hash"], computed)
        else:
            computed = _hash_pair(computed, step["hash"])
    return computed == root


# ----------------------------------------------------------------------
# Receipts
# ----------------------------------------------------------------------

def make_receipt(records: List[Dict[str, Any]], index: int) -> Dict[str, Any]:
    """
    Build a replayable receipt for one DecisionRecord in a set.

    The receipt carries everything a later reader needs to re-check
    custody: the record, its hash, its proof, and the committed root.
    """
    leaves = [hash_record(r) for r in records]
    root = merkle_root(leaves)
    return {
        "record": records[index],
        "leaf_hash": leaves[index],
        "leaf_index": index,
        "inclusion_proof": inclusion_proof(leaves, index),
        "merkle_root": root,
    }


def verify_receipt(receipt: Dict[str, Any]) -> bool:
    """
    Re-check a receipt end to end.

    Rehashes the record from scratch, then walks the proof to the root.
    If the record was altered after the receipt was made, the rehash
    differs and verification fails.
    """
    recomputed_leaf = hash_record(receipt["record"])
    if recomputed_leaf != receipt["leaf_hash"]:
        return False
    return verify_proof(
        receipt["leaf_hash"],
        receipt["inclusion_proof"],
        receipt["merkle_root"],
    )


# ----------------------------------------------------------------------
# Demonstrator entry point
# ----------------------------------------------------------------------

def _demo() -> None:
    import copy
    import os

    here = os.path.dirname(os.path.abspath(__file__))
    example = os.path.join(here, "..", "examples", "mock_decision_records.json")
    with open(example, "r", encoding="utf-8") as fh:
        records = json.load(fh)

    receipt = make_receipt(records, index=1)
    print("merkle_root :", receipt["merkle_root"])
    print("leaf_index  :", receipt["leaf_index"])
    print("verify (ok) :", verify_receipt(receipt))

    tampered = copy.deepcopy(receipt)
    tampered["record"]["decision"] = "DENY"  # quietly change the record
    print("verify (tampered):", verify_receipt(tampered), "<- the stop")


if __name__ == "__main__":
    _demo()
