from abc import ABC

from utils.enums import StatusModifierType


class StatusModifierModel(ABC):
	def __init__(self, status_id, status_modifier_type, stat, active_character_turns, multiplicative_bonus, flat_bonus, custom_bonus):
		# Fixed Variables
		self.status_id = status_id
		self.status_modifier_type = status_modifier_type
		self.stat = stat
		self.multiplicative_bonus = multiplicative_bonus
		self.flat_bonus = flat_bonus
		self.custom_bonus = custom_bonus

		# Mutable Variables
		self.active_character_turns = active_character_turns

	def __eq__(self, other):
		return self.status_id == other.status_id

	@staticmethod
	def modifier(status_modifier_model, inverse):
		return (-1 if status_modifier_model.status_modifier_type == StatusModifierType.DEBUFF else 1) * \
			   (-1 if inverse else 1) * (1 if status_modifier_model.active_character_turns > 0 else -1)

	@staticmethod
	def calculate_stat_change(stat_value, status_modifier_model, inverse_modifier=False):
		assert not (status_modifier_model.multiplicative_bonus is None and status_modifier_model.flat_bonus is None and status_modifier_model.customBonus is None)

		multiplicative_bonus = stat_value * (0 if status_modifier_model.multiplicative_bonus is None else status_modifier_model.multiplicative_bonus)
		flat_bonus = 0 if status_modifier_model.flat_bonus is None else status_modifier_model.flat_bonus

		return StatusModifierModel.modifier(status_modifier_model=status_modifier_model, inverse=inverse_modifier) * \
			   ((multiplicative_bonus + flat_bonus) if status_modifier_model.customBonus is None else status_modifier_model.customBonus(stat_value))


class BuffStatusModel(StatusModifierModel):
	def __init__(self, status_id, stat, active_character_turns, multiplicative_bonus=None, flat_bonus=None,
				 custom_bonus=None):
		super().__init__(
			status_id=status_id,
			stat=stat,
			active_character_turns=active_character_turns,
			status_modifier_type=StatusModifierType.BUFF,
			multiplicative_bonus=multiplicative_bonus,
			flat_bonus=flat_bonus,
			custom_bonus=custom_bonus
		)


class DebuffStatusModel(StatusModifierModel):
	def __init__(self, status_id, stat, active_character_turns, multiplicative_bonus=None, flat_bonus=None,
				 custom_bonus=None):
		super().__init__(
			status_id=status_id,
			stat=stat,
			active_character_turns=active_character_turns,
			status_modifier_type=StatusModifierType.DEBUFF,
			multiplicative_bonus=multiplicative_bonus,
			flat_bonus=flat_bonus,
			custom_bonus=custom_bonus
		)
