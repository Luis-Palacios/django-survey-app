from django.db import models
from django.db.models import Sum
"""
    Shamefully copying and pasting from the django intro tutorial 🤣
    and pridefully extending from there
"""


class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')

    def __str__(self):
        return self.question_text

    def choices_count(self):
        return self.choices.count()

    choices_count.short_description = 'Number of choices'

    def total_votes(self):
        aggregate_dict = self.choices.aggregate(aggregate_dict=Sum('votes'))
        if aggregate_dict:
            return aggregate_dict.get('total_votes', 0)
        return 0


class Choice(models.Model):
    question = models.ForeignKey(Question,
                                 on_delete=models.CASCADE,
                                 related_name='choices')
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text
