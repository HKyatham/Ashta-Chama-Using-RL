import pygame
from board_updated import Board
from feat_StrategicPlayers_updated import StrategicPlayer

# Initialize pygame
pygame.init()

# Set up the game window
screen_width, screen_height = 800, 600  # Adjust according to your game board size
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Strategic Game")

# Initialize the board
game_board = Board()

# Define player start positions and colors
start_positions = [
    [(0, 4), (0, 4), (0, 4), (0, 4)],  # Player 1, 4 pawns at the same position
    [(4, 0), (4, 0), (4, 0), (4, 0)],  # Player 2, 4 pawns at the same position
    [(8, 4), (8, 4), (8, 4), (8, 4)],  # Player 3, 4 pawns at the same position
    [(4, 8), (4, 8), (4, 8), (4, 8)]   # Player 4, 4 pawns at the same position
]

colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0)]  # Red, Green, Blue, Yellow
strategies = ["defensive", "aggressive", "defensive", "aggressive"]


# Add players to the game
for i in range(len(start_positions)):
    player = StrategicPlayer(player_id=i, start_positions=start_positions[i], color=colors[i], strategy=strategies[i])
    game_board.add_player(player)

players = game_board.players
# Game loop
running = True
clock = pygame.time.Clock()
current_player_id = 0  # Start with player 1

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Clear screen and render the board
    screen.fill((255, 255, 255))  # White background (or any color you prefer)
    game_board.render(screen)  # Pass the screen to the render function

    # Perform a move for the current player
    current_player = game_board.players[current_player_id]
    possible_moves = []
    roll = game_board.diceRoll()

    # Go through each pawn for the current player and calculate possible moves
    for pawn_index, pawn in enumerate(current_player.pawns):
        if pawn is None:
            continue
        # Instead of manually calculating the dice roll, use the move function from Board
        new_position = game_board.move(current_player, pawn_index, roll)
        if new_position != pawn:
            possible_moves.append((current_player_id, current_player.kill, pawn_index, new_position))

    # If there are possible moves, choose the first one (or the best one based on strategy)
    if possible_moves:
        print(possible_moves)
        chosen_move = current_player.decide_move(possible_moves, game_board.players)
        _,_, pawn_index, new_position = chosen_move
        print(chosen_move)
        current_player.update_position(pawn_index, new_position) # Update pawn's position


    # Check if the current player has won
    winner = game_board.check_winner(chosen_move)
    if winner:
        print(f"Player {winner.player_id} wins!")
        print(f"Player {winner.player_id} strategy: {winner.strategy}")
        print(f"The scores of all players are:{[player.score for player in game_board.players]}")
        running = False  # End the game

    # Cycle to the next player
    current_player_id = (current_player_id + 1) % len(game_board.players)

    # Cap the frame rate
    clock.tick(1)

    # Update the display
    pygame.display.flip()

# Quit the game
pygame.quit()

