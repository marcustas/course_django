from modeltranslation.translator import register, TranslationOptions
from hr.models import Position, Department


@register(Position)
class PositionTranslationOptions(TranslationOptions):
    fields = ('title', 'job_description')


@register(Department)
class DepartmentTranslationOptions(TranslationOptions):
    fields = ('name', )
