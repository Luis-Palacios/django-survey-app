from random import randint

from django.db import models
from django.db.models import Count

from .constants import REQUIRED_CHOICES


class QuestionQuerySet(models.QuerySet):
    def get_random(self, session_key=None):
        """Get a Random valid question from the database if
        session_key paremeter is passed it will filter
        question that haven't been answered by that session_id


        Keyword Arguments:
            session_key {string} -- [Session_key] (default: {None})

        Returns:
            [Question] -- [Question instance]
            [None] -- [If not valid question remains on database]
        """
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
        """Get valid questions from the database
        in order for question to be valid it must have at least
        2 choices

        Returns:
            [QuestionQuerySet] -- [A QuestionQuerySet]
        """
        return self.annotate(num_choices=Count('choices')).filter(
            num_choices__gte=REQUIRED_CHOICES)

    def get_invalid_questions(self):
        """Get invalid questions from the database
        in order for question to be invalid it must have at less
        than 2 choices

        Returns:
            [QuestionQuerySet] -- [A QuestionQuerySet]
        """
        return self.annotate(num_choices=Count('choices')).filter(
            num_choices__lte=REQUIRED_CHOICES)
