import types

from django.db import models
from django_extensions.db.models import TimeStampedModel

import spacy

from whoisthat.utils import max_length_from_choices, ttext

def _spacy_pos_map(namespace:object) -> object:
    for key, val in spacy.parts_of_speech.univ_pos_t.__members__.items():
        namespace[key] = (int(val), ttext(spacy.explain(key) or 'Untagged'))
    return namespace

PartsOfSpeech = types.new_class('PartsOfSpeech',
                                bases=(models.TextChoices,),
                                exec_body=_spacy_pos_map)

class RedditStatus(models.TextChoices):
    """Enumeration of reddit states."""
    ACTIVE = 'A', ttext('Active')
    INACTIVE = 'I', ttext('Inactive')
    SUSPENDED = 'S', ttext('Suspended')

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


class Post(TimeStampedModel):

    posted_to = models.ForeignKey('reddit_bot.Reddit', on_delete=models.CASCADE)
    post_id = models.CharField(null=False, blank=False, max_length=32)
    title = models.TextField(null=False, blank=False)
    permalink = models.CharField(null=False, blank=False, max_length=512)
    post_create_date = models.DateTimeField()
    tokenized = models.NullBooleanField()

    def __str__(self):
        return f'{self.title} (id {self.post_id})'

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=('post_id', ),
                                    name='uq_post_post_id'),
        ]
        indexes = [
            models.Index(fields=('title', ),
                         name='idx_post_title'),
        ]


class PostPersonTokens(TimeStampedModel):

    post = models.ForeignKey('reddit_bot.Post', on_delete=models.CASCADE, related_name='person_tokens')
    token = models.CharField(null=False, blank=False, max_length=128)
    confirmed = models.NullBooleanField()
    corrected = models.NullBooleanField()

    def __str__(self):
        return f'Post {self.post}: {self.token}'

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=('post', 'token'),
                                    name='uq_ppt_post_token'),
        ]
        indexes = [
            models.Index(fields=('token', ),
                         name='idx_ppt_token'),
        ]


class PostNonPersonTokens(TimeStampedModel):

    post = models.ForeignKey('reddit_bot.Post', on_delete=models.CASCADE, related_name='non_person_tokens')
    token = models.CharField(null=False, blank=False, max_length=128)
    part_of_speech = models.CharField(null=False, blank=False,
                                      choices=PartsOfSpeech.choices, default=PartsOfSpeech.NO_TAG,
                                      max_length=max_length_from_choices(PartsOfSpeech))
    person_translation = models.CharField(null=True, blank=True, max_length=128)

    def __str__(self):
        part = PartsOfSpeech(self.part_of_speech)
        return f'Post {self.post}: {self.token} (part.label)'

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=('post', 'token'),
                                    name='uq_pnpt_post_token'),
        ]
        indexes = [
            models.Index(fields=('token', 'part_of_speech'),
                         name='idx_pnpt_token_pos'),
        ]
