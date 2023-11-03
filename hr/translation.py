from modeltranslation.translator import (
    TranslationOptions,
    translator,
)

from hr.models import (
    Position,
    Department,
    Company,
)


class PositionTranslationOptions(TranslationOptions):
    fields = ('title', 'job_description')


class CompanyTranslationOptions(TranslationOptions):
    fields = ('name', 'address')


class DepartmentTranslationOptions(TranslationOptions):
    fields = ('name', 'parent_department')


translator.register(Position, PositionTranslationOptions, Company, CompanyTranslationOptions, Department, DepartmentTranslationOptions)
