import hashlib

from src.domain.password_hasher import PasswordHasher


class sha256HashCreator(PasswordHasher):
    async def hash(self, password):
        sha256hash = hashlib.sha256()
        sha256hash.update(password.encode("utf-8"))
        return str(sha256hash.hexdigest())

    async def verify(self, password: str, hashed: str) -> bool:
        return await self.hash(password) == hashed
