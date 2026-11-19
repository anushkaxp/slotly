
from pwdlib import PasswordHash


password_hash = PasswordHash.recommended()


def hash_password(password: str) -> str:
    """Convert a plain-text password into a secure hash."""
    return password_hash.hash(password)


def verify_password(password: str, hashed_password: str) -> bool:
    """Check a password against its stored hash."""
    return password_hash.verify(password, hashed_password)


# hash_password() will be used when a user registers.
# verify_password() will be used when a user logs in.
# Argon2 hashes the password; the original password isn't stored.
# The hash includes the information needed to verify the password, including its salt.