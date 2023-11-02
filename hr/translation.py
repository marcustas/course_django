from modeltranslation.translator import TranslationOptions, register

from hr.models import Department, Position


@register(Position)
class PositionTranslationOptions(TranslationOptions):
    fields = ('title', 'job_description')


@register(Department)
class DepartmentTranslationOptions(TranslationOptions):
    fields = ('name',)


