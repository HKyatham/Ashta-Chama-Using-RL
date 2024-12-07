import pygame
import random
from feat_StrategicPlayers_updated import StrategicPlayer

class Board:
    def __init__(self):
        self.board_size = 9  # 9x9 board
        self.safe_places = [(1, 4), (2, 2), (2, 6), (4, 1), (4, 4), (4, 7), (6, 2), (6, 6), (7, 4)]
        self.home_places = [(4, 8), (8, 4), (4, 0), (0, 4)]
        # self.board_state = [[None for _ in range(self.board_size)] for _ in range(self.board_size)]
        self.players = []  # List of Player objects
        self.cell_size = 60
        self.padding = 20
        self.paths = [
            [(0, 4), (1, 4), (1, 3), (1, 2), (1, 1), (2, 1), (3, 1), (4, 1), (5, 1), (6, 1), (7, 1), (7, 2), (7, 3),
             (7, 4), (7, 5), (7, 6), (7, 7), (6, 7), (5, 7), (4, 7), (3, 7), (2, 7), (1, 7), (1, 6), (1, 5),
             (2, 6), (3, 6), (4, 6), (5, 6), (6, 6), (6, 5), (6, 4), (6, 3), (6, 2), (5, 2), (4, 2), (3, 2), (2, 2),
             (2, 3), (2, 4), (2, 5), (3, 5), (4, 5), (5, 5), (5, 4), (5, 3), (4, 3), (3, 3), (3, 4), (4, 4)],

            [(4, 0), (4, 1), (5, 1), (6, 1), (7, 1), (7, 2), (7, 3), (7, 4), (7, 5), (7, 6), (7, 7), (6, 7), (5, 7),
             (4, 7), (3, 7), (2, 7), (1, 7), (1, 6), (1, 5), (1, 4), (1, 3), (1, 2), (1, 1), (2, 1), (3, 1),
             (2, 2), (2, 3), (2, 4), (2, 5), (2, 6), (3, 6), (4, 6), (5, 6), (6, 6), (6, 5), (6, 4), (6, 3), (6, 2),
             (5, 2), (4, 2), (3, 2), (3, 3), (3, 4), (3, 5), (4, 5), (5, 5), (5, 4), (5, 3), (4, 3), (4, 4)],

            [(8, 4), (7, 4), (7, 5), (7, 6), (7, 7), (6, 7), (5, 7), (4, 7), (3, 7), (2, 7), (1, 7), (1, 6), (1, 5),
             (1, 4), (1, 3), (1, 2), (1, 1), (2, 1), (3, 1), (4, 1), (5, 1), (6, 1), (7, 1), (7, 2), (7, 3),
             (6, 2), (5, 2), (4, 2), (3, 2), (2, 2), (2, 3), (2, 4), (2, 5), (2, 6), (3, 6), (4, 6), (5, 6), (6, 6),
             (6, 5), (6, 4), (6, 3), (5, 3), (4, 3), (3, 3), (3, 4), (3, 5), (4, 5), (5, 5), (5, 4), (4, 4)],

            [(4, 8), (4, 7), (3, 7), (2, 7), (1, 7), (1, 6), (1, 5), (1, 4), (1, 3), (1, 2), (1, 1), (2, 1), (3, 1),
             (4, 1), (5, 1), (6, 1), (7, 1), (7, 2), (7, 3), (7, 4), (7, 5), (7, 6), (7, 7), (6, 7), (5, 7),
             (6, 6), (6, 5), (6, 4), (6, 3), (6, 2), (5, 2), (4, 2), (3, 2), (2, 2), (2, 3), (2, 4), (2, 5), (2, 6),
             (3, 6), (4, 6), (5, 6), (5, 5), (5, 4), (5, 3), (4, 3), (3, 3), (3, 4), (3, 5), (4, 5), (4, 4)]
            ]
        pygame.init()

        self.screen = pygame.display.set_mode((self.board_size * self.cell_size + 2 * self.padding,
                                               self.board_size * self.cell_size + 2 * self.padding))
        pygame.display.set_caption("Ashta Chamma")

    # def _create_players(self):
    #     # Define starting positions and colors
    #     start_positions = [
    #         [(0, 4), (1, 4), (1, 3), (1, 2)],  # Player 1's pawns
    #         [(4, 0), (4, 1), (5, 1), (6, 1)],  # Player 2's pawns
    #         [(8, 4), (7, 4), (7, 5), (7, 6)],  # Player 3's pawns
    #         [(4, 8), (4, 7), (3, 7), (2, 7)],  # Player 4's pawns
    #     ]
    #     colors = ["red", "blue", "green", "yellow"]  # Player colors
    #
    #     players = []
    #     for i, start_pos in enumerate(start_positions):
    #         players.append(
    #             StrategicPlayer(player_id=i, start_positions=start_pos, color=colors[i], strategy="aggressive")
    #         )
    #     return players
    def add_player(self, player):
        """
        Add a player to the game.
        :param player: Player object
        """
        self.players.append(player)


    def diceRoll(self):
        """
        Simulate a dice roll with weighted probabilities.
        Possible outcomes are 1, 2, 3, 4, and 8.
        :return: The number rolled on the dice.
        """
        possibleNumbers = [1, 2, 3, 4, 5, 6]
        number = random.choices(population=possibleNumbers, k=1)[0]
        return number

    def move(self, player, pawn_index, roll):
        """Move a pawn for the player, based on the dice roll."""
        print(f"Player {player.player_id} rolled a {roll}")

        current_pos = player.pawns[pawn_index]
        # Ensure the current position is valid
        if current_pos not in self.paths[player.player_id]:
            print("Error: Pawn is not on the board!")
            return current_pos

        current_pos_index = self.paths[player.player_id].index(current_pos)
        new_pos_index = current_pos_index + roll

        # Handle out of bounds move
        if new_pos_index >= len(self.paths[player.player_id]):
            print("Move out of bounds!")
            return current_pos

        # Update the new position
        new_position = self.paths[player.player_id][new_pos_index]
        player.kill = False  # Reset kill flag

        # Check if the position is occupied by another pawn
        for opponent in self.players:
            if opponent != player:
                if new_position in opponent.pawns:
                    # Kill the opponent's pawn
                    killed_pawn_index = opponent.pawns.index(new_position)
                    player.kill = True
                    # Reset opponent pawn to their start position
                    opponent.pawns[killed_pawn_index] = self.paths[opponent.player_id][0]  # Reset to start position

        # Update the player's pawn position
        # player.update_position(pawn_index, new_position)
        return new_position

    def kill_check(self, best_move):
        """
        Check if the move captures an opponent's pawn.
        :param best_move: The move being considered.
        :return: Information about the captured pawn, if any.
        """
        player_id = best_move[0]
        pawn_id = best_move[1]
        position = best_move[2]
        kill = []
        if position not in self.safe_places:
            for player in self.players:
                if player.player_id != player_id:
                    for pawn_index, pawn in enumerate(player.pawns):
                        if position == pawn:
                            kill.append((player_id, player.player_id, pawn_index))

        return kill

    def update(self, best_move, kill):
        """
        Update the board state with the new pawn position and handle captures.
        :param best_move: The move to update the board with.
        :param kill: Information about the captured pawn, if any.
        """
        self.players[best_move[0]].pawns[best_move[1]] = best_move[2]
        if kill != None and len(kill) != 0:
            self.players[kill[1]].pawns[kill[2]] = self.paths[kill[1]][0]

    def check_winner(self,chosen_move):
        """
        Check if any player has moved all their pawns to their home.
        :return: The player who won, or None if no winner yet.
        """
        player_id,_,pawn_no,_ = chosen_move
        if self.players[player_id].pawns[pawn_no] == (4,4):
            self.players[player_id].pawns[pawn_no] = None
            self.players[player_id].score += 1
            if self.players[player_id].score == 3:
                return self.players[player_id]

        return None

    def render(self, screen):
        """
        Render the board and the current positions of all pawns.
        """
        screen.fill((0, 0, 0))  # Fill the background with black

        # Draw the board
        for i in range(self.board_size):
            for j in range(self.board_size):
                rect = pygame.Rect(
                    self.padding + j * self.cell_size,
                    self.padding + i * self.cell_size,
                    self.cell_size,
                    self.cell_size
                )

                # Check if the cell is a safe place
                if (i, j) in self.safe_places:
                    pygame.draw.rect(screen, (240, 207, 174), rect)
                    cross = pygame.image.load("assets/icons/cross.png")
                    cross = pygame.transform.scale(cross, (53, 53))
                    screen.blit(cross, rect.topleft)  # Draw the cross icon in the safe place
                # Check if the cell is a home place
                elif (i, j) in self.home_places:
                    home_color_index = self.home_places.index((i, j))
                    home_colors = [(255, 255, 255), (200, 200, 200), (180, 180, 180), (220, 220, 220)]
                    pygame.draw.rect(screen, home_colors[home_color_index], rect)
                else:
                    pygame.draw.rect(screen, (240, 207, 174), rect)

                pygame.draw.rect(screen, (255, 255, 255), rect, 2)  # Border

        # Render each player's pawns
        for player in self.players:
            for pawn in player.pawns:
                if pawn is None:
                    continue
                # Convert pawn position from grid coordinates to pixel coordinates
                # Assuming pawn is a tuple of (row, col)
                row, col = pawn
                pawn_position = (self.padding + col * self.cell_size + self.cell_size // 2,  # X coordinate
                                 self.padding + row * self.cell_size + self.cell_size // 2)  # Y coordinate
                pygame.draw.circle(screen, player.color, pawn_position, 10)  # Render pawns as circles



