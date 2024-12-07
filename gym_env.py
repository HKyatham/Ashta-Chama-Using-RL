import gym
import pygame
from gym import spaces
import numpy as np
from board_updated import Board
from feat_StrategicPlayers_updated import StrategicPlayer


class StrategicGameEnv(gym.Env):
    def __init__(self):
        super(StrategicGameEnv, self).__init__()

        # Define the state space ? maybe 
        self.state_size = 16  # Example: 4 players x 4 pawns
        self.observation_space = spaces.Box(low=0, high=9, shape=(self.state_size,), dtype=np.int32)
        # Define the action space: Choose a pawn to move
        self.action_space = spaces.Discrete(4)  # Example: 4 pawns per player
        
        self.board_size = 9 
        self.cell_size = 60
        self.padding = 20
        self.screen = pygame.display.set_mode((self.board_size * self.cell_size + 2 * self.padding,
                                               self.board_size * self.cell_size + 2 * self.padding))
        pygame.display.set_caption("Ashta Chamma")
        pygame.display.set_caption("Strategic Game")

        # Define player start positions and colors
        player_start_positions = [
            [(0, 4), (1, 4)],  # Player 1, 4 pawns at the same position
            [(4, 0), (4, 1)],  # Player 2, 4 pawns at the same position
            [(8, 4), (7, 4)],  # Player 3, 4 pawns at the same position
            [(4, 8), (4, 7)]   # Player 4, 4 pawns at the same position
        ]
        colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0)]  # Red, Green, Blue, Yellow

        # initialize the board 
        self.board = Board()

        # initialize the RL agent and add to board 
        self.agent = StrategicPlayer(player_id=0, start_positions=player_start_positions[0], color=colors[0], strategy="RL")
        self.board.add_player(self.agent)

        # initialize the computer players and add to board 
        self.computer_players = [] 
        for i in range(3):
            player = StrategicPlayer(player_id=i + 1, start_positions=player_start_positions[i + 1], color=colors[i + 1], strategy="aggressive")
            self.computer_players.append(player)
            self.board.add_player(player)

        self.current_player_id = 0

    def reset(self):
        self.__init__()
        return self._get_observation()


    # TODO Fix 
    def step(self, action):
        # Perform action for the agent
        current_player = self.board.players[self.current_player_id]
        roll = self.board.diceRoll()
        chosen_move = self.board.move(current_player, action, roll)

        # Update the player's position
        current_player.update_position(action, chosen_move[3])

        # Check if the game ends
        winner = self.board.check_winner(chosen_move)
        done = winner is not None

        # Compute rewards
        reward = 0
        if winner:
            reward = 100 if winner.player_id == self.agent.player_id else -50

        # Cycle to the next player
        self.current_player_id = (self.current_player_id + 1) % len(self.board.players)

        return self._get_observation(), reward, done, {}

    def render(self, mode="human"):
        # Use Pygame to render the board
        self.board.render(self.screen)

    def _get_observation(self):
        # Flatten pawn positions and return as a numpy array
        positions = []
        for player in self.board.players:
            positions.extend(player.pawns)
        return np.array(positions, dtype=np.int32).flatten()