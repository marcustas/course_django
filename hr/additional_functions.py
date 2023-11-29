from django import forms


def validate_day_count(cleaned_data, day_type, max_count):
    day_types_ukr = {
        'SICK_DAY': "лікарняних",
        'HOLIDAY': "святкових",
    }
    day_type_ukr = day_types_ukr[day_type]
    days = [
        value
        for key, value in cleaned_data.items()
        if key.startswith('day_') and value == day_type
    ]
    if len(days) > max_count:
        error_message = f'Кількість {day_type_ukr} днів не повинна перевищувати {max_count}.'
        raise forms.ValidationError(error_message)
