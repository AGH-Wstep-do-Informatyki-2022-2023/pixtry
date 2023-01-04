import pygame
import sys
import os

BOX_SIZE=36

PLAYER='@'
TARGET='.'
SPACE=' '
BOX='$'
BINGO='*'
WALL='#'

board= []
targets= []

root = os.path.dirname(os.path.abspath(__file__))

def initBoard():
    with open(root+'/game01.txt', 'r') as f:
        for line in f.read().splitlines():
            board.append(list(line))


def initTargets():
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j]==TARGET:
                targets.append([i, j])


def isTarget(row, col):
    for target in targets:
        if target[0]==row and target [1]==col:
            return True
    return False


def getPlayerPosition():
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] == PLAYER:
                return i, j


def moveLeft():
    movePlayer(0, -1)


def moveUp():
    movePlayer(-1,0)


def moveRight():
    movePlayer(0,1)


def moveDown():
    movePlayer(1,0)


def movePlayer(i,j):
    row, col = getPlayerPosition()

    m, n =i*2, j*2


    if board[row+i][col+j] == SPACE:
        doMove(row, col, i, j)


    elif board[row+i][col+j]== TARGET:
        doMove(row, col, i, j)


    elif board[row+i][col+j] == BOX:
        if board[row+m][col+n]== SPACE:
            board[row+m][col+n] = BOX
            doMove(row, col, i, j)

        elif board[row+m][col+n] ==TARGET:
            board[row+m][col+n] = BINGO
            doMove(row, col, i, j)


    elif board[row+i][col+j] == BINGO:
        if board[row+m][col+n]==SPACE:
            board[row+m][col+n]=BOX
            doMove(row, col, i, j)

        elif board[row+m][col+n] == TARGET:
            board[row+m][col+n]= BINGO
            doMove(row, col, i, j)


        else:
            pass


def doMove(row, col, i, j):
    board[row+i][col+j]=PLAYER
    if isTarget(row,col):
        board[row][col]= TARGET
    else:
        board[row][col]=SPACE


def drawBoard(screen):

    img_wall=pygame.image.load(root+'/wall.png').convert()
    img_box=pygame.image.load(root+'/box.png').convert()
    img_bingo=pygame.image.load(root+'/bingo.png').convert()
    img_space=pygame.image.load(root+'/space.png').convert()
    img_target=pygame.image.load(root+'/target.png').convert()
    img_player=pygame.image.load(root+'/player.png').convert()
    images = {WALL: img_wall, SPACE: img_space, BOX: img_box, TARGET: img_target, PLAYER: img_player, BINGO: img_bingo}


    for i in range (len(board)):
        for j in range(len(board[i])):
            screen.blit(images[board[i][j]], (j*BOX_SIZE, i*BOX_SIZE))

    pygame.display.update()


def getScreenSize():
    j=0
    for i in range (len(board)):
        j=len(board[i]) if len(board[i])> j else j
    return j*BOX_SIZE, len(board)*BOX_SIZE


def main():
    board= initBoard()
    targets=initTargets()

    pygame.display.init()
    pygame.display.set_caption("Sokoban")
    screen = pygame.display.set_mode(getScreenSize(), pygame.FULLSCREEN)
    screen.fill((0,0,0))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    moveLeft()
                elif event.key == pygame.K_RIGHT:
                    moveRight()
                elif event.key == pygame.K_UP:
                    moveUp()
                elif event.key == pygame.K_DOWN:
                     moveDown()
                elif event.key == pygame.K_ESCAPE:
                    pygame.event.get()
                    return
            elif event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        drawBoard(screen)


main()