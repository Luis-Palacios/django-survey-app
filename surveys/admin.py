from django.contrib import admin
from .models import Question, Choice


class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 3
    fields = ['choice_text', 'votes']
    readonly_fields = ['votes']


class QuestionAdmin(admin.ModelAdmin):
    list_display = ('question_text', 'choices_count', 'total_votes', 'pub_date')
    search_fields = ['question_text']
    fieldsets = [
        (None, {'fields': ['question_text']}),
        ('Date information', {'fields': ['pub_date']}),
    ]
    inlines = [ChoiceInline]


admin.site.register(Question, QuestionAdmin)
