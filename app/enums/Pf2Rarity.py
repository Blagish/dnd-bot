from app.enums.base import BaseEnum

class Rarity(BaseEnum):
    EMPTY = 'empty'
    COMMON = "common"
    UNCOMMON = "uncommon"
    RARE = "rare"
    UNIQUE = "unique"

    @classmethod
    def from_string(cls, value: str) -> 'Rarity':
        try:
            return super().from_string(value)
        except ValueError:
            return cls.EMPTY
