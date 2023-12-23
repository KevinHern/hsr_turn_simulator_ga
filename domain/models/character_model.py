import math
import random
from abc import ABC

from utils.enums import CharacterType, MoveType
from utils.numeric_constants import DEFAULT_ACTION_GAUGE_VALUE


class CharacterModel(ABC):

	def __init__(self, playable_id, name, base_speed, character_type, status_modifiers):
		# Immutable Variables
		self.playable_id = playable_id
		self.name = name
		self.base_speed = base_speed
		self.character_type = character_type

		# Mutable Variables
		self.status_modifiers = status_modifiers
		self.current_speed = base_speed
		self.current_action_value = 0
		self.action_gauge_forward = 0.0
		self.action_gauge_delay = 0.0
		self.turn_counter = 0

	def reset_action_value(self):
		self.turn_counter += 1
		self.current_action_value = \
			math.ceil(DEFAULT_ACTION_GAUGE_VALUE * (1 - self.action_gauge_forward + self.action_gauge_delay) / self.current_speed)

	def __eq__(self, other):
		return self.playable_id == other.playable_id

	def __hash__(self):
		return hash(self.playable_id)


class PlayableCharacterModel(CharacterModel):

	def __init__(self, playable_id, character_role, name, base_speed, status_modifiers, energy_cap, moves, energy_regeneration_modifier=0):
		super().__init__(
			playable_id=playable_id,
			name="Playable Character" if name is None else name,
			base_speed=base_speed,
			character_type=CharacterType.PLAYABLE,
			status_modifiers=status_modifiers,
		)

		assert len(moves) == 3, "Character must have: basic, skill and ultimate moves in their kit"

		self.character_role = character_role

		self.energy_counter = 0
		self.energy_cap = energy_cap
		self.energy_regeneration_modifier = energy_regeneration_modifier

		self.moves = moves

	# TODO: Modify this move later to include fitness
	def execute_action(self):
		# Choose an action
		while True:
			move = random.choice(list(self.moves))

			if move.move_type == MoveType.BASIC_ATTACK or move.move_type == MoveType.SKILL:
				self.energy_counter += move.energy_regeneration
				return move
			elif self.energy_counter >= self.energy_cap:
				self.energy_counter = 0
				return move
			else:
				continue



