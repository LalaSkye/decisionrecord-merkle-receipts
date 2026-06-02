"""
Tests for merkle_receipt.

These tests do two things:
  - confirm a valid receipt verifies
  - confirm a tampered record breaks verification (the stop)
"""

import copy
import json
import os
import sys

import pytest

# Make src/ importable without installation.
HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "..", "src")
sys.path.insert(0, SRC)

import merkle_receipt as mr  # noqa: E402


def load_records():
    path = os.path.join(HERE, "..", "examples", "mock_decision_records.json")
    with open(path, "r", encoding="utf-8") as fh:
        return json.load(fh)


# ----------------------------------------------------------------------
# Hashing
# ----------------------------------------------------------------------

def test_hash_is_deterministic():
    records = load_records()
    assert mr.hash_record(records[0]) == mr.hash_record(records[0])


def test_hash_changes_when_record_changes():
    records = load_records()
    original = mr.hash_record(records[0])
    changed = copy.deepcopy(records[0])
    changed["decision"] = "DENY"
    assert mr.hash_record(changed) != original


def test_key_order_does_not_change_hash():
    a = {"id": "X", "decision": "ALLOW"}
    b = {"decision": "ALLOW", "id": "X"}
    assert mr.hash_record(a) == mr.hash_record(b)


# ----------------------------------------------------------------------
# Tree
# ----------------------------------------------------------------------

def test_empty_set_is_rejected():
    with pytest.raises(ValueError):
        mr.build_levels([])


def test_root_is_stable():
    records = load_records()
    leaves = [mr.hash_record(r) for r in records]
    assert mr.merkle_root(leaves) == mr.merkle_root(leaves)


def test_single_leaf_root_equals_leaf():
    records = load_records()
    leaf = mr.hash_record(records[0])
    assert mr.merkle_root([leaf]) == leaf


# ----------------------------------------------------------------------
# Inclusion proofs
# ----------------------------------------------------------------------

def test_every_leaf_has_a_valid_proof():
    records = load_records()
    leaves = [mr.hash_record(r) for r in records]
    root = mr.merkle_root(leaves)
    for i, leaf in enumerate(leaves):
        proof = mr.inclusion_proof(leaves, i)
        assert mr.verify_proof(leaf, proof, root) is True


def test_proof_for_wrong_leaf_fails():
    records = load_records()
    leaves = [mr.hash_record(r) for r in records]
    root = mr.merkle_root(leaves)
    proof = mr.inclusion_proof(leaves, 0)
    # Use leaf 1's hash against leaf 0's proof.
    assert mr.verify_proof(leaves[1], proof, root) is False


def test_out_of_range_index_raises():
    records = load_records()
    leaves = [mr.hash_record(r) for r in records]
    with pytest.raises(IndexError):
        mr.inclusion_proof(leaves, len(leaves))


# ----------------------------------------------------------------------
# Receipts — the headline behaviour
# ----------------------------------------------------------------------

def test_valid_receipt_verifies():
    records = load_records()
    receipt = mr.make_receipt(records, index=1)
    assert mr.verify_receipt(receipt) is True


def test_tampered_record_breaks_verification():
    records = load_records()
    receipt = mr.make_receipt(records, index=1)
    tampered = copy.deepcopy(receipt)
    tampered["record"]["decision"] = "DENY"
    assert mr.verify_receipt(tampered) is False


def test_tampered_root_breaks_verification():
    records = load_records()
    receipt = mr.make_receipt(records, index=1)
    tampered = copy.deepcopy(receipt)
    tampered["merkle_root"] = "0" * 64
    assert mr.verify_receipt(tampered) is False


def test_tampered_proof_breaks_verification():
    records = load_records()
    receipt = mr.make_receipt(records, index=1)
    tampered = copy.deepcopy(receipt)
    if tampered["inclusion_proof"]:
        tampered["inclusion_proof"][0]["hash"] = "f" * 64
        assert mr.verify_receipt(tampered) is False
