import pygame
import sys

pygame.init()
pygame.mixer.init()

WIDTH, HEIGHT = 800,800
SQUARE_SIZE = WIDTH//8

#Colors
WHITE =(255, 255, 255)
BLACK =(0,0,0)
BLUE=(111,180,255)
BEIGE =(255, 249,199)
YELLOW =(255,232,104)

#Screen
screen = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Chess Wizard")

# Load sounds
move_sound = pygame.mixer.Sound('sounds/move.mp3')
capture_sound = pygame.mixer.Sound("sounds/capture.mp3")
promotion_sound = pygame.mixer.Sound("sounds/promotion.mp3")
game_over_sound = pygame.mixer.Sound('sounds/game_over.mp3')

font = pygame.font.SysFont("Arial", 48)

#Chess peices
class ChessPiece:
    def __init__(self,color,type,image):
        self.color = color
        self.type = type
        self.image = pygame.image.load(image)
        self.image = pygame.transform.scale(self.image, (SQUARE_SIZE,SQUARE_SIZE))
        self.has_moved = False

#The board 
board = [[None for _ in range(8)] for _ in range (8)]

#current
current_player='white'

#slected peice
selected_peice = None
selected_pos = None

def init_board():
    # Pawns
    for col in range(8):
        board[1][col] = ChessPiece('black', 'pawn', 'images/black_pawn.png')
        board[6][col] = ChessPiece('white', 'pawn', 'images/white_pawn.png')

    # Rooks
    board[0][0] = board[0][7] = ChessPiece('black', 'rook', 'images/black_rook.png')
    board[7][0] = board[7][7] = ChessPiece('white', 'rook', 'images/white_rook.png')

    # Knights
    board[0][1] = board[0][6] = ChessPiece('black', 'knight', 'images/black_knight.png')
    board[7][1] = board[7][6] = ChessPiece('white', 'knight', 'images/white_knight.png')

    # Bishops
    board[0][2] = board[0][5] = ChessPiece('black', 'bishop', 'images/black_bishop.png')
    board[7][2] = board[7][5] = ChessPiece('white', 'bishop', 'images/white_bishop.png')

    # Queens
    board[0][3] = ChessPiece('black', 'queen', 'images/black_queen.png')
    board[7][3] = ChessPiece('white', 'queen', 'images/white_queen.png')

    # Kings
    board[0][4] = ChessPiece('black', 'king', 'images/black_king.png')
    board[7][4] = ChessPiece('white', 'king', 'images/white_king.png')

