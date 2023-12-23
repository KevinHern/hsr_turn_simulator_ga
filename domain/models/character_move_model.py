from abc import ABC

from utils.enums import MoveType
from utils.numeric_constants import BASIC_ATTACK_ID, ULTIMATE_ABILITY_ID, SKILL_ABILITY_ID
from utils.text_constants import BASIC_ATTACK_NAME, SKILL_ABILITY_NAME, ULTIMATE_ABILITY_NAME


# TODO: Add "how much fitness" the move adds when used, depending on the role and also effects
class CharacterMoveModel(ABC):

	def __init__(self, move_id, name, move_type, energy_regeneration, effects):
		self.move_id = move_id
		self.name = name
		self.move_type = move_type
		self.energy_regeneration = energy_regeneration
		self.effects = effects

	def __eq__(self, other):
		return self.move_id == other.move_id

	def __hash__(self):
		return hash(self.move_id)

	def to_string(self):
		return "Move type: {}".format(self.move_type)


class BasicMoveModel(CharacterMoveModel):
	def __init__(self, energy_regeneration):
		super().__init__(
			move_id=BASIC_ATTACK_ID, name=BASIC_ATTACK_NAME, energy_regeneration=energy_regeneration, effects=None,
			move_type=MoveType.BASIC_ATTACK
		)


class SkillMoveModel(CharacterMoveModel):
	def __init__(self, energy_regeneration, effects):
		super().__init__(
			move_id=SKILL_ABILITY_ID, name=SKILL_ABILITY_NAME, energy_regeneration=energy_regeneration, effects=effects,
			move_type=MoveType.SKILL
		)


class UltimateMoveModel(CharacterMoveModel):
	def __init__(self, energy_regeneration, effects):
		super().__init__(
			move_id=ULTIMATE_ABILITY_ID, name=ULTIMATE_ABILITY_NAME, energy_regeneration=energy_regeneration, effects=effects,
			move_type=MoveType.ULTIMATE
		)
