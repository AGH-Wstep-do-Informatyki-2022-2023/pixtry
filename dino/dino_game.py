import pygame
from random import randint
import math

pygame.init()
screen = pygame.display.set_mode((1280, 720))  # 1280x720


character = pygame.image.load('dino/graphics/psychopath_derek.png').convert_alpha()  # 520x730
character = pygame.transform.scale(character, (120, 170))  # 120x170
background_graveyard_1 = pygame.image.load('dino/graphics/background_1.png').convert_alpha()  # 1863x455
background_graveyard_2 = background_graveyard_1
ground = pygame.image.load('dino/graphics/ground.png').convert_alpha()  # 1387x180
grave = pygame.image.load('dino/graphics/grave.png').convert_alpha()  # 800x840
grave = pygame.transform.scale(grave, (100, 105))
grave_2 = pygame.image.load('dino/graphics/grave.png').convert_alpha()  # 800x840
grave_2 = pygame.transform.scale(grave_2, (100, 105))
background = pygame.Surface((1280, 720))
background.fill('grey')
font_game = pygame.font.Font("dino/font/Pixeltype.ttf", 72)
game_clock = pygame.time.Clock()

background_x_coord = 0  # always 0
ground_x_coord = 0  # always 0
game_speed = 0

grave_x_coord = 1300
grave_y_coord = 650
grave_list = []

#   jump setup

jump = 0  # always 0
player_y_coord = 650
jump_count_down = 0  # always 0
jump_len = 40  # jump length in frames
player_y_coord_change_base = 30  # changes speed of jump
player_y_coord_change = player_y_coord_change_base
player_acceleration = 2 * player_y_coord_change_base / jump_len

spawn_countdown = 0
radius = 45

score = 0
did_win = 0
did_lose = 0
points_to_win = 50


def draw_text(text, font, text_color, x, y):
    img = font.render(text, True, text_color)
    img_rect = img.get_rect(midtop=(x, y))
    screen.blit(img, img_rect)


def spawn_grave():

    grave_list.append(randint(1200, 1600))


def grave_move(grave_list_inner):
    if grave_list_inner:
        grave_list_inner = [grave_x_coord_list - game_speed for grave_x_coord_list in grave_list if
                            grave_x_coord_list >= -100]
        return grave_list_inner


def show_grave(grave_list_inner):
    if grave_list_inner:
        for grave_list_x_coord in grave_list_inner:
            screen.blit(grave, (grave_list_x_coord, 550))
            pygame.draw.circle(grave, (255, 255, 255), (grave_list_x_coord + 55, 595), radius)


def grave_collision(rbottom, center_x):
    distance_x_mid_r = center_x - 220
    distance_y_mid_r = 650 - rbottom
    distance_x_bot_r = center_x - 220
    distance_y_bot_r = 650 - rbottom - 55
    distance_x_bot_m = center_x - 160
    distance_y_bot_m = 650 - rbottom - 55
    distance_x_bot_l = center_x - 100
    distance_y_bot_l = 650 - rbottom - 55

    if math.hypot(distance_x_mid_r, distance_y_mid_r) <= radius:
        return True
    elif math.hypot(distance_x_bot_r, distance_y_bot_r) <= radius:
        return True
    elif math.hypot(distance_x_bot_m, distance_y_bot_m) <= radius:
        return True
    elif math.hypot(distance_x_bot_l, distance_y_bot_l) <= radius:
        return True
    else:
        return False


def detect_grave_collision(grave_list_inner):
    if grave_list_inner:
        for grave_list_x_coord in grave_list_inner:
            return grave_collision(player_y_coord, grave_list_x_coord + 55, )


def main():
    # had to add to global, thanks that game is running in MAIN
    global background_x_coord, ground_x_coord, player_y_coord, game_speed, spawn_countdown, grave_list, jump, jump_count_down, player_y_coord_change, score, did_lose, did_win

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return

        keys = pygame.key.get_pressed()
        if score >= points_to_win:
            did_win = 1

        screen.blit(background, (0, 0))

        background_graveyard_1_rect = background_graveyard_1.get_rect(bottomleft=(background_x_coord, 720))
        screen.blit(background_graveyard_1, background_graveyard_1_rect)

        background_graveyard_2_rect = background_graveyard_2.get_rect(bottomleft=(background_x_coord + 1863, 720))
        screen.blit(background_graveyard_2, background_graveyard_2_rect)

        ground_rect = ground.get_rect(bottomleft=(ground_x_coord, 770))
        screen.blit(ground, ground_rect)

        ground_2_rect = ground.get_rect(bottomleft=(ground_x_coord + 1387, 770))
        screen.blit(ground, ground_2_rect)

        character_rect = character.get_rect(bottomleft=(100, player_y_coord))
        screen.blit(character, character_rect)

        draw_text("Score: "+str(score), font_game, 'black', 120, 30)

        if game_speed == 0:
            if did_lose and did_win:
                draw_text("Congrats you won!!! Your score is: "+str(score), font_game, 'black', 600, 200)
                pygame.display.update()
                pygame.time.wait(5000)
                return
            if did_lose == 1:
                score = 0
                did_lose = 0
                spawn_countdown = 0
                ground_x_coord = 0
                background_x_coord = 0

            draw_text("Score "+str(points_to_win)+" points to pass", font_game, 'black', 600, 200)
            pygame.display.update()
            pygame.time.wait(3000)
            grave_list = []
            game_speed = 12

        # move of graves and tree background
        background_x_coord -= game_speed
        ground_x_coord -= game_speed

        if background_x_coord < -1863:
            background_x_coord = 0
        if ground_x_coord < -1387:
            ground_x_coord = 0

        if spawn_countdown % 60 == 0 and game_speed != 0:
            spawn_grave()
            score += 1

        spawn_countdown += 1

        show_grave(grave_list)
        grave_list = grave_move(grave_list)
        if detect_grave_collision(grave_list):
            if not did_win:
                pygame.time.wait(800)
            game_speed = 0
            did_lose = 1
        # jump
        if keys[pygame.K_SPACE] and game_speed != 0:
            jump = 1

        if jump and game_speed != 0:
            if jump_count_down < jump_len / 2:
                jump_count_down += 1
                player_y_coord_change -= player_acceleration
                player_y_coord -= player_y_coord_change
            if jump_count_down == jump_len / 2:
                player_y_coord_change = 0
                jump_count_down += 1
            if jump_len / 2 < jump_count_down < jump_len:
                jump_count_down += 1
                player_y_coord_change += player_acceleration
                player_y_coord += player_y_coord_change
            if jump_count_down == jump_len:
                jump = 0
                jump_count_down = 0
                player_y_coord_change = player_y_coord_change_base

        pygame.display.update()
        game_clock.tick(60)


main()