#drawing the board
def draw_board():
    for row in range (8):
        for col in range (8):
               color = BEIGE if (row + col) % 2 ==0 else BLUE
               pygame.draw.rect(screen,color,(col*SQUARE_SIZE, row*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

    if selected_pos:
        pygame.draw.rect(screen, YELLOW, (selected_pos[1]*SQUARE_SIZE, selected_pos[0]*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

#drawing the peiee
def draw_piece():
    for row in range (8):
        for col in range (8):
             piece = board[row][col]
             if piece:
                  screen.blit(piece.image,(col*SQUARE_SIZE, row*SQUARE_SIZE))

#the pieces moves
def possible_moves(piece, row,col):
    moves = []
    if piece.type == 'pawn':
         direction = -1 if piece.color == 'white' else 1
         if 0 <= row + direction < 8 and board[row + direction][col] is None:
              moves.append((row +direction, col))
              if (piece.color == 'white' and row == 6) or (piece.color == 'black' and row ==1):
                   if board[row +2*direction][col] is None:
                        moves.append((row +2*direction, col))
         for dc in  [-1, 1] :
              if 0 <= row + direction <8 and 0 <= col + dc < 8:
                   if board [row + direction][col + dc] and board [row + direction] [col + dc].color != piece.color:
                        moves.append((row + direction, col + dc))

    elif piece.type == 'rook':
         #down, up, right, left
         for dr, dc in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
              r, c = row + dr, col + dc
              while 0 <= r <8 and 0 <= c < 8:
                   if board[r][c] is None:
                        moves.append((r,c))
                   elif board[r][c].color != piece.color:
                        moves.append((r,c))
                        break
                   else:
                        break
                   r, c = r +dr, c + dc

    elif piece.type == 'knight':
         #- = up,left / + = down,right
         for dr, dc in [(-2, -1), (-2, 1),(-1, -2), (-1, 2),(1, -2), (1, 2),(2, -1), (2, 1)]:
              r, c = row + dr, col + dc
              if 0 <= r <8 and 0 <= c <8 and (board[r][c] is None or board[r][c].color != piece.color):
                   moves.append((r, c))

    elif piece.type == 'bishop':
         for dr, dc in [(1, 1), (1, -1), (-1, 1), (-1, -1)]:
              r, c = row + dr, col + dc
              while 0 <= r < 8 and 0 <= c < 8:
                if board[r][c] is None:
                    moves.append((r, c))
                elif board[r][c].color != piece.color:
                    moves.append((r, c))
                    break
                else:
                    break
                r, c = r +dr, c + dc

    elif piece.type == 'queen':
         for dr, dc in [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (1, -1), (-1, 1), (-1, -1)]:
              r, c = row + dr, col + dc
              while 0 <= r < 8 and 0 <= c < 8:
                if board[r][c] is None:
                    moves.append((r, c))
                elif board[r][c].color != piece.color:
                    moves.append((r, c))
                    break
                else:
                    break
                r, c = r +dr, c + dc

    elif piece.type == 'king':
        #horizontal
        #vertical
        #diagonal
        for dr, dc in [(-1, -1), (-1, 0), (-1, 1),
                    (0, -1),          (0, 1),
                    (1, -1),  (1, 0), (1, 1)]:
            r, c = row + dr, col + dc
            if 0 <= r < 8 and 0 <= c < 8 and (board[r][c] is None or board[r][c].color != piece.color):
                    moves.append((r, c))

    return moves

#if the king in check
def is_check(color):
    king_pos = None
    for r in range(8):
        for c in range(8):
            if board[r][c] and board[r][c].color == color and board[r][c].type == 'king':
                king_pos = (r, c)
                break
        if king_pos:
            break

    # If king is missing, its a "check"
    if king_pos is None:
        return True

    for r in range(8):
        for c in range(8):
            piece = board[r][c]
            if piece and piece.color != color:
                if king_pos in possible_moves(piece, r, c):
                    return True
    return False

#if really checkmate
def game_over():
     for r in range(8):
          for c in range(8):
               piece = board[r][c]
               if piece and piece.color == current_player:
                    valid_moves = possible_moves(piece,r,c)
                    for move in valid_moves:
                         #try moving
                         temp = board[move[0]][move[1]]
                         board[move[0]][move[1]] = piece
                         board[r][c] = None
                         check = is_check(current_player)
                         #undo move
                         board[r][c] = piece
                         board[move[0]][move[1]] = temp
                         if not check:
                              return False
                         
     return True

def show_message(msg):
    overlay = pygame.Surface((WIDTH, HEIGHT))
    overlay.set_alpha(200)
    overlay.fill(BLACK)
    screen.blit(overlay, (0,0))
    text = font.render(msg, True, WHITE)
    rect = text.get_rect(center=(WIDTH//2, HEIGHT//2))
    screen.blit(text, rect)
    pygame.display.update()
    pygame.time.wait(3000)

#handling the mouse clicks
def handle_click(pos):
    global selected_peice, selected_pos, current_player

    c = pos[0] // SQUARE_SIZE
    r = pos[1] // SQUARE_SIZE

    piece = board[r][c]

    if selected_peice is None:
        if piece and piece.color == current_player:
            selected_peice = piece
            selected_pos = (r, c)
    else:
        if (r, c) in possible_moves(selected_peice, selected_pos[0], selected_pos[1]):
            # move the piece
            captured = board[r][c]
            board[r][c] = selected_peice
            board[selected_pos[0]][selected_pos[1]] = None
            selected_peice.has_moved = True

            if captured:
                if captured.type == 'king':
                    draw_board()
                    draw_piece()
                    pygame.display.update()
                    pygame.time.wait(300) 
                    game_over_sound.play()
                    show_message(f"{captured.color.capitalize()} King captured! Game Over.")

                    pygame.quit()
                    sys.exit()
                else:
                    capture_sound.play()
            else:
                move_sound.play()

            # pawn promotion
            if selected_peice.type == 'pawn' and (r == 0 or r == 7):
                board[r][c] = ChessPiece(selected_peice.color, 'queen', f'images/{selected_peice.color}_queen.png')
                promotion_sound.play()

            # switch player
            current_player = 'black' if current_player == 'white' else 'white'

        selected_peice = None
        selected_pos = None


init_board()

running = True
while running:
    draw_board()
    draw_piece()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            handle_click(pygame.mouse.get_pos())

    pygame.display.update()

pygame.quit()
sys.exit()
