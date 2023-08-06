from enum import StrEnum as DefaultStrEnum, auto, IntEnum
from typing import Any

__all__ = (
    "Role",
    "CharacterType", "SquadType",
    "School",
    "Position",
    "Weapon",
    "DamageType",
    "ArmorType",
    "TerrainMood"
)


class StrEnum(DefaultStrEnum):
    """Re-declaration of StrEnum, to set name with original string, not lowered value."""
    @staticmethod
    def _generate_next_value_(name: str, start: int, count: int, last_values: list[Any]) -> Any:
        return name


class Role(StrEnum):
    """
    Blue Archive Student Roles as enum.
    """
    Attacker = auto()
    Healer = auto()
    Supporter = auto()
    Tanker = auto()
    Tactical = auto()


class CharacterType(StrEnum):
    """
    Blue Archive Student Types as enum.
    """
    Special = auto()
    Striker = auto()


SquadType = CharacterType       # alias


class School(StrEnum):
    """
    Blue Archive Schools as enum.
    """
    Abydos = auto()
    Gehenna = auto()
    Hyakkiyako = auto()
    Millennium = auto()     # Yuuka~
    Shanhaijing = auto()
    Trinity = auto()


class Position(StrEnum):
    """
    Blue Archive Student Positions as enum.
    """
    Front = Forward = auto()
    Middle = auto()
    Back = auto()


class Weapon(StrEnum):
    """
    Blue Archive Student Weapons as enum.
    """
    AR = AssaultRifle = auto()
    GL = GrenadeLauncher = auto()
    HG = HandGun = auto()
    MG = MachineGun = auto()
    MT = Mortar = auto()        # Hibiki's gun.
    RF = Rifle = auto()
    RG = RailGun = auto()
    RL = RocketLauncher = auto()
    SG = ShotGun = auto()
    SMG = SubMachineGun = auto()
    SR = SniperRifle = auto()


class DamageType(StrEnum):
    """
    Blue Archive Student Damage Types as enum.
    """
    Explosion = auto()
    Mystic = auto()
    Pierce = Penetration = auto()

    def __class_getitem__(cls, item):
        try:
            super().__class_getitem__(item)
        except ValueError:
            m: DamageType | None = {
                "Penetration": DamageType.Pierce
            }.get(item, None)
            if m is None:
                raise ValueError(f"Either {cls.__name__} or alias does not exist for the value {item}.")
            return m


class ArmorType(StrEnum):
    """
    Blue Archive Student Armor Types as enum.
    """
    HeavyArmor = Heavy = "Heavy Armor"
    LightArmor = Light = "Light Armor"
    SpecialArmor = Special = "Special Armor"


class TerrainMood(IntEnum):
    """
    Terrain specific student mood data.
    Made using IntEnum, to compare & sort.
    """
    D = 0
    C = 1
    B = 2
    A = 3
    S = 4
    SS = 5
