# Copyright (c) 2022 warevil <jg@warevil.dev>

from datetime import datetime, timezone

from argon2 import PasswordHasher, Type, exceptions

ph = PasswordHasher(
    memory_cost=65536,
    time_cost=4,
    parallelism=2,
    hash_len=32,
    type=Type.ID,
)


def check_password(hash: str, password: str) -> bool | None:
    try:
        ph.verify(hash, password)
    except exceptions.VerifyMismatchError:
        return False

    # Optional
    # if ph.check_needs_rehash(hash):
    #     return None

    # After checking rehash, you should use something like:
    # if is_correct_password is None:
    #     self.password = password
    #     self.save()
    #     is_correct_password = True

    return True


def hash_password(password: str) -> str:
    return ph.hash(password)


def utc_now():
    return datetime.now().astimezone(timezone.utc)
