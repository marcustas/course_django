from rest_framework import serializers

from hr.constants import MAX_MONTH_DAYS


def validate_positive(value):
    if value < 0:
        raise serializers.ValidationError('This field must be positive.')


def validate_max_month_days(value):
    if value > MAX_MONTH_DAYS:
        raise serializers.ValidationError(f'Max month days is {MAX_MONTH_DAYS}.')