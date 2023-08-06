# Copyright (c) 2022 warevil <jg@warevil.dev>

import re
from datetime import datetime


def validator_bool(field_name: str, value: bool) -> str | None:
    if not isinstance(value, bool):
        return f'[Not a bool] Field "{field_name}" could not validate "{value}".'


def validator_datetime(field_name: str, value: datetime) -> str | None:
    if not isinstance(value, datetime):
        return f'[Not a datetime] Field "{field_name}" could not validate "{value}".'


def validator_email(field_name: str, value: str) -> str | None:
    '''
    This validator supports email subaddressing, also known as
    the plus sign (+) trick, which allows treating an email
    address with an appended plus sign as if it were a different
    email address.

    NOTE: If you don't want to accept email subaddressing
          you can just copy this code to create your own
          validator and remove '+' in '[.-_+]'
    '''
    regex = re.compile(r'([A-Za-z0-9]+[.-_+])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')

    if not re.fullmatch(regex, value):
        return f'[Invalid email] Field "{field_name}" could not validate "{value}".'


def validator_string(field_name: str, value: str) -> str | None:
    if not isinstance(value, str):
        return f'[Not a string] Field "{field_name}" could not validate "{value}".'
