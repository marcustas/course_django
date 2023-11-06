from modeltranslation.translator import (
    TranslationOptions,
    translator,
    register,
)

from hr.models import Position,Department


class PositionTranslationOptions(TranslationOptions):
    fields = ('title', 'job_description')


translator.register(Position, PositionTranslationOptions)


@register(Department)
class DepartmentTranslationOptions(TranslationOptions):
    fields = ('name',)
