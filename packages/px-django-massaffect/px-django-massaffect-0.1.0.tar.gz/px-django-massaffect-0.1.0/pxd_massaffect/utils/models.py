from typing import Callable

from django.db import models


__all__ = 'get_model_content_type_key',


def get_model_content_type_key(model: models.Model) -> str:
    opts = model._meta
    return '.'.join((opts.app_label, opts.model_name))
