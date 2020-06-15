"""General utility features that apply across all apps in the project."""
from typing import Optional

from django.db import models
from django.utils.translation import gettext_lazy

def max_length_from_choices(choices: models.Choices) -> int:
    """Find the maximum length of a django.db.models.Choices or similar Enum."""
    if vals := choices.values:
        return max([len(str(val)) for val in vals])
    return 0

def ttext(text:Optional[str]) -> str:
    if not text:
        return ''
    return gettext_lazy(text)
