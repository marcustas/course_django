from modeltranslation.translator import (
    TranslationOptions,
    translator,
)

from hr.models import Position, Department


class PositionTranslationOptions(TranslationOptions):
    fields = ('title', 'job_description')


class DepartmentTranslationOptions(TranslationOptions):


translator.register(Position, PositionTranslationOptions)
translator.register(Department, DepartmentTranslationOptions)
