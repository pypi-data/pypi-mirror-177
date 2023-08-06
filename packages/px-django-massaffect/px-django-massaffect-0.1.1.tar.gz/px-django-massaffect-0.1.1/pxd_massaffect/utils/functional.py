from functools import lru_cache
from django.utils.module_loading import import_string
import random
import string


__all__ = (
    'cached_import_string',
    'make_unique_label',
)


@lru_cache
def cached_import_string(path: str):
    return import_string(path)


def make_unique_label(length: int, alphabet: str = string.ascii_lowercase) -> str:
    return ''.join(random.choices(alphabet, k=length))
