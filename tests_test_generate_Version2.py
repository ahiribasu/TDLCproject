"""
tests/test_generate.py

Tests for the /generate endpoint using FastAPI's TestClient.
"""

import hashlib
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def sha256_hex(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def test_root_welcome():
    """
    Ensure the root endpoint returns the welcome message containing the participant name.
    """
    resp = client.get("/")
    assert resp.status_code == 200
    data = resp.json()
    assert "Welcome to the Tokenization API" in data.get("message", "")


def test_generate_simple_text():
    """
    Test tokenization and checksum for a simple sentence.
    """
    input_text = "Hello, world!"
    resp = client.post("/generate", json={"text": input_text})
    assert resp.status_code == 200
    data = resp.json()

    # tokens should include "Hello" and "world" (regex \w+ picks alphanumerics)
    assert "Hello" in data["tokens"]
    assert "world" in data["tokens"]

    # checksum should match expected sha256 hex digest
    expected_checksum = sha256_hex(input_text)
    assert data["checksum"] == expected_checksum


def test_generate_empty_text():
    """
    Test behaviour when text is empty or whitespace.
    """
    resp = client.post("/generate", json={"text": ""})
    assert resp.status_code == 200
    data = resp.json()
    assert data["tokens"] == []
    assert data["checksum"] == sha256_hex("")