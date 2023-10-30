from enum import Enum, StrEnum, IntEnum, unique


class Color(Enum):
    RED = 1
    GREEN = 2
    BLUE = 3


class HttpMethod(StrEnum):
    GET = 'GET'
    POST = 'POST'
    PATCH = 'PATCH'


@unique
class PriorityLevel(IntEnum):
    LOW = 1
    MEDUIM = 2
    HIGH = 3


class ColorInfoMember:
    def __init__(self, value: int, default_value: int, description: str):
        self.value = value
        self.default_value = default_value
        self.description = description


class Colors2(Enum):
    RED = ColorInfoMember(value=1, default_value=0, description='Red color')


print(Colors2.RED)
