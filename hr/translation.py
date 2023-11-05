from modeltranslation.translator import (
    TranslationOptions,
    translator,
    register,
)

from hr.models import Position, Department



@register(Department)
class DepartmentTranslationOptions(TranslationOptions):
    fields = ('name',)


class PositionTranslationOptions(TranslationOptions):
    fields = ('title', 'job_description')


translator.register(Position, PositionTranslationOptions)
