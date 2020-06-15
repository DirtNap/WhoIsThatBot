from django.db import models
from django.utils.translation import gettext_lazy
from django_extensions.db.models import TimeStampedModel

from whoisthat.utils import max_length_from_choices

class RedditStatus(models.TextChoices):
    """Enumeration of reddit states."""
    ACTIVE = 'A', gettext_lazy('Active')
    INACTIVE = 'I', gettext_lazy('Inactive')
    SUSPENDED = 'S', gettext_lazy('Suspended')

class Reddit(TimeStampedModel):

    reddit_name = models.CharField(null=False, blank=False, max_length=21)
    status = models.CharField(null=False, blank=False, default=RedditStatus.ACTIVE,
                              max_length=max_length_from_choices(RedditStatus))
    auto_post = models.BooleanField(default=False)
    listen = models.BooleanField(default=True)
    allow_multiple_replies_in_post = models.BooleanField(default=False)
    max_post_age_days = models.PositiveIntegerField(null=False, default=7)

    def __str__(self):
        return f'{self.reddit_name} ({RedditStatus(self.status).label})'

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=('reddit_name', ),
                                    name='uq_reddit_reddit_name'),
        ]
