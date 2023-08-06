# Copyright (c) 2022 warevil <jg@warevil.dev>

from collections.abc import Sized
from datetime import datetime

from .utils import hash_password, utc_now
from .validators import (validator_bool, validator_datetime, validator_email,
                         validator_string)


class Field:
    '''
    Field class
        All parameters are set False by default, except, ironically, "default",
    which is set None by default.

    auto: Set True to make your field always get an auto_value.
        IMPORTANT: You won't be able to edit it manually.
    blank: Set True if you want to allow blank values.
    default: Set a default value if None is passed in.
    edit: Set True if you want to make your field mutable.
    null: Set True if you want to accept null values.
    process: Set True if you want to trigger a process on your value.
        NOTE: You can customize this process, because it is a function.
    unique: Set True if you want to limit to 1 values passed in.
    '''

    def __init__(
        self,
        auto: bool = False,
        blank: bool = False,
        default=None,
        edit: bool = False,
        null: bool = False,
        process: bool = False,
        unique: bool = False,
    ):
        self.auto = auto
        self.blank = blank
        self.default = default
        self.edit = edit
        # TODO: self.min, self.max
        self.null = null
        self.process = process
        self.unique = unique  # It does not use create_index from pymongo

    @property
    def auto_value(self):
        raise NotImplementedError('You must override "auto_value" property to implement it')

    @property
    def validators(self) -> list:
        return []

    def process_value(self, value):
        return value

    def validate(self, model, field_name: str, value):
        if value is None and self.default is not None:
            value = self.default

        if self.unique:
            self.validate_unique(model, field_name, value)

        if self.auto:
            return self.auto_value

        # Validate 'null'
        if value is None:
            if self.null:
                return

            raise ValueError(f'Field "{field_name}" cannot be null')

        # Validate 'blank'
        if isinstance(value, Sized) and not len(value):
            if self.blank:
                return value

            raise ValueError(f'Field "{field_name}" cannot be empty')

        # Additional validators
        if self.validators:
            for validator in self.validators:
                error_msg = validator(field_name, value)
                if error_msg:
                    raise ValueError(error_msg)

        if self.process:
            return self.process_value(value)

        return value

    def validate_unique(self, model, field_name: str, value):
        rejects = model._reject_unique(**{field_name: value})
        if rejects:
            error_msg = f'Field "{field_name}": "{value}" already exists'
            raise ValueError(error_msg)

    def validate_update(self, model, field_name: str, value):
        if self.edit:
            return self.validate(model, field_name, value)

        error_msg = f'Field "{field_name}" is not editable, but you tried "{value}"'
        raise ValueError(error_msg)


class FieldBool(Field):
    @property
    def validators(self) -> list:
        return [validator_bool]


class FieldDatetime(Field):
    @property
    def auto_value(self) -> datetime:
        return utc_now()

    @property
    def validators(self) -> list:
        return [validator_datetime]


class FieldId(Field):
    pass


class FieldText(Field):
    @property
    def validators(self) -> list:
        return [validator_string]


class FieldEmail(FieldText):
    @property
    def validators(self) -> list:
        validators = super().validators
        validators.append(validator_email)
        return validators


class FieldPassword(FieldText):
    def process_value(self, value: str):
        return hash_password(value)
