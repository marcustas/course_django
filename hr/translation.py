from modeltranslation.translator import (
    register,
    TranslationOptions,
    translator,
)

from hr.models import Position
from hr.models import Department


class PositionTranslationOptions(TranslationOptions):
    fields = ('title', 'job_description')


translator.register(Position, PositionTranslationOptions)


@register(Department)
class DepartmentTranslationOptions(TranslationOptions):
    fields = ('name',)
