from enum import Enum


class BaseEnum(Enum):
    @classmethod
    def all_types(cls) -> list[str]:
        return [pack_type.value for pack_type in cls]

    @classmethod
    def from_string(cls, value: str):
        for pack_type in cls:
            if pack_type.value == value:
                return pack_type
        raise ValueError(value)