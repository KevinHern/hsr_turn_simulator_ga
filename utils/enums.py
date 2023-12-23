from enum import Enum


class CharacterType(Enum):
    PLAYABLE = 1
    ENEMY = 2


class CharacterRole(Enum):
    DPS = 1
    TANK = 2
    SUPPORTER = 3


class StatusModifierType(Enum):
    BUFF = 1
    DEBUFF = 2


class Stat(Enum):
    NONE = 1
    SPEED = 2
    ACTION_GAUGE = 3


class MoveType(Enum):
    BASIC_ATTACK = 1
    SKILL = 2
    ULTIMATE = 3
