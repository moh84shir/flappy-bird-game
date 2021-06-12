# IMPORTS
import pygame
import sys
import os
import random
import time

# CLEAR TERMINAL
os.system('cls')

# START PYGAME MODULES
pygame.init()


# ALL VARIABLES
display_width = 340
display_height = 630
floor_x = 0
gravity = 0.25
bird_movement = 0
pipe_list = []
game_status = True
bird_list_index = 0
score = 0
hight_score = 0
active_score = True


# IMAGES
backgound_image = pygame.transform.scale2x(
    pygame.image.load("assets/img/bg1.png"))
floor_image = pygame.transform.scale2x(
    pygame.image.load("assets/img/floor.png"))
pipe_image = pygame.transform.scale2x(
    pygame.image.load("assets/img/pipe_green.png"))
game_over_image = pygame.transform.scale2x(
    pygame.image.load("assets/img/message.png"))

# BIRD IMGAGES
bird_image_down = pygame.transform.scale2x(
    pygame.image.load("assets/img/red_bird_down_flap.png"))
bird_image_mid = pygame.transform.scale2x(
    pygame.image.load("assets/img/red_bird_mid_flap.png"))
bird_image_up = pygame.transform.scale2x(
    pygame.image.load("assets/img/red_bird_up_flap.png"))


game_over_image_rect = game_over_image.get_rect(center=(170, 300))


bird_list = [bird_image_down, bird_image_mid, bird_image_up]
bird_image = bird_list[bird_list_index]

# FONTS --> FLAPPY BIRD
game_font = pygame.font.Font("assets/font/Flappy.TTF", 40)

# SOUNDS
win_sound = pygame.mixer.Sound("assets/sound/smb_stomp.wav")
game_over_sound = pygame.mixer.Sound("assets/sound/smb_mariodie.wav")


# FUNCTION
def generate_pipe_rect():
    random_pipes = random.randrange(250, 500)
    pipe_rect_top = pipe_image.get_rect(midbottom=(630, random_pipes - 150))
    pipe_rect_botton = pipe_image.get_rect(midtop=(630, random_pipes))
    return pipe_rect_top, pipe_rect_botton


def move_pipe_rect(pipes):
    for pipe in pipe_list:
        pipe.centerx -= 5
    inside_pipes = [pipe for pipe in pipes if pipe.right > -50]
    return pipes


def display_pipes(pipes):
    for pipe in pipes:
        if pipe.bottom >= 630:
            main_screen.blit(pipe_image, pipe)
        else:
            reversed_pipes = pygame.transform.flip(pipe_image, False, True)
            main_screen.blit(reversed_pipes, pipe)


def check_collisin(pipes):
    global active_score
    for pipe in pipes:
        if bird_image_rect.colliderect(pipe):
            game_over_sound.play()
            time.sleep(3)
            active_score = True
            return False

        if bird_image_rect.top <= -50 or bird_image_rect.bottom >= 560:
            game_over_sound.play()
            time.sleep(3)
            active_score = True
            return False
        game_over_sound.play()

    return True


def bird_animation():
    new_bird = bird_list[bird_list_index]
    new_bird_rect = new_bird.get_rect(center=(100, bird_image_rect.centery))
    return new_bird, new_bird_rect


def display_score(status):
    if status == "active":
        text1 = game_font.render(str(score), False, (255, 255, 255))
        text1_rect = text1.get_rect(center=(170, 50))
        main_screen.blit(text1, text1_rect)
    if status == "game_over":
        # SCRORE
        text1 = game_font.render(
            str(f"Score : {score}"), False, (255, 255, 255))
        text1_rect = text1.get_rect(center=(170, 50))
        main_screen.blit(text1, text1_rect)

        # HIGHT SCORE
        text2 = game_font.render(
            str(f"HightScore : {hight_score}"), False, (255, 255, 255))
        text2_rect = text2.get_rect(center=(170, 500))
        main_screen.blit(text2, text2_rect)


def update_score():
    global score, hight_score, active_score
    if pipe_list:
        for pipe in pipe_list:
            if 95 < pipe.centerx < 105 and active_score == True:
                win_sound.play()
                score += 1
                active_score = False
            if pipe.centerx < 0:

                active_score = True

    if score > hight_score:
        hight_score = score

    return hight_score


# REACTANGLES
bird_image_rect = bird_image.get_rect(center=(78, 300))


# USER EVENTS
create_flap = pygame.USEREVENT + 1
pygame.time.set_timer(create_flap, 100)

create_pipe = pygame.USEREVENT
pygame.time.set_timer(create_pipe, 1200)


# GAME DISPLAY
main_screen = pygame.display.set_mode((display_width, display_height))


# GAME TIMER
clock = pygame.time.Clock()


# GAME LOGIC
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            # END PYGAME MODULS
            pygame.quit()

            # TERMINATE PROGRAM
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bird_movement = 0
                bird_movement -= 5
            if event.key == pygame.K_r and game_status == False:
                game_status = True
                pipe_list.clear()
                bird_image_rect.center = (78, 300)
                bird_movement = 0

        if event.type == create_pipe:
            pipe_list.extend(generate_pipe_rect())

        if event.type == create_flap:

            if bird_list_index < 2:
                bird_list_index += 1

            else:
                bird_list_index = 0

            bird_image, bird_image_rect = bird_animation()

    floor_x -= 1

    if floor_x <= -340:
        floor_x = 0

    # DISPLAY BACK GROUND IMAGE --> BG1.PNG
    main_screen.blit(backgound_image, (0, 0))

    if game_status:
        # CHECK COLLISINON
        check_collisin(pipe_list)

        # DISPLAY BIRD IMAGE --> RED_BIRD_MID_FLAP.PNG
        main_screen.blit(bird_image, bird_image_rect)

        # CHECK FOR COLLISION
        game_status = check_collisin(pipe_list)

        # DISPLAY PIPES
        pipe_list = move_pipe_rect(pipe_list)
        display_pipes(pipe_list)

        # FLOOR GRAVITY AND BIRD MOVEMENT
        bird_movement += gravity
        bird_image_rect.centery += bird_movement

        # DISPLAY GAME SCORE
        update_score()
        display_score("active")

    else:
        main_screen.blit(game_over_image, game_over_image_rect)
        display_score("game_over")

    # DISPLAY FLOOR IMAGE --> FLOOR.PNG
    main_screen.blit(floor_image, (floor_x, 560))
    main_screen.blit(floor_image, (floor_x + 340, 560))

    pygame.display.update()
    # SET GAME SPEED
    clock.tick(70)
