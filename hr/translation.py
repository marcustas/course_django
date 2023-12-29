from modeltranslation.translator import (
    TranslationOptions,
    translator,
    register,
)

from hr.models import Position, Department


class PositionTranslationOptions(TranslationOptions):
    fields = ('title', 'job_description')


@register(Department)
class DepartmentTranslationOptions(TranslationOptions):
    fields = ('name',)


translator.register(Position, PositionTranslationOptions)
