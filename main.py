import time
import pygame
from os import path
import interactions

pygame.init()

# fps
clock = pygame.time.Clock()
fps = 60

# res
screen_width = 1280
screen_height = 720

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('All saints of me')

# define game variables
tile_size = 40
room = 0
max_room = 5
mainMenu = True
inventory = False

#stupid variables, that could be just one variable, but i didn't add class for this, maybe some day after exams it will be added
moveFloat=0 #to get text move
moveFloatSokoban=0
moveFLoatDino=0
moveFloatFlappy=0

# load font
font = pygame.font.Font('font/Pixeltype.ttf', 72)
fontMenu = pygame.font.Font('font/Pixeltype.ttf', 100)
fontFloating = pygame.font.Font('font/Pixeltype.ttf', 48)

# load images
bg_img = pygame.image.load('img/bk_img.png')


# draw text
def draw_text(text, font, text_color, x, y):
    img = font.render(text, True, text_color)
    img_rect = img.get_rect(midtop=(x, y))
    screen.blit(img, img_rect)

# creating black lines (better to use than pixels)
def draw_grid():
    for line in range(0, int(screen_width / tile_size)):
        pygame.draw.line(screen, 'black', (line * tile_size, 0), (line * tile_size, screen_height))
    for line in range(0, int(screen_height / tile_size)):
        pygame.draw.line(screen, 'black', (0, line * tile_size), (screen_width, line * tile_size))


# to check what room we have
def returnRoom(): return room


# function to increment room
def roomPP():
    global room
    room += 1


# resetting room, to create new room
def reset_room(room):
    player.reset(80, screen_height - 200)
    door_group.empty()
    backdoor_group.empty()
    patientCard_group.empty()
    sokobanDoor_group.empty()
    dinoDoor_group.empty()
    flappyDoor_group.empty()
    badge_group.empty()

    # load in room and create world
    if path.exists(f'rooms/room_{room}'):
        with open(f'rooms/room_{room}', 'r') as f:
            world_data = [list(line.strip()) for line in f.readlines()]
    world = World(world_data)

    return world


# with class button we can click on text in main menu
class Button():
    def __init__(self, text, font, textColor, x, y):
        self.font = font
        self.text = text
        self.textColor = textColor
        self.img = self.font.render(self.text, True, self.textColor)
        self.img_rect = self.img.get_rect(midtop=(x, y))
        self.clicked = False

    def draw(self):
        action = False

        # get mouse position
        pos = pygame.mouse.get_pos()

        # check mouseover and clicked conditions
        if self.img_rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                action = True
                self.clicked = True

        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False

        # draw button
        screen.blit(self.img, self.img_rect)

        return action


