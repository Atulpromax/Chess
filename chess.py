import pygame
import chess
import chess.svg
from io import BytesIO
import cairosvg

# Initialize Pygame
pygame.init()

# Screen dimensions
width, height = 512, 512
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Chess")

# Load chess board
board = chess.Board()

def render_board(board):
    # Convert the SVG to a PNG
    svg = chess.svg.board(board=board).encode("UTF-8")
    png = BytesIO()
    cairosvg.svg2png(bytestring=svg, write_to=png)
    png.seek(0)
    return pygame.image.load(png)

# Main game loop
running = True
selected_square = None
while running:
    screen.fill((255, 255, 255))
    chessboard_img = render_board(board)
    screen.blit(chessboard_img, (0, 0))
    pygame.display.flip()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()
            file = chess.FILE_NAMES[x // 64]
            rank = chess.RANK_NAMES[7 - (y // 64)]
            square = chess.parse_square(f"{file}{rank}")
            
            if selected_square is None:
                if board.piece_at(square):
                    selected_square = square
            else:
                move = chess.Move(from_square=selected_square, to_square=square)
                if move in board.legal_moves:
                    board.push(move)
                selected_square = None

    if board.is_game_over():
        print("Game over")
        running = False

pygame.quit()
