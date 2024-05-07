import pygame
import numpy as np
import json

# Définition des constantes
ROW_COUNT = 6
COLUMN_COUNT = 7
SQUARESIZE = 100
RADIUS = int(SQUARESIZE / 2 - 5)
WIDTH = COLUMN_COUNT * SQUARESIZE
HEIGHT = (ROW_COUNT + 1) * SQUARESIZE
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
BGCOLOR = (238, 229, 229)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
BGRESTART = (255, 120, 0)

# Création de la grille
def create_board():
    board = np.zeros((ROW_COUNT, COLUMN_COUNT))
    return board

# Placement d'un jeton dans la grille
def drop_piece(board, row, col, piece):
    board[row][col] = piece

# Vérification si la colonne est valide pour placer un jeton
def is_valid_location(board, col):
    return board[ROW_COUNT-1][col] == 0

# Trouver la première ligne vide dans une colonne
def get_next_open_row(board, col):
    for r in range(ROW_COUNT):
        if board[r][col] == 0:
            return r

# Affichage de la grille
def draw_board(board, screen):
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            pygame.draw.rect(screen, BLUE, (c*SQUARESIZE, r*SQUARESIZE+SQUARESIZE, SQUARESIZE, SQUARESIZE))
            pygame.draw.circle(screen, BGCOLOR, (int(c*SQUARESIZE+SQUARESIZE/2), int(r*SQUARESIZE+SQUARESIZE+SQUARESIZE/2)), RADIUS)
    
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            if board[r][c] == 1:
                pygame.draw.circle(screen, RED, (int(c*SQUARESIZE+SQUARESIZE/2), HEIGHT - int(r*SQUARESIZE+SQUARESIZE/2)), RADIUS)
            elif board[r][c] == 2:
                pygame.draw.circle(screen, YELLOW, (int(c*SQUARESIZE+SQUARESIZE/2), HEIGHT - int(r*SQUARESIZE+SQUARESIZE/2)), RADIUS)
    pygame.display.update()

# Vérification des lignes
def check_win_horizontal(board, piece):
    for r in range(ROW_COUNT):
        for c in range(COLUMN_COUNT - 3):
            if board[r][c] == piece and board[r][c+1] == piece and board[r][c+2] == piece and board[r][c+3] == piece:
                return True
    return False

# Vérification des colonnes
def check_win_vertical(board, piece):
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT - 3):
            if board[r][c] == piece and board[r+1][c] == piece and board[r+2][c] == piece and board[r+3][c] == piece:
                return True
    return False

# Vérification des diagonales (descendantes)
def check_win_diagonal_down(board, piece):
    for r in range(ROW_COUNT - 3):
        for c in range(COLUMN_COUNT - 3):
            if board[r][c] == piece and board[r+1][c+1] == piece and board[r+2][c+2] == piece and board[r+3][c+3] == piece:
                return True
    return False

# Vérification des diagonales (ascendantes)
def check_win_diagonal_up(board, piece):
    for r in range(3, ROW_COUNT):
        for c in range(COLUMN_COUNT - 3):
            if board[r][c] == piece and board[r-1][c+1] == piece and board[r-2][c+2] == piece and board[r-3][c+3] == piece:
                return True
    return False

# Vérification de la victoire
def check_win(board, piece):
    return (check_win_horizontal(board, piece) or
            check_win_vertical(board, piece) or
            check_win_diagonal_down(board, piece) or
            check_win_diagonal_up(board, piece))

# Initialisation de Pygame
pygame.init()

# Création de la fenêtre
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Initialisation de la police
pygame.font.init()
font = pygame.font.Font(None, 36)  # Choisir une police et une taille

# Définition des noms de joueurs
PLAYER_NAMES = ["Rouge", "Jaune"]

# Définition des variables pour le timer
START_TIME = pygame.time.get_ticks()
TURN_TIME = 20 * 1000  # 20 secondes en millisecondes

# Variable pour suivre le joueur actuel
current_player = 0

# Initialisation des statistiques des joueurs
player_stats = {name: {"victoires": 0, "temps": 0, "coups": 0} for name in PLAYER_NAMES}

# Compteur pour stocker le nombre de secondes restantes
remaining_seconds = TURN_TIME // 1000

# Fonction pour afficher le timer et mettre à jour l'affichage chaque seconde
def draw_timer():
    global remaining_seconds
    current_time = pygame.time.get_ticks()
    remaining_time = max(0, TURN_TIME - (current_time - START_TIME))
    global seconds
    seconds = remaining_time // 1000
    
    # Vérifier si le nombre de secondes a changé
    if seconds != remaining_seconds:
        pygame.display.flip()
        remaining_seconds = seconds
        pygame.display.update()  # Mettre à jour l'affichage
        
    timer_text = font.render(f"Temps restant : {remaining_seconds}", True, RED)
    screen.blit(timer_text, (10, 10))
    pygame.display.update()

