from django.contrib import admin
from django.utils import timezone
from material.decorators import register
from material.options import MaterialModelAdmin
from material.sites import site

from .models import Choice, Question


class EnoughChoicesFilter(admin.SimpleListFilter):
    title = 'Has enough choices'
    parameter_name = 'choices'

    def lookups(self, request, model_admin):
        return (('y', 'Yes'), ('n', 'No'))

    def queryset(self, request, queryset):
        if self.value() == 'y':
            return queryset.get_valid_questions()

        if self.value() == 'n':
            return queryset.get_invalid_questions()


class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 0
    min_num = 2
    fields = ['choice_text', 'votes']
    readonly_fields = ['votes']

    def get_formset(self, request, obj=None, **kwargs):
        formset = super().get_formset(request, obj=None, **kwargs)
        formset.validate_min = True
        return formset


@register(Question)
class QuestionAdmin(MaterialModelAdmin):
    icon_name = 'question_answer'
    list_display = ('question_text', 'choices_count', 'has_enough_choices',
                    'pub_date')
    search_fields = ['question_text']
    inlines = [ChoiceInline]
    list_filter = ['pub_date', EnoughChoicesFilter]

    def get_changeform_initial_data(self, request):
        return {'pub_date': timezone.now()}


site.site_header = 'Surveys Demo'
