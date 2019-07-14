from django.contrib import admin
from django.utils import timezone
from material.options import MaterialModelAdmin
from material.decorators import register
from material.sites import site
from .models import Question, Choice


class ChoiceInline(admin.StackedInline):
    model = Choice
    extra = 2
    fields = ['choice_text', 'votes']
    readonly_fields = ['votes']


@register(Question)
class QuestionAdmin(MaterialModelAdmin):
    icon_name = 'question_answer'
    list_display = ('question_text', 'choices_count', 'total_votes',
                    'pub_date')
    search_fields = ['question_text']
    inlines = [ChoiceInline]

    def get_changeform_initial_data(self, request):
        return {'pub_date': timezone.now()}


site.site_header = 'Surveys Demo'
