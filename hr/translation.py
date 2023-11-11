from modeltranslation.translator import (
    register,
    TranslationOptions,
    translator,
)

from hr.models import Position, Department


class PositionTranslationOptions(TranslationOptions):
    fields = ('title', 'job_description')


@register(Department)
class DepartmentTraslationOptions(TranslationOptions):
    fields = ('name',)


translator.register(Position, PositionTranslationOptions)
