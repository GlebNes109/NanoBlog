import hashlib

import pytest

from src.infrastructure.password_hasher_impl import sha256HashCreator


@pytest.mark.asyncio
async def test_hash_password():
    hasher = sha256HashCreator()
    password = "test_password"

    hashed = await hasher.hash(password)

    # Verify it's a SHA256 hash (64 hex characters)
    assert len(hashed) == 64
    assert hashed == hashlib.sha256(password.encode("utf-8")).hexdigest()


@pytest.mark.asyncio
async def test_verify_correct_password():
    hasher = sha256HashCreator()
    password = "test_password"

    hashed = await hasher.hash(password)
    is_valid = await hasher.verify(password, hashed)

    assert is_valid is True


@pytest.mark.asyncio
async def test_verify_incorrect_password():
    hasher = sha256HashCreator()
    password = "test_password"
    wrong_password = "wrong_password"

    hashed = await hasher.hash(password)
    is_valid = await hasher.verify(wrong_password, hashed)

    assert is_valid is False


@pytest.mark.asyncio
async def test_hash_different_passwords_different_hashes():
    hasher = sha256HashCreator()
    password1 = "password1"
    password2 = "password2"

    hashed1 = await hasher.hash(password1)
    hashed2 = await hasher.hash(password2)

    assert hashed1 != hashed2


@pytest.mark.asyncio
async def test_hash_same_password_same_hash():
    hasher = sha256HashCreator()
    password = "test_password"

    hashed1 = await hasher.hash(password)
    hashed2 = await hasher.hash(password)

    assert hashed1 == hashed2
