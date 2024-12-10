import pygame
import random

class Board:
    def __init__(self):
        self.board_size = 9
        self.safe_places = [(1, 4), (2, 2), (2, 6), (4, 1), (4, 4), (4, 7), (6, 2), (6, 6), (7, 4)]
        self.home_places = [(4, 8), (8, 4), (4, 0), (0, 4)]
        self.players = []
        self.cell_size = 60
        self.padding = 20
        self.paths = [
            # Paths for each player
            [(0, 4), (1, 4), (1, 3), (1, 2), (1, 1), (2, 1), (3, 1), (4, 1), (5, 1), (6, 1), (7, 1), (7, 2), (7, 3),
             (7, 4), (7, 5), (7, 6), (7, 7), (6, 7), (5, 7), (4, 7), (3, 7), (2, 7), (1, 7), (1, 6), (1, 5), (2, 6),
             (3, 6), (4, 6), (5, 6), (6, 6), (6, 5), (6, 4), (6, 3), (6, 2), (5, 2), (4, 2), (3, 2), (2, 2), (2, 3),
             (2, 4), (2, 5), (3, 5), (4, 5), (5, 5), (5, 4), (5, 3), (4, 3), (3, 3), (3, 4), (4, 4)],
            [(4, 0), (4, 1), (5, 1), (6, 1), (7, 1), (7, 2), (7, 3), (7, 4), (7, 5), (7, 6), (7, 7), (6, 7), (5, 7),
             (4, 7), (3, 7), (2, 7), (1, 7), (1, 6), (1, 5), (1, 4), (1, 3), (1, 2), (1, 1), (2, 1), (3, 1), (2, 2),
             (2, 3), (2, 4), (2, 5), (2, 6), (3, 6), (4, 6), (5, 6), (6, 6), (6, 5), (6, 4), (6, 3), (6, 2), (5, 2),
             (4, 2), (3, 2), (3, 3), (3, 4), (3, 5), (4, 5), (5, 5), (5, 4), (5, 3), (4, 3), (4, 4)],
            [(8, 4), (7, 4), (7, 5), (7, 6), (7, 7), (6, 7), (5, 7), (4, 7), (3, 7), (2, 7), (1, 7), (1, 6), (1, 5),
             (1, 4), (1, 3), (1, 2), (1, 1), (2, 1), (3, 1), (4, 1), (5, 1), (6, 1), (7, 1), (7, 2), (7, 3), (6, 2),
             (5, 2), (4, 2), (3, 2), (2, 2), (2, 3), (2, 4), (2, 5), (2, 6), (3, 6), (4, 6), (5, 6), (6, 6), (6, 5),
             (6, 4), (6, 3), (5, 3), (4, 3), (3, 3), (3, 4), (3, 5), (4, 5), (5, 5), (5, 4), (4, 4)],
            [(4, 8), (4, 7), (3, 7), (2, 7), (1, 7), (1, 6), (1, 5), (1, 4), (1, 3), (1, 2), (1, 1), (2, 1), (3, 1),
             (4, 1), (5, 1), (6, 1), (7, 1), (7, 2), (7, 3), (7, 4), (7, 5), (7, 6), (7, 7), (6, 7), (5, 7), (6, 6),
             (6, 5), (6, 4), (6, 3), (6, 2), (5, 2), (4, 2), (3, 2), (2, 2), (2, 3), (2, 4), (2, 5), (2, 6), (3, 6),
             (4, 6), (5, 6), (5, 5), (5, 4), (5, 3), (4, 3), (3, 3), (3, 4), (3, 5), (4, 5), (4, 4)],
        ]
        pygame.init()
        self.screen = pygame.display.set_mode(
            (self.board_size * self.cell_size + 2 * self.padding,
             self.board_size * self.cell_size + 2 * self.padding)
        )
        pygame.display.set_caption("Ashta Chamma")

    def add_player(self, player):
        self.players.append(player)

    def dice_roll(self):
        return random.choice([1, 2, 3, 4, 8])

    def move(self, player, pawn_index, roll):
        current_pos = player.pawns[pawn_index]
        if current_pos not in self.paths[player.player_id]:
            return current_pos

        current_index = self.paths[player.player_id].index(current_pos)
        new_index = current_index + roll

        if new_index >= len(self.paths[player.player_id]):
            return current_pos

        return self.paths[player.player_id][new_index]

    def render(self):
        self.screen.fill((0, 0, 0))
        for i in range(self.board_size):
            for j in range(self.board_size):
                rect = pygame.Rect(
                    self.padding + j * self.cell_size,
                    self.padding + i * self.cell_size,
                    self.cell_size,
                    self.cell_size
                )
                pygame.draw.rect(self.screen, (240, 207, 174), rect)
                pygame.draw.rect(self.screen, (255, 255, 255), rect, 2)

        for player in self.players:
            for pawn in player.pawns:
                if pawn is None:
                    continue
                x, y = pawn
                center_x = self.padding + y * self.cell_size + self.cell_size // 2
                center_y = self.padding + x * self.cell_size + self.cell_size // 2
                pygame.draw.circle(self.screen, player.color, (center_x, center_y), 10)

        pygame.display.flip()
