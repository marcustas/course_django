from modeltranslation.translator import (
    TranslationOptions,
    translator,
)

from hr.models import (
    Company,
    Department,
    Position,
)


class PositionTranslationOptions(TranslationOptions):
    fields = ('title', 'job_description')


class CompanyTranslationOptions(TranslationOptions):
    fields = ('name', 'address')


class DepartmentTranslationOptions(TranslationOptions):
    fields = ('name', 'parent_department')


translator.register(Position, PositionTranslationOptions)
translator.register(Company, CompanyTranslationOptions)
translator.register(Department, DepartmentTranslationOptions)
