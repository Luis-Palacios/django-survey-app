from django.db import models
from django.utils.timezone import now

from .constants import REQUIRED_CHOICES
from .managers import QuestionQuerySet


"""
    Shamefully copying and pasting from the django intro tutorial 🤣
    and pridefully extending from there 😎
"""


class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
    objects = QuestionQuerySet.as_manager()

    def __str__(self):
        return self.question_text

    def choices_count(self):
        return self.choices.count()

    choices_count.short_description = 'Number of choices'

    def has_enough_choices(self):
        return self.choices.count() >= REQUIRED_CHOICES

    has_enough_choices.boolean = True

    def total_votes(self):
        # TODO: Refactor
        # aggregate_dict = self.choices.aggregate(aggregate_dict=Sum('votes'))
        # if aggregate_dict:
        #     return aggregate_dict.get('total_votes', 0)
        return 0


class Choice(models.Model):
    question = models.ForeignKey(Question,
                                 on_delete=models.CASCADE,
                                 related_name='choices')
    choice_text = models.CharField(max_length=200)

    def __str__(self):
        return self.choice_text

    def votes(self):
        return self.answers.count()


class Answer(models.Model):
    choice = models.ForeignKey(Choice,
                               on_delete=models.CASCADE,
                               related_name='answers')
    session_key = models.CharField(max_length=32)
    date = models.DateTimeField(default=now)
