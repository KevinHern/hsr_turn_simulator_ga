import math
from abc import ABC, abstractmethod

from domain.models.status_modifier_model import StatusModifierModel
from utils.enums import Stat, StatusModifierType
from utils.numeric_constants import DEFAULT_ACTION_GAUGE_VALUE


class StatusModifierRepositoryContract(ABC):

	@abstractmethod
	def apply_stat_modification(self, character, status_modifier):
		pass

	@abstractmethod
	def add_status_modifiers(self, character, modifiers):
		pass

	@abstractmethod
	def advance_status_modifiers(self, character):
		pass


class StatusModifierRepositoryImpl(StatusModifierRepositoryContract):

	def apply_stat_modification(self, character, status_modifier):
		match character.stat:
			case Stat.SPEED:
				new_speed = math.ceil(character.current_speed + StatusModifierModel.calculate_stat_change(
					stat_value=character.base_speed,
					status_modifier_model=status_modifier
				))

				character.current_action_value = math.ceil(
					character.current_action_value * character.current_speed / new_speed)

				character.current_speed = new_speed

			case Stat.ACTION_GAUGE:
				if status_modifier.status_modifier_type == StatusModifierType.BUFF:
					character.action_gauge_forward += StatusModifierModel.calculate_stat_change(
						stat_value=0, status_modifier_model=status_modifier
					)
				else:
					character.action_gauge_delay += StatusModifierModel.calculate_stat_change(
						stat_value=0, status_modifier_model=status_modifier, inverse_modifier=True
					)

				current_action_gauge = character.current_action_value * character.base_speed
				modifier_action_gauge = DEFAULT_ACTION_GAUGE_VALUE * (
							character.current_action_value - character.action_gauage_delay)
				new_action_gauge = max(0, current_action_gauge - modifier_action_gauge)

				character.current_action_value = math.ceil(new_action_gauge / character.current_speed)

			case default:
				raise Exception(
					"Status Modifier Repository Impl: Unimplemented stat change for {}".format(status_modifier.stat))

	def add_status_modifiers(self, character, modifiers):
		for modifier in modifiers:
			if modifier in character.status_modifiers:
				character.status_modifiers.remove(modifier)
				character.status_modifiers.add(modifier)
			else:
				character.status_modifiers.add(modifier)
				self.apply_stat_modification(character=character, status_modifier=modifier)

	def advance_status_modifiers(self, character):
		for modifier in character.status_modifiers:
			modifier.active_character_turns -= 1

			if modifier.active_character_turns == 0:
				self.apply_stat_modification(character=character, status_modifier=modifier)
