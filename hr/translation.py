from modeltranslation.translator import (
    TranslationOptions,
    translator,
)

from hr.models import Position


class PositionTranslationOptions(TranslationOptions):
    fields = ('title', 'job_description')


translator.register(Position, PositionTranslationOptions)
