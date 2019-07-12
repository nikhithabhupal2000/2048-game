import pygame, sys, time
from pygame.locals import *
from colours import *
from random import *

TOTAL_POINTS = 0

BOARD_SIZE = 8

pygame.init()

SURFACE = pygame.display.set_mode((400, 500))
pygame.display.set_caption("2048 game")

myfont = pygame.font.SysFont("monospace", 20)
scorefont = pygame.font.SysFont("comicsansms", 50)

tileMatrix  = []

def main():
	global BOARD_SIZE
	FirstScreen()	
	placeRandomTile()
	placeRandomTile()
	printMatrix()
	while True:
		for event in pygame.event.get():
			if event.type == QUIT:
				pygame.quit()
				sys.exit()

			if checkIfCanGo() == True:
				if event.type == KEYDOWN:
					if isArrow(event.key):
						move(event.key)
						merge(event.key)
						placeRandomTile()
						printMatrix()
					elif event.key == pygame.K_r:
						reset()
					
			else:
				printGameOver()
			if event.type == KEYDOWN:
				if event.key == pygame.K_r:
					reset()
		pygame.display.update()


def FirstScreen():
	global BOARD_SIZE
	global tileMatrix
	SURFACE.fill(BLACK)
	label1 = scorefont.render("Hello!!!", 1, (255,255,255))
	label2 = scorefont.render("Choose the level", 1, (255,255,255))
	label3 = scorefont.render(" [e] : Easy", 1, (255,255,255))
	label4 = scorefont.render("[m] : Medium", 1, (255,255,255))
	label5 = scorefont.render("[h] : Hard", 1, (255,255,255))

	SURFACE.blit(label1, (50, 100))
	SURFACE.blit(label2, (50, 150))
	SURFACE.blit(label3, (50, 200))
	SURFACE.blit(label4, (50, 250))
	SURFACE.blit(label5, (50, 300))
	pygame.display.update()
	tmp = True
	while tmp:	
		for event in pygame.event.get():
		

			if event.type == KEYDOWN:
				if event.key == pygame.K_e:
					BOARD_SIZE = 8
				elif event.key == pygame.K_m:
					BOARD_SIZE = 6
				else:
					BOARD_SIZE = 4
				tileMatrix = [[0 for i in range(BOARD_SIZE)] for j in range(BOARD_SIZE)]
				tmp = False
			pygame.display.update()
			
			

def checkIfCanGo():
        for i in range(0, BOARD_SIZE ** 2):
		 if tileMatrix[floor(i / BOARD_SIZE)][i % BOARD_SIZE] == 0:
			 return True
	for i in range(0, BOARD_SIZE):
		 for j in range(0, BOARD_SIZE - 1):
			 if tileMatrix[i][j] == tileMatrix[i][j + 1]:
				 return True
			 elif tileMatrix[j][i] == tileMatrix[j + 1][i]:
			 	 return True
        
	return False


def move_left(Matrix):
	
	for i in range(BOARD_SIZE):
		temp = []
		for j in range(BOARD_SIZE):
			if (Matrix[i][j] != 0):
				temp.append(Matrix[i][j])
		while(len(temp) != BOARD_SIZE):
			temp.append(0)


		Matrix[i] = temp
	return Matrix




def move_right(Matrix):
	
	for i in range(BOARD_SIZE):
		temp = []
		for j in range( BOARD_SIZE - 1, -1, -1):
			if Matrix[i][j] != 0:
				temp.append(Matrix[i][j])
		while(len(temp) != BOARD_SIZE):
			temp.append(0)
		temp.reverse()
		Matrix[i] = temp
	return Matrix




def move(key):	
	global tileMatrix
	if key == 273:
		transpose = list(zip(*tileMatrix))
		transpose = [list(i) for i in transpose]
		transpose = move_left(transpose)
		transpose = list(zip(*transpose))
                tileMatrix = [list(i) for i in transpose]
		
	
		
	elif key == 274:
		transpose = list(zip(*tileMatrix))
		transpose = [list(i) for i in transpose]
		transpose = move_right(transpose)
		transpose = list(zip(*transpose))
                tileMatrix = [list(i) for i in transpose]
	
	elif key == 276:
		tileMatrix = move_left(tileMatrix)
	
	else:
		tileMatrix = move_right(tileMatrix)



			
