from django.db import models
from django.db.models import Count
from random import randint


class QuestionQuerySet(models.QuerySet):
    def get_random(self, session_key=None):
        # more code than order_by('?') but better performance
        # see https://stackoverflow.com/a/2118712/1685147 for more

        valid_questions_query_set = self.get_valid_questions()
        if session_key:
            valid_questions_query_set = self.get_valid_questions().exclude(
                choices__answers__session_key=session_key)
            count = valid_questions_query_set.aggregate(
                count=Count('id'))['count']
            if count == 0:
                return None
            random_index = randint(0, count - 1)
            question = valid_questions_query_set[random_index]
        else:
            count = valid_questions_query_set.aggregate(
                count=Count('id'))['count']
            if count == 0:
                return None
            random_index = randint(0, count - 1)
            question = valid_questions_query_set[random_index]
        return question

    def get_valid_questions(self):
        return self.annotate(num_choices=Count('choices')).filter(
            num_choices__gte=2)

    def get_invalid_questions(self):
        return self.annotate(num_choices=Count('choices')).filter(
            num_choices__lte=2)
