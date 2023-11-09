from modeltranslation.translator import (
    TranslationOptions,
    translator,
)

from hr.models import Position


class PositionTranslationOptions(TranslationOptions):
    fields = ('title', 'job_description')


class DepartmentTranslationOptions(TranslationOptions):
    fields = ('name',)


translator.register(Position, PositionTranslationOptions)
translator.register(Department, DepartmentTranslationOptions)
