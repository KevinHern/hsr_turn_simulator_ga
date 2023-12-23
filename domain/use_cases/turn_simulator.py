from domain.models.character_model import PlayableCharacterModel
from domain.models.character_move_model import BasicMoveModel, SkillMoveModel, UltimateMoveModel
from domain.repositories.status_modifier_repository import StatusModifierRepositoryImpl
from domain.repositories.turn_manager_repository import TurnManagerRepositoryImpl
from utils.enums import CharacterRole


class TurnSimulator:
	def __init__(self):
		self.status_manager = StatusModifierRepositoryImpl()
		self.turn_manager = TurnManagerRepositoryImpl()

		self.player_party = set([])
		self.enemy_party = set([])
		self.characters = set([])

	def setup_party(self):
		# Playable characters
		self.player_party = {PlayableCharacterModel(
			playable_id=1,
			character_role=CharacterRole.DPS,
			name="PC1",
			base_speed=90,
			status_modifiers=set([]),
			energy_cap=70,
			moves={
				BasicMoveModel(energy_regeneration=15),
				SkillMoveModel(energy_regeneration=30, effects=None),
				UltimateMoveModel(energy_regeneration=30, effects=None),
			},
		), PlayableCharacterModel(
			playable_id=2,
			character_role=CharacterRole.TANK,
			name="PC2",
			base_speed=100,
			status_modifiers=set([]),
			energy_cap=60,
			moves={
				BasicMoveModel(energy_regeneration=15),
				SkillMoveModel(energy_regeneration=30, effects=None),
				UltimateMoveModel(energy_regeneration=30, effects=None),
			},
		), PlayableCharacterModel(
			playable_id=3,
			character_role=CharacterRole.SUPPORTER,
			name="PC3",
			base_speed=120,
			status_modifiers=set([]),
			energy_cap=50,
			moves={
				BasicMoveModel(energy_regeneration=15),
				SkillMoveModel(energy_regeneration=30, effects=None),
				UltimateMoveModel(energy_regeneration=30, effects=None),
			},
		)}

		# Enemy team

		self.characters = list(self.player_party.union(self.enemy_party))

	def run_simulation(self, action_turns=10):
		# Init
		self.setup_party()
		self.turn_manager.initialize_turn_order(characters=self.characters)

		print("INITIAL SETUP\n{}\n\n".format(self.turn_manager.format_turn_queue(characters=self.characters)))

		for turn in range(action_turns):
			# Advance queue based on action value
			actor = self.turn_manager.initialize_character_turn(characters=self.characters)

			print("TURN #{}\n\n{}\n\n".format(turn + 1, self.turn_manager.format_turn_queue(characters=self.characters)))

			# Character performs action
			selected_move = actor.execute_action()
			print(selected_move.to_string())

			# Return character on queue
			self.turn_manager.back_to_turn_queue(characters=self.characters, character=actor)

			print("END OF TURN #{}\n\n{}\n\n".format(turn + 1, self.turn_manager.format_turn_queue(characters=self.characters)))