def merge_left(Matrix):
	global TOTAL_POINTS
	for row in range(BOARD_SIZE):
		i = 0
		temp = []
		while(i <= BOARD_SIZE - 1):
			if i + 1 < BOARD_SIZE and Matrix[row][i] == Matrix[row][i + 1]:
				temp.append(2 * Matrix[row][i])
				TOTAL_POINTS += 2 * Matrix[row][i]
				i += 2
			else: 
				temp.append(Matrix[row][i])
				i += 1
		while(len(temp) != BOARD_SIZE):
			temp.append(0)
		Matrix[row] = temp
	return Matrix

def merge_right(Matrix):
	global TOTAL_POINTS
	global BOARD_SIZE
	for row in range(BOARD_SIZE):
		i = BOARD_SIZE - 1 
		temp = []
		while( i >= 0):
			if i - 1 >= 0 and Matrix[row][i] == Matrix[row][i - 1] :
				temp.append( 2 * Matrix[row][i])
				TOTAL_POINTS += 2 * Matrix[row][i]
				i -= 2
			else:
				temp.append(Matrix[row][i])
				i -= 1
		while(len(temp) != BOARD_SIZE):
			temp.append(0)
		temp.reverse()
		Matrix[row] = temp
	return Matrix

			

def merge(key):
	global BOARD_SIZE
        global tileMatrix

	if key == 273:
		transpose = list(zip(*tileMatrix))
		transpose = [list(i) for i in transpose]
		transpose = merge_left(transpose)
		transpose = list(zip(*transpose))
		tileMatrix = [list(i) for i in transpose]

	elif key == 274:
		transpose = list(zip(*tileMatrix))
		transpose = [list(i) for i in transpose]
		transpose = merge_right(transpose)
		transpose = list(zip(*transpose))
                tileMatrix = [list(i) for i in transpose]


	elif key == 276:
		tileMatrix = merge_left(tileMatrix)


	else:
		tileMatrix = merge_right(tileMatrix)

	


def printMatrix():

        SURFACE.fill(BLACK)

        global BOARD_SIZE
        global TOTAL_POINTS

        for i in range(0, BOARD_SIZE):
                for j in range(0, BOARD_SIZE):
                        pygame.draw.rect(SURFACE, getColour(tileMatrix[j][i]), (i*(400/BOARD_SIZE), j*(400/BOARD_SIZE) + 100, 400/BOARD_SIZE, 400/BOARD_SIZE))

                        label = myfont.render(str(tileMatrix[j][i]), 1, (255,255,255))
                        label2 = scorefont.render("Score:" + str(TOTAL_POINTS), 1, (255, 255, 255))

                        SURFACE.blit(label, (i*(400/BOARD_SIZE) + 30, j*(400/BOARD_SIZE) + 130))
                        SURFACE.blit(label2, (10, 20))


def printGameOver():
        global TOTAL_POINTS

        SURFACE.fill(BLACK)

        label = scorefont.render("Game Over!", 1, (255,255,255))
        label2 = scorefont.render("Score:" + str(TOTAL_POINTS), 1, (255,255,255))
        label3 = myfont.render("Press r to restart!", 1, (255,255,255))

        SURFACE.blit(label, (50, 100))
        SURFACE.blit(label2, (50, 200))
        SURFACE.blit(label3, (50, 300))


def placeRandomTile():
	global tileMatrix
  	tmp = False
	for i in range(0, BOARD_SIZE ** 2):
		if tileMatrix[floor(i / BOARD_SIZE)][i % BOARD_SIZE] == 0:
			tmp = True

	if tmp == True:
		i = floor(random() * BOARD_SIZE)
		j = floor(random() * BOARD_SIZE)
		while(tileMatrix[i][j] != 0):
			i = floor(random() * BOARD_SIZE)
			j = floor(random() * BOARD_SIZE)

		tileMatrix[i][j] = 2

def floor(n):
        return int(n - (n % 1))



def reset():
        global TOTAL_POINTS
        global tileMatrix

        TOTAL_POINTS = 0
        SURFACE.fill(BLACK)

        tileMatrix = [[0 for i in range(0, BOARD_SIZE)] for j in range(0, BOARD_SIZE)]

        main()

def isArrow(k):
        return(k == pygame.K_UP or k == pygame.K_DOWN or k == pygame.K_LEFT or k == pygame.K_RIGHT)

main()
