from rest_framework import serializers


def validate_positive(value):
    if value < 0:
        raise serializers.ValidationError('This field must be positive.')
