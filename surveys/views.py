from django.shortcuts import render
from .models import Question


def index(request):
    question = Question.objects.all()[0]
    return render(request, 'surveys/index.html', {'question': question})
