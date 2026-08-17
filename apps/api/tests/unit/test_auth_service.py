from __future__ import annotations

from uuid import uuid4

import pytest

from ares.domain.exceptions import AuthenticationError
from ares.services.auth_service import AuthService


def test_password_hashing() -> None:
    password = "secure_password"
    hashed = AuthService.hash_password(password)
    assert hashed != password
    assert AuthService.verify_password(password, hashed) is True
    assert AuthService.verify_password("wrong_password", hashed) is False

def test_token_creation_and_decoding() -> None:
    user_id = uuid4()
    token = AuthService.create_access_token(user_id)
    assert token is not None
    
    payload = AuthService.decode_token(token)
    assert payload["sub"] == str(user_id)
    assert payload["type"] == "access"

def test_invalid_token_decoding() -> None:
    with pytest.raises(AuthenticationError):
        AuthService.decode_token("invalid.token.string")
