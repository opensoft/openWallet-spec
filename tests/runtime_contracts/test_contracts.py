"""Structural wire checks only; cryptographic verification lives in the code leg."""
import json
from pathlib import Path
import pytest
from jsonschema import Draft202012Validator

ROOT=Path(__file__).resolve().parents[2]
DIGEST="sha256:"+"1"*64

def read(name):
    schema=json.loads((ROOT/"contracts"/name).read_text())
    Draft202012Validator.check_schema(schema)
    return Draft202012Validator(schema)

def rejects(validator,value):
    assert list(validator.iter_errors(value)), "negative structural fixture unexpectedly accepted"

def example():
    return dict(profile="openwallet.challenge-proof.v0",alg="Ed25519",
                challenge_digest=DIGEST,binding_revision=3,
                binding_ref="binding:fixture",wallet_ref="wallet:fixture",
                key_ref="key:fixture",subject_ref="subject:fixture",
                custody_ref="custody:fixture",signature="A"*86)

def test_exact_fields_and_fixed_profile():
    validator=read("challenge-proof-v0.schema.json")
    value=example()
    validator.validate(value)
    for field in value:
        altered=dict(value);del altered[field]
        rejects(validator,altered)
    for changed in [dict(value,public_key="client-selected"),dict(value,mfa=True),
                    dict(value,alg="none"),dict(value,signature="A"*85+"B"),
                    dict(value,binding_revision=-1)]:
        rejects(validator,changed)