# Fonction pour redémarrer le jeu
def restart_game():
    global board, game_over, current_player
    board = create_board()
    draw_board(board, screen)
    pygame.display.update()
    game_over = False
    current_player = 0

# Fonction pour afficher le bouton de redémarrage
def winner_button(player_name):
    pygame.draw.rect(screen, BGRESTART, (WIDTH // 4, 5, WIDTH // 2, 50))
    restart_text = font.render(f"{player_name} a gagné", True, BGCOLOR)
    screen.blit(restart_text, (WIDTH // 2 - 90, 15))
    pygame.display.update()

# Initialisation du jeu
restart_game()

# Fonction pour charger les statistiques à partir du fichier JSON
def load_stats_from_json(filename):
    with open(filename, "r") as file:
        stats = json.load(file)
    return stats

# Fonction pour afficher les statistiques des joueurs
def display_stats(stats):
    small_font = pygame.font.Font(None, 22)
    y_offset = 10  # Décalage vertical initial pour afficher les statistiques
    for player, data in stats.items():
        stats_text = f"{player}: Victoires : {data['victoires']} en {round(data['temps'] / 1000,1)} secondes Coups : {data['coups']}"
        stats_rendered = small_font.render(stats_text, True, BLACK)
        screen.blit(stats_rendered, (WIDTH - 400, y_offset))
        y_offset += 30  # Augmenter le décalage pour le prochain joueur
    pygame.display.update()

def time_passed():
    pygame.draw.rect(screen, BGRESTART, (WIDTH // 4, 5, WIDTH // 2, 50))
    restart_text = font.render(f"Temps écoulé...", True, BGCOLOR)
    screen.blit(restart_text, (WIDTH // 2 - 90, 15))
    pygame.display.update()

pygame.display.update()
pygame.display.flip()

# Boucle principale du jeu
while True:
    draw_timer()  # Afficher le timer
    draw_board(board, screen)  # Afficher la grille
    stats = load_stats_from_json("stats.json")
    display_stats(stats)  # Afficher les statistiques des joueurs
    # Vérifier si aucun coup n'a été joué pendant plus de 20 secondes

    # Rafraîchissement de l'écran
    pygame.display.update()
    pygame.display.flip()

    # Gestion des événements
    for event in pygame.event.get():
        # Rafraîchissement de l'écran
        pygame.display.update()
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

        if event.type == pygame.MOUSEMOTION:
            pygame.draw.rect(screen, BGCOLOR, (0, 0, WIDTH, SQUARESIZE))
            posx = event.pos[0]
            if current_player == 0:
                pygame.draw.circle(screen, RED, (posx, int(SQUARESIZE/2)), RADIUS)
            else:
                pygame.draw.circle(screen, YELLOW, (posx, int(SQUARESIZE/2)), RADIUS)
            pygame.display.update()
            

        if event.type == pygame.MOUSEBUTTONDOWN:
            pygame.draw.rect(screen, BGCOLOR, (0, 0, WIDTH, SQUARESIZE))
            posx = event.pos[0]
            col = int(np.floor(posx / SQUARESIZE))
            # Initialisation du compteur de coups
            total_moves = 0
            if is_valid_location(board, col):
                row = get_next_open_row(board, col)
                drop_piece(board, row, col, current_player + 1)
                total_moves += 1
                player_stats[PLAYER_NAMES[current_player]]["coups"] += total_moves

                if check_win(board, current_player + 1):
                    game_over = True
                    # Mise à jour des statistiques des joueurs
                    player_stats[PLAYER_NAMES[current_player]]["victoires"] += 1
                    # Mise à jour du temps total passé par le joueur
                    elapsed_time = pygame.time.get_ticks()
                    player_stats[PLAYER_NAMES[current_player]]["temps"] += elapsed_time
                current_player = (current_player + 1) % 2  # Passer au joueur suivant
                START_TIME = pygame.time.get_ticks()

                if seconds == 0:
                    player_stats[PLAYER_NAMES[current_player]]["victoires"] += 1
                    game_over = True
                    
            if game_over:
                if np.all(board != 0):
                    print("Egalité")
                    pygame.draw.rect(screen, BGRESTART, (WIDTH // 4, 5, WIDTH // 2, 50))
                    draw_text = font.render("Egalité", True, BGCOLOR)
                    screen.blit(draw_text, (WIDTH // 2 - 90, 15))
                else:
                    if seconds == 0:
                        time_passed()
                    else:
                        winner_button(PLAYER_NAMES[(current_player + 1) % 2])
                    # Enregistrement des statistiques dans un fichier JSON avant de quitter
                    with open("stats.json", "w") as file:
                        json.dump(player_stats, file)
                restart_game()
                pygame.time.wait(3000)
                    
