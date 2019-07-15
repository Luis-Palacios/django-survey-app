from django.shortcuts import reverse
from django.test import TestCase
from django.utils import timezone

from .constants import REQUIRED_CHOICES
from .models import Question


class QuestionQuerySetTest(TestCase):
    def test_random_question_fetch_question_on_init_data(self):
        question = Question.objects.get_random()

        self.assertIsNotNone(question)

    def test_all_question_on_init_data_are_valid(self):
        valid_questions_count = Question.objects.get_valid_questions().count()
        questions_count = Question.objects.count()
        invalid_questions_count = Question.objects.get_invalid_questions(
        ).count()

        self.assertEqual(valid_questions_count, questions_count)
        self.assertEqual(invalid_questions_count, 0)

    def test_invalid_questions_fetch_invalid_questions(self):
        self.addInvalidQuestion()

        invalid_question_count = Question.objects.get_invalid_questions(
        ).count()

        self.assertEqual(invalid_question_count, 1)

    def test_random_question_no_fetch_invalid_question(self):
        # Delete all questions
        Question.objects.all().delete()
        self.addInvalidQuestion()

        question = Question.objects.get_random()

        self.assertIsNone(question)

    def test_random_question_no_fetch_invalid_question_with_session(self):
        Question.objects.all().delete()
        self.addInvalidQuestion()

        question = Question.objects.get_random('init-data-session-key')

        self.assertIsNone(question)

    def test_random_question_fetch_none_if_no_questions(self):
        Question.objects.all().delete()

        question = Question.objects.get_random()

        self.assertIsNone(question)

    def addInvalidQuestion(self):
        invalid_question = Question(
            question_text='This is an invalid question',
            pub_date=timezone.now())
        invalid_question.save()


class QuestionViewTests(TestCase):
    def test_no_questions_answered_return_valid_question(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(response.context['question'])
        self.assertGreaterEqual(response.context['question'].choices.count(),
                                REQUIRED_CHOICES)

    def test_all_questions_answered_get_no_question(self):
        session = self.client.session
        session.save()

        questions = Question.objects.get_valid_questions()
        for question in questions:
            if question.choices.count() >= REQUIRED_CHOICES:
                question.choices.first().answers.create(
                    session_key=session.session_key)

        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertIsNone(response.context['question'])

    def test_some_questions_answered_get_valid_question(self):
        session = self.client.session
        session.save()

        questions = Question.objects.get_valid_questions().order_by('-id')
        for question in questions[0:questions.count() - 1]:
            if question.choices.count() >= REQUIRED_CHOICES:
                question.choices.first().answers.create(
                    session_key=session.session_key)

        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(response.context['question'])
        self.assertGreaterEqual(response.context['question'].choices.count(),
                                REQUIRED_CHOICES)

    def test_post_question_no_choice_selected(self):
        response = self.client.post(reverse('index'), {
            'question-id': 1,
        })

        self.assertEqual(response.status_code, 400)
        self.assertIsNotNone(response.context['error_message'])
