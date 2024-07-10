from enum import Enum, auto


class TextDirection(Enum):
    TEXT_DIRECTION_UNKNOWN = auto()
    TEXT_DIRECTION_TOP = auto()
    TEXT_DIRECTION_BOTTOM = auto()
    TEXT_DIRECTION_LEFT = auto()
    TEXT_DIRECTION_RIGHT = auto()


str_to_text_direction = {
    "Unknown": TextDirection.TEXT_DIRECTION_UNKNOWN,
    "Top": TextDirection.TEXT_DIRECTION_TOP,
    "Bottom": TextDirection.TEXT_DIRECTION_BOTTOM,
    "Right": TextDirection.TEXT_DIRECTION_RIGHT
}

text_direction_to_str = {v: k for k, v in str_to_text_direction.items()}


def text_direction_str_to_enum(direction_str: str):
    return str_to_text_direction.get(direction_str, TextDirection.TEXT_DIRECTION_UNKNOWN)


def text_direction_enum_to_str(direction_enum: TextDirection):
    return text_direction_to_str.get(direction_enum, "Unknown")
