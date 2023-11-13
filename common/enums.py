from enum import StrEnum


class WorkDayEnum(StrEnum):
    WORKING_DAY = 'Working Day'
    SICK_DAY = 'Sick Day'
    HOLIDAY = 'Holiday'
    WEEKEND = 'Weekend'
    UNPAID_DAY = 'Unpaid day'
    VACATION = 'Vacation day'