# in world, we display every block, that we can collide/interact with
class World():
    def __init__(self, data):
        self.tile_list = []

        # load images
        dirt_img = pygame.image.load('img/brown_dirt.png')
        floor_img = pygame.image.load('img/black.png')
        platform_img = pygame.image.load('img/platform.png')

        row_count = 0
        for row in data:
            col_count = 0
            for tile in row:
                tile = int(tile)
                if tile == 1:  # dirt, the lowest part of floor
                    img = pygame.transform.scale(dirt_img, (tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                elif tile == 2:  # door +1
                    door = interactions.Door(col_count * tile_size, row_count * tile_size)
                    door_group.add(door)
                elif tile == 3:  # door -1
                    bdoor = interactions.BackDoor(col_count * tile_size, row_count * tile_size)
                    backdoor_group.add(bdoor)
                elif tile == 4:  # platforms (you can jump on it)
                    img = pygame.transform.scale(platform_img, (tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                elif tile == 5 and 'Patient Card' not in player.eq:
                    patientCard = interactions.PatientCard(col_count * tile_size, row_count * tile_size, 1)
                    patientCard_group.add(patientCard)
                elif tile == 6:  # play sokoban
                    sokobanDoor = interactions.SokobanDoor(col_count * tile_size, row_count * tile_size)
                    sokobanDoor_group.add(sokobanDoor)
                elif tile == 7:  # play dino
                    dinoDoor = interactions.DinoDoor(col_count * tile_size, row_count * tile_size)
                    dinoDoor_group.add(dinoDoor)
                elif tile == 8:  # play flappy
                    flappyDoor = interactions.FlappyDoor(col_count * tile_size, row_count * tile_size)
                    flappyDoor_group.add(flappyDoor)
                elif tile == 9:  # main floor
                    img = pygame.transform.scale(floor_img, (tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                col_count += 1
            row_count += 1

    def draw(self):
        for tile in self.tile_list:
            screen.blit(tile[0], tile[1])


# player class has everything that our player need, moving, jumping interacting with objects...
class Player():
    def __init__(self, x, y):
        self.reset(x, y)
        self.eq = []

    def update(self):
        dx = 0
        dy = 0
        nextRoom = 0

        # get keypresses
        key = pygame.key.get_pressed()
        if key[pygame.K_SPACE] and not self.jumped:
            self.vel_y = -20
            self.jumped = True
        if key[pygame.K_LEFT]:
            dx -= 5
        if key[pygame.K_RIGHT]:
            dx += 5
        if key[pygame.K_e] and pygame.sprite.spritecollide(self, door_group, False):
            if returnRoom() == 1 and 'Patient Card' not in self.eq:  # in room 1 we must find patient card
                draw_text('Get patient card first', font, 'black', screen_width // 2, screen_height // 2 )
            else:
                nextRoom = 1
                time.sleep(0.125)
        if key[pygame.K_e] and pygame.sprite.spritecollide(self, backdoor_group, False):
            nextRoom = -1
            time.sleep(0.125)
        if key[pygame.K_e] and pygame.sprite.spritecollide(self, patientCard_group, False):
            self.eq.append('Patient Card')
            print('Collected Card')
            patientCard_group.empty()
        if key[pygame.K_e] and pygame.sprite.spritecollide(self, sokobanDoor_group, False):
            import sokoban.sokoban
            self.eq.append('Sokoban badge')
            print('Collected Sokoban badge')
            roomPP()
            reset_room(room)
        if key[pygame.K_e] and pygame.sprite.spritecollide(self, dinoDoor_group, False):
            import dino.dino_game
            self.eq.append('Dino badge')
            print('Collected Dino badge')
            roomPP()
            reset_room(room)
        if key[pygame.K_e] and pygame.sprite.spritecollide(self, flappyDoor_group, False):
            import flappy.flappyBird
            self.eq.append('Flappy badge')
            print('Collected Flappy badge')
            roomPP()
            reset_room(room)

        # add gravity
        self.vel_y += 1
        if self.vel_y > 10:
            self.vel_y = 10
        dy += self.vel_y

        # check for collision
        for tile in world.tile_list:
            # check for collision in x direction
            if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                dx = 0
            # check for collision in y direction
            if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                self.jumped = False
                # check if below the ground i.e. jumping
                if self.vel_y < 0:
                    dy = tile[1].bottom - self.rect.top
                    self.vel_y = 0
                # check if above the ground i.e. falling
                elif self.vel_y >= 0:
                    dy = tile[1].top - self.rect.bottom
                    self.vel_y = 0

        # update player coordinates
        self.rect.x += dx
        self.rect.y += dy

        # making sure, that player won't disappear
        if self.rect.top > screen_height+30:
            self.rect.bottom = 0
        if self.rect.right >= 1280:
            self.rect.right = 1280
            dx = 0
        if self.rect.left <= 0:
            self.rect.left = 0
            dx = 0

        # draw player onto screen
        screen.blit(self.image, self.rect)

        return nextRoom

    def reset(self, x, y):
        img = pygame.image.load('img/guy.png')
        self.image = pygame.transform.scale(img, (80, 150))
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.vel_y = 0
        self.jumped = False


# objects of our classes

player = Player(80, 200)
door_group = pygame.sprite.Group()
backdoor_group = pygame.sprite.Group()
patientCard_group = pygame.sprite.Group()
sokobanDoor_group = pygame.sprite.Group()
dinoDoor_group = pygame.sprite.Group()
flappyDoor_group = pygame.sprite.Group()
badge_group = pygame.sprite.Group()

# loading room from file
if path.exists(f'rooms/room_{room}'):
    with open(f'rooms/room_{room}', 'r') as f:
        world_data = [list(line.strip()) for line in f.readlines()]
world = World(world_data)

# create buttons in main menu
newGameButton = Button('New Game', font, 'white', screen_width // 2, screen_height // 2 - 130)
continueGameButton = Button('Continue', font, 'white', screen_width // 2, screen_height // 2)
eqButton = Button('Inventory', font, 'white', screen_width // 2, screen_height // 2 + 130)
quitButton = Button('Quit', font, 'white', screen_width // 2, screen_height // 2 + 260)

run = True
while run:
    clock.tick(fps)
    screen.fill('black')
    if mainMenu:  # main menu
        draw_text('All saints of me', fontMenu, 'white', screen_width // 2, 70)
        if newGameButton.draw():
            room = 0
            world_data = []
            world = reset_room(room)
            nextRoom = 0
            mainMenu = False
            inventory = False
            player.eq.clear()
        if continueGameButton.draw():
            mainMenu = False
            inventory = False
        if eqButton.draw():  # go to inventory
            inventory = True
            mainMenu = False
        if quitButton.draw():
            run = False
    elif not mainMenu and inventory:  # el. in inventory
        if len(player.eq) == 0:
            draw_text("Your inventory is empty", font, 'white', screen_width // 2,
                      screen_height // 2 - 100)
        else:
            #for i in player.eq:
                if 'Patient Card' in player.eq:
                    patientCardButton = Button('Patient Card', font, 'white', screen_width // 2, 0)
                    if patientCardButton.draw():
                        pCard = interactions.PatientCard(10 * tile_size, 0, 2)
                        patientCard_group.add(pCard)
                        patientCard_group.draw(screen)
                    else:
                        patientCard_group.empty()
                if 'Sokoban badge' in player.eq:
                    sBadgeButton = Button('Sokoban badge', font, 'white', screen_width // 2, 3*tile_size)
                    if sBadgeButton.draw():
                        sBadge = interactions.Badges(14 * tile_size, screen_height//2 - tile_size, 'sokoban/player.png', 1)
                        badge_group.add(sBadge)
                        badge_group.draw(screen)
                    else:
                        badge_group.empty()
                if 'Dino badge' in player.eq:
                    dBadgeButton = Button('Dino badge', font, 'white', screen_width // 2, 6 * tile_size)
                    if dBadgeButton.draw():
                        dBadge = interactions.Badges(11 * tile_size, 0, 'dino/graphics/psychopath_derek.png', 2)
                        badge_group.add(dBadge)
                        badge_group.draw(screen)
                    else:
                        badge_group.empty()
                if 'Flappy badge' in player.eq:
                    fBadgeButton = Button('Flappy badge', font, 'white', screen_width // 2, 9 * tile_size)
                    if fBadgeButton.draw():
                        fBadge = interactions.Badges(14 * tile_size , screen_height//2 - tile_size, 'flappy/grafika/bird.png', 3)
                        badge_group.add(fBadge)
                        badge_group.draw(screen)
                    else:
                        badge_group.empty()
            # here put other things, that you created
    else:
        # displaying everything
        screen.blit(bg_img, (0, 0))
        world.draw()
        door_group.draw(screen)
        backdoor_group.draw(screen)
        patientCard_group.draw(screen)
        sokobanDoor_group.draw(screen)
        dinoDoor_group.draw(screen)
        flappyDoor_group.draw(screen)
        badge_group.draw(screen)
        nextRoom = player.update()

        #code below is very poor and can be rewritten much better
        if returnRoom()==0:
            draw_text('Arrow - walk, Space - jump,  E - interact', font, 'black', screen_width // 2, screen_height // 2 - 3*tile_size)
        elif returnRoom()==1 and len(player.eq)==1 and moveFloat<=screen_height//2:
            draw_text('Collected Card', font, 'black', screen_width // 2, screen_height // 2 - moveFloat)
            moveFloat+=3
        elif returnRoom()==3 and moveFloatSokoban<=screen_height//2:
            draw_text('Collected Sokoban badge', font, 'black', screen_width // 2, screen_height // 2 - moveFloatSokoban)
            moveFloatSokoban+=3
        elif returnRoom()==4 and moveFLoatDino<=screen_height//2:
            draw_text('Collected Dino badge', font, 'black', screen_width // 2, screen_height // 2 - moveFLoatDino)
            moveFLoatDino+=3
        elif returnRoom()==5 and moveFloatFlappy<=screen_height//2:
            draw_text('Collected Flappy Badge', font, 'black', screen_width // 2, screen_height // 2 - moveFloatFlappy)
            moveFloatFlappy+=3
        if returnRoom()==5:
            draw_text('Check your inventory, there are some cool badges', font, 'black', screen_width // 2, screen_height // 2 - 3*tile_size)


        # setting new room
        if nextRoom == 1:
            # reset game and go to next level
            prev_room = room
            room += 1
            print('door', room, prev_room)
            if room <= max_room:
                # reset level
                world_data = []
                world = reset_room(room)
                nextRoom = 0
            else: #if player finishes playing
                screen.fill('black')
                draw_text('Game Over', fontMenu, 'white', screen_width // 2, screen_height // 2 - 100)
                draw_text('Thanks for playing', font, 'white', screen_width // 2, screen_height // 2 + 50)
                pygame.display.update()
                time.sleep(5)
                mainMenu=True
                reset_room(0)
        elif nextRoom == -1:
            prev_room = room
            room -= 1
            print('backdoor', room, prev_room)
            if room >= 0:
                world_data = []
                world = reset_room(room)
                nextRoom = 0

    #draw_grid() #you can comment it to remove those black lines

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:  # open main menu
            if event.key == pygame.K_ESCAPE and not mainMenu:
                mainMenu = True
                inventory = False
            elif event.key == pygame.K_ESCAPE and mainMenu:
                mainMenu = False
            elif event.key == pygame.K_i:
                if inventory:
                    inventory = False
                else:
                    inventory = True

    pygame.display.update()

pygame.quit()
