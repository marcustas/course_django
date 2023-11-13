from hr.models import Position, Department
from modeltranslation.translator import (
    TranslationOptions,
    translator,
    register
)


class PositionTranslationOptions(TranslationOptions):
    fields = ('title', 'job_description')


@register(Department)
class DepartmentTranslationOptions(TranslationOptions):
    fields = ('name',)


translator.register(Position, PositionTranslationOptions)
