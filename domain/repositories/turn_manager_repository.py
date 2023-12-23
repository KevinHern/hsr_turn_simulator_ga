import math
from abc import ABC, abstractmethod
from functools import reduce

from domain.repositories.status_modifier_repository import StatusModifierRepositoryImpl
from utils.numeric_constants import DEFAULT_ACTION_GAUGE_VALUE


class TurnManagerRepositoryContract(ABC):

	@abstractmethod
	def calculate_base_action_value(self, character):
		pass

	@abstractmethod
	def calculate_current_action_gauge(self, character):
		pass

	@abstractmethod
	def initialize_turn_order(self, characters):
		pass

	@abstractmethod
	def advance_action_value(self, characters, action_value_consumption):
		pass

	@abstractmethod
	def initialize_character_turn(self, characters):
		pass

	@abstractmethod
	def back_to_turn_queue(self, characters, character):
		pass

	@abstractmethod
	def format_turn_queue(self, characters):
		pass


class TurnManagerRepositoryImpl(TurnManagerRepositoryContract):

	def __init__(self):
		self.status_modifier_repository = StatusModifierRepositoryImpl()

	def calculate_base_action_value(self, character):
		return math.ceil(DEFAULT_ACTION_GAUGE_VALUE / character.base_speed)

	def calculate_current_action_gauge(self, character):
		return math.ceil(character.current_action_value * character.current_base_speed)

	def initialize_turn_order(self, characters):
		for character in characters:
			character.current_speed = character.base_speed

			base_action_value = self.calculate_base_action_value(character=character)

			character.base_action_value = base_action_value
			character.current_action_value = base_action_value

		characters.sort(key=lambda x: x.current_action_value, reverse=False)

	def advance_action_value(self, characters, action_value_consumption):
		for character in characters:
			character.current_action_value -= action_value_consumption

	def initialize_character_turn(self, characters):
		self.advance_action_value(characters=characters, action_value_consumption=characters[0].current_action_value)

		return characters.pop(0)

	def back_to_turn_queue(self, characters, character):
		self.status_modifier_repository.advance_status_modifiers(character=character)

		character.reset_action_value()

		characters.append(character)

		characters.sort(key=lambda x: x.current_action_value, reverse=False)

	def format_turn_queue(self, characters):
		return "Next in line: " + reduce(
			lambda x, y: x + "\n" + y,
			map(
				lambda x: "{} [AV: {}, Base Speed: {}, Current Speed: {}, Turn Counter {}, Energy Counter: {}, Energy Cap: {}]".format(
					x.name, x.current_action_value, x.base_speed, x.current_speed, x.turn_counter, x.energy_counter, x.energy_cap),
				characters
			))
