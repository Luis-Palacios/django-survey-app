from django.shortcuts import render
from .models import Question


def index(request):
    question = Question.objects.order_by('?').first()
    return render(request, 'surveys/index.html', {'question': question})
