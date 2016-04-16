import pygame, sys, random
from pygame.locals import *

class Grille:
    def __init__(self, x, y):
        self.matrice = [[ESPACE for i in range(y)] for j in range(x)]
        self.longueur = x
        self.largeur = y


class Snake:
    def __init__(self):
        self.list_blocks = []
        self.direction = "right"
        self.blocks = 2
        self.pos = [1, 1]

    def verif_pos(self):
        ### Modifie les coordonés ###
        if self.direction == "up":
            if grille.matrice[self.pos[0]][self.pos[1] - 1] not in OBSTACLES:
                self.pos[1] -= 1
            else:
                Var.GAME_OVER = True
                return False

        elif self.direction == "down":
            if grille.matrice[self.pos[0]][self.pos[1] + 1] not in OBSTACLES:
                self.pos[1] += 1
            else:
                Var.GAME_OVER = True
                return False

        elif self.direction == "left":
            if grille.matrice[self.pos[0] - 1][self.pos[1]] not in OBSTACLES:
                self.pos[0] -= 1
            else:
                Var.GAME_OVER = True
                return False

        elif self.direction == "right":
            if grille.matrice[self.pos[0] + 1][self.pos[1]] not in OBSTACLES:
                self.pos[0] += 1
            else:
                Var.GAME_OVER = True
                return False

        return True

    def actualise_pos(self):
        ### Efface ###
        for snake_block in self.list_blocks:
            grille.matrice[snake_block[0]][snake_block[1]] = ESPACE

        ### Actualise les valeurs ###
        self.list_blocks.append(self.pos[:])
        if len(self.list_blocks) > self.blocks:
            self.list_blocks.pop(0)

        ### Actualise la grille ###
        for snake_block in self.list_blocks:
            if snake_block == self.pos:
                grille.matrice[snake_block[0]][snake_block[1]] = TETE
            else:
                grille.matrice[snake_block[0]][snake_block[1]] = CORP

    def verif_point_mange(self):
        if self.pos == point.pos:     ## Si le point est mangé
            point.spawn_point()
            self.blocks += 1
            Var.SCORE += 1
            pygame.display.set_caption('Snake - Score: {}'.format(Var.SCORE))
            Var.FPS += 0.25


class Point:
    def spawn_point(self):
        x = random.randint(1, grille.longueur - 2)
        y = random.randint(1, grille.largeur - 2)

        while grille.matrice[x][y] in OBSTACLES:      ### Au cas ou, si le point est dans le snake il se regénère
            x = random.randint(1, grille.longueur - 2)
            y = random.randint(1, grille.largeur - 2)

        self.pos = []
        self.pos.append(x)
        self.pos.append(y)
        grille.matrice[x][y] = POINT




def blocks2pixels(x, y):
    return (x * BLOCK_DIM), (y * BLOCK_DIM)

def dessine():
    ### Murs ###
    for block_y in range(GRILLE_LARG):
        x, y = blocks2pixels(0, block_y)
        if block_y == 0 or block_y == GRILLE_LARG - 1:
            for block_x in range(GRILLE_LONG):
                grille.matrice[block_x][block_y] = MUR
        else:
            grille.matrice[0][block_y] = MUR
            grille.matrice[GRILLE_LONG - 1][block_y] = MUR

    ### Éléments du jeu ###
    for block_x in range(GRILLE_LONG):
        for block_y in range(GRILLE_LARG):
            x, y = blocks2pixels(block_x, block_y)
            if grille.matrice[block_x][block_y] != ESPACE:
                pygame.draw.rect(DISPLAYSURF, grille.matrice[block_x][block_y][1], (x, y, BLOCK_DIM, BLOCK_DIM))

def reset():
    global grille, snake, point
    Var.FPS = 5
    Var.GAME_OVER = False
    Var.PAUSED = False
    Var.SCORE = 0

    grille = Grille(GRILLE_LARG, GRILLE_LONG)
    snake = Snake()
    point = Point()
    point.spawn_point()
    pygame.display.set_caption('Snake - Score: {}'.format(Var.SCORE))


class Var:
    FPS = 5
    GAME_OVER = False
    PAUSED = False
    SCORE = 0

GRILLE_LONG = 30 # blocks
GRILLE_LARG = 30 # blocks
BLOCK_DIM = 20 # px
FENETRE_LONG = GRILLE_LONG * BLOCK_DIM
FENETRE_LARG = GRILLE_LARG * BLOCK_DIM

ORANGE = (255, 128, 0)
VERT = (0, 204, 0)
BLANC = (255, 255, 255)
ROUGE = (255, 0, 0)
BG = (100, 100, 100)

ESPACE = ["espace", BG]
MUR = ["mur", ORANGE]
TETE = ["tete", BLANC]
CORP = ["corp", VERT]
POINT = ["point", ROUGE]

OBSTACLES = [MUR, TETE, CORP]

pygame.init()
FPSCLOCK = pygame.time.Clock()
DISPLAYSURF = pygame.display.set_mode((FENETRE_LONG, FENETRE_LARG))
pygame.display.set_caption('Snake - Score: {}'.format(Var.SCORE))

grille = Grille(GRILLE_LARG, GRILLE_LONG)
snake = Snake()
point = Point()
point.spawn_point()

while True:
    DISPLAYSURF.fill(BG)
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if Var.GAME_OVER == False and Var.PAUSED == False:
                direction = snake.direction
                if (event.key == pygame.K_UP or event.key == pygame.K_z) and direction != "down":
                    snake.direction = "up"
                elif (event.key == pygame.K_DOWN or event.key == pygame.K_s) and direction != "up":
                    snake.direction = "down"
                elif (event.key == pygame.K_LEFT or event.key == pygame.K_q) and direction != "right":
                    snake.direction = "left"
                elif (event.key == pygame.K_RIGHT or event.key == pygame.K_d) and direction != "left":
                    snake.direction = "right"

            if (event.key == pygame.K_SPACE or event.key == pygame.K_p) and Var.GAME_OVER == False:
                if Var.PAUSED == False:
                    Var.PAUSED = True
                    pygame.display.set_caption('Snake - Score: {} (Paused)'.format(Var.SCORE))
                else:
                    Var.PAUSED = False
                    pygame.display.set_caption('Snake - Score: {}'.format(Var.SCORE))

            if event.key == pygame.K_r and Var.GAME_OVER == True:
                reset()


    if Var.GAME_OVER == False and Var.PAUSED == False:
        if snake.verif_pos() is True:
            snake.actualise_pos()
            snake.verif_point_mange()
        dessine()
        pygame.display.update()

    if Var.GAME_OVER == True:
        pygame.display.set_caption('Snake - Score: {} (Game Over)'.format(Var.SCORE))

    FPSCLOCK.tick(Var.FPS)
