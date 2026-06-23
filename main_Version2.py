"""
main.py

FastAPI application that exposes:
- GET /            -> welcome message (customized)
- POST /generate  -> accepts JSON body {"text": "..."} and returns tokens and checksum

Copyright © 2024 Accenture. All Rights Reserved.
GitHub Copilot
"""

from typing import List
import re
import hashlib

from fastapi import FastAPI
from pydantic import BaseModel

# ---------------------------------------------------------------------------
# NOTE for GitHub Copilot:
# Please generate a Pydantic model named `TokenRequest` with a single field:
# - text: str
# ---------------------------------------------------------------------------

class TokenRequest(BaseModel):
    """
    Request model for token generation endpoint.

    Fields:
    - text: str -- the input text to be tokenized and checksummed
    """
    text: str


class TokenResponse(BaseModel):
    """
    Response model for the token generation endpoint.

    Fields:
    - tokens: List[str] -- the tokenized words from the input text
    - checksum: str     -- SHA-256 checksum (hex) of the original text
    """
    tokens: List[str]
    checksum: str


app = FastAPI(
    title="Tokenization API",
    description="Small API that tokenizes input text and returns tokens + checksum.",
    version="0.1.0",
)


def generate(text: str) -> List[str]:
    """
    Tokenize the provided text into a list of tokens.

    Implementation details:
    - Uses a simple regex to find word tokens (alphanumeric + underscore).
    - Returns tokens in the original case (preserves capitalization).
    - This function is intentionally simple but can be replaced with a
      more advanced tokenizer (e.g., spaCy, NLTK, or a BPE tokenizer) if needed.
    """
    # Find sequences of word characters (equivalent to \w+), avoid punctuation.
    tokens = re.findall(r"\w+", text)
    return tokens


def compute_checksum(text: str) -> str:
    """
    Compute a SHA-256 checksum hex digest for the given text.

    Returns:
        hex string of the checksum
    """
    # Always encode the text to bytes using utf-8 for a consistent checksum.
    h = hashlib.sha256(text.encode("utf-8"))
    return h.hexdigest()


@app.get("/")
async def root():
    """
    Root endpoint with a welcome note customized for the participant.

    This returns a short JSON welcome message. The name is customized as requested.
    """
    # Welcome note includes the participant name (from session): "Ahiri Basu"
    return {"message": "Welcome to the Tokenization API, Ahiri Basu!"}


# ---------------------------------------------------------------------------
# NOTE for GitHub Copilot:
# Please create a POST FastAPI endpoint at path '/generate' that:
# - Accepts JSON request body matching TokenRequest
# - Uses generate() to create tokens list
# - Computes checksum of the original text
# - Returns TokenResponse with tokens and checksum
# ---------------------------------------------------------------------------
@app.post("/generate", response_model=TokenResponse)
async def generate_endpoint(request: TokenRequest):
    """
    Generate tokens and checksum for the provided text.

    Request body (JSON):
    {
      "text": "your input text here"
    }

    Response (200):
    {
      "tokens": ["list", "of", "tokens"],
      "checksum": "sha256-hex-string"
    }
    """
    # Basic validation: make sure text is not empty
    if request.text is None or request.text.strip() == "":
        # Return an empty list and checksum of empty string for clarity,
        # alternatively raise an HTTPException if you prefer 400 responses.
        tokens = []
        checksum = compute_checksum("")
        return TokenResponse(tokens=tokens, checksum=checksum)

    # Use existing generate() helper to produce tokens
    tokens = generate(request.text)

    # Compute a deterministic checksum of the *original* text
    checksum = compute_checksum(request.text)

    return TokenResponse(tokens=tokens, checksum=checksum)


# Run with: uvicorn main:app --reload
if __name__ == "__main__":
    import uvicorn

    # Use uvicorn programmatically when running directly for convenience.
    # This avoids some warnings if uvicorn is unavailable at import time.
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)