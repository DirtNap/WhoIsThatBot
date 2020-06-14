"""General utility features that apply across all apps in the project."""

def max_length_from_choices(choices):
    """Find the maximum length of a django.db.models.Choices or similar Enum."""
    if vals := choices.values:
        return max([len(str(val)) for val in vals])
    return 0
