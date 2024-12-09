import numpy as np
import random

class RLEnvironment:
    def __init__(self, board, rl_player_id):
        self.board = board
        self.rl_player_id = rl_player_id
        self.state = self.get_state()
        self.done = False

    def get_state(self):
        """Generate a state representation."""
        state = []
        for player in self.board.players:
            state.append(player.pawns)  # Use pawn positions as state features
        return tuple(map(tuple, state))  # Convert to hashable format

    def get_possible_actions(self):
        """Return possible actions for the RL player."""
        possible_moves = []
        rl_player = self.board.players[self.rl_player_id]
        roll = self.board.diceRoll()
        print(f"Dice roll: {roll} for Player {self.rl_player_id}")
        for pawn_index, pawn in enumerate(rl_player.pawns):
            if pawn is None:
                print(f"Pawn {pawn_index} for Player {self.rl_player_id} is None (already removed).")
                continue
            new_position = self.board.move(rl_player, pawn_index, roll)
            if new_position != pawn:  # Ensure the move is valid
                possible_moves.append((self.rl_player_id, rl_player.kill, pawn_index, new_position))
            else:
                print(f"Pawn {pawn_index} for Player {self.rl_player_id} cannot move with roll {roll}.")
        if not possible_moves:
            print(f"No possible moves for Player {self.rl_player_id} with roll {roll}.")
        return possible_moves



    def step(self, action):
        """Take an action and return the next state, reward, and done flag."""
        rl_player = self.board.players[self.rl_player_id]
        _, _, pawn_index, new_position = action
        rl_player.update_position(pawn_index, new_position)

        # Check for a winner
        winner = self.board.check_winner(action)
        if winner:
            self.done = True
            return self.get_state(), 1 if winner.player_id == self.rl_player_id else -1, self.done

        # No winner yet, neutral reward
        self.state = self.get_state()
        return self.state, 0, self.done

    def reset(self):
        """Reset the game for a new episode."""
        self.done = False
        self.state = self.get_state()
        for player in self.board.players:
            player.pawns = [(0, 4), (0, 4), (0, 4), (0, 4)]  # Reset pawns
