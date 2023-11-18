from modeltranslation.decorators import register
from modeltranslation.translator import (
    TranslationOptions,
    translator,
)

from hr.models import Position, Department


class PositionTranslationOptions(TranslationOptions):
    fields = ('title', 'job_description')


translator.register(Position, PositionTranslationOptions)


@register(Department)
class DepartmentTranslationOptions(TranslationOptions):
    fields = ('name', 'parent_department')
