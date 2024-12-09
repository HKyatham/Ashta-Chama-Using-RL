from board_updated import Board
from feat_StrategicPlayers_updated import StrategicPlayer
from rl_environment import RLEnvironment
from q_learning_agent import QLearningAgent

def train_rl_agent():
    rl_player_id = 0  # Train for Player 1
    rl_agent = QLearningAgent(action_space=[], exploration_rate=1.0)

    start_positions = [
        [(0, 4), (0, 4), (0, 4), (0, 4)],  # Player 1
        [(4, 0), (4, 0), (4, 0), (4, 0)],  # Player 2
        [(8, 4), (8, 4), (8, 4), (8, 4)],  # Player 3
        [(4, 8), (4, 8), (4, 8), (4, 8)]   # Player 4
    ]
    colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0)]

    # Training Phases
    phases = [
        {"opponents": ["random"] * 4, "games": 20},
        {"opponents": ["aggressive"] + ["random"] * 3, "games": 20},
        {"opponents": ["defensive"] + ["random"] * 3, "games": 20},
    ]

    for phase in phases:
        for _ in range(phase["games"]):
            game_board = Board()
            # Add RL player and opponents
            for i, strategy in enumerate(phase["opponents"]):
                strategy = strategy if i != rl_player_id else "random"
                player = StrategicPlayer(player_id=i, start_positions=start_positions[i], color=colors[i], strategy=strategy)
                game_board.add_player(player)

            env = RLEnvironment(game_board, rl_player_id)
            while not env.done:
                state = env.state
                possible_actions = env.get_possible_actions()
                action = rl_agent.choose_action(state, possible_actions)
                next_state, reward, done = env.step(action)
                next_possible_actions = env.get_possible_actions() if not done else []
                rl_agent.learn(state, action, reward, next_state, next_possible_actions)
                if done:
                    break
            rl_agent.decay_exploration()

    return rl_agent

def evaluate_rl_agent(rl_agent, strategy, games=10):
    wins = 0
    for _ in range(games):
        game_board = Board()
        # Add RL player and opponents
        for i in range(4):
            strat = strategy if i != rl_player_id else "random"
            player = StrategicPlayer(player_id=i, start_positions=start_positions[i], color=colors[i], strategy=strat)
            game_board.add_player(player)

        env = RLEnvironment(game_board, rl_player_id)
        while not env.done:
            state = env.state
            possible_actions = env.get_possible_actions()
            if not possible_actions:
                print(f"No possible actions for Player {env.rl_player_id} in state: {state}")
                continue  # Skip this turn

            action = rl_agent.choose_action(state, possible_actions)
            if action is None:  # Handle None action
                print("No action chosen. Skipping this turn.")
                continue

            next_state, reward, done = env.step(action)
            next_possible_actions = env.get_possible_actions() if not done else []
            rl_agent.learn(state, action, reward, next_state, next_possible_actions)


    print(f"RL agent won {wins}/{games} games against {strategy} strategy.")

# Train and evaluate the RL agent
rl_agent = train_rl_agent()
for strat in ["random", "aggressive", "defensive"]:
    evaluate_rl_agent(rl_agent, strat)
