from domain.use_cases.turn_simulator import TurnSimulator

if __name__ == '__main__':
    simulation = TurnSimulator()

    simulation.run_simulation(action_turns=15)
