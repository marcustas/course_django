from modeltranslation.translator import (
    TranslationOptions,
    register,
    translator,
)

from hr.models import Department, Position


class PositionTranslationOptions(TranslationOptions):
    fields = ('title', 'job_description')


@register(Department)
class DepartmentTranslationOptions(TranslationOptions):
    fields = ('name',)


translator.register(Position, PositionTranslationOptions)
