from __future__ import annotations
from typing import Callable, Any

import ckan.plugins.toolkit as tk
import ckan.lib.navl.dictization_functions as df

from ckanext.transmute.types import Field

_transmutators: dict[str, Callable[..., Any]] = {}


def get_transmutators():
    return _transmutators


def transmutator(func):
    _transmutators[f"tsm_{func.__name__}"] = func
    return func


@transmutator
def name_validator(field: Field) -> Field:
    name_validator = tk.get_validator("name_validator")
    field.value = name_validator(field.value, {})

    return field


@transmutator
def to_lowercase(field: Field) -> Field:
    field.value = field.value.lower()
    return field


@transmutator
def to_uppercase(field: Field) -> Field:
    field.value = field.value.upper()
    return field


@transmutator
def string_only(field: Field) -> Field:
    if not isinstance(field.value, str):
        raise df.Invalid(tk._("Must be a string value"))
    return field


@transmutator
def isodate(field: Field) -> Field:
    name_validator = tk.get_validator("isodate")
    field.value = name_validator(field.value, {})

    return field