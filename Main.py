import pygame
from Obstacle import *
from Player import *
from sys import exit
from random import randint, randrange

#draw a scrolling background to the screen
def draw_background():
    global ground_start, sky_start
    sky_start -= 1
    ground_start -= game_speed

    #repeats every 784 pixels to repeat the pattern on the ground texture smoothly
    if ground_start <= -784: ground_start = 0
    if sky_start <= -800:  sky_start = 0

    #draw two of each sky/background to convincinly repeat itself ///this can be optimised in the future with a smaller secondary texture
    screen.blit(sky_background, (sky_start, 0))
    screen.blit(sky_background, (sky_start + 800, 0))
    screen.blit(ground, (ground_start, 300))
    screen.blit(ground, (ground_start + 784, 300))

#increments player score
def add_points():
    global score, high_score, show_message
    score += int(1 * point_multiplier)
    if score > high_score: 
        high_score = score
        show_message = True

#adds an enemy to the obstacle sprite group
def spawn_enemy():
    obstacle_type = randint(0, 2)
    if obstacle_type == 0: obstacle_group.add(Snail(game_level))
    elif obstacle_type == 1: obstacle_group.add(Fly(game_level))
    elif obstacle_type == 2: obstacle_group.add(Pit(game_level))

#continuously checks for certain keypresses or custom event timers
def check_events():
    global ground_start, sky_start, music_started, game_speed, game_level, point_multiplier, score, motivation_timer_lenth, motivate, show_message, already_shown
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            
            pygame.display.quit()
            pygame.quit()
            exit()

        #reset some variables when the game restarts
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                if player.game_begin == False:
                    obstacle_group.empty()
                    ground_start = 0
                    sky_start = 0
                    player.game_begin = True
                    music_started = False
                    game_speed = 4
                    game_level = 1
                    point_multiplier = 1
                    score = 0
                    motivation_timer_lenth = 90
                    motivate = False
                    show_message = False
                    already_shown = False

            #pressing escape will end the run and return to menu
            if event.key == pygame.K_ESCAPE: player.game_begin = False
    
        if event.type == point_timer and player.game_begin: add_points()

        #spawns 1 of three obstacle types by adding it to the obstacle_rect_list
        if event.type == spawn_timer and player.game_begin: spawn_enemy()

        if event.type == difficulty_timer and player.game_begin: increase_game_speed()
    
#display score on screen
def display_score(score):
    global motivate
    score_surf = default_font.render(str(score), False, (64, 64, 64))
    score_rect = score_surf.get_rect(midleft = (798 - score_surf.get_width(), 20))
    screen.blit(score_surf, score_rect)

    #display motivation upon certain point thresholds
    if score > 0 and score % 15 == 0: motivate = True

#display a message onscreen congratulating the player for being so good at this game
def motivate_player():
    global motivate, motivation_text, prev_motivation_text, is_motivating, motivation_timer
    if motivate == True:
        if is_motivating == False:
            while True:
                motivation_text = motivation_list[randrange(0, len(motivation_list))]

                #check if the motivation text is the same as before, and if so, select another one ///find something more elegant, this could have poor performance if you're unlucky
                if motivation_text != prev_motivation_text: break
            is_motivating = True

        if motivation_timer > 0:
            if show_message and not already_shown: pass
            else: 
                motivation_timer -= 1
            
                motiv_surf = large_font.render(motivation_text, False, (49, 127, 134))
                motiv_rect = motiv_surf.get_rect(center = (800/2, 35))
                screen.blit(motiv_surf, motiv_rect)

        #reset timer once it reaches 0
    if motivation_timer == 0:
        motivation_timer = 90
        motivate = False
        is_motivating = False
        #store last used motivation so it won't be used consecutively
        prev_motivation_text = motivation_text

def high_score_message():
    global show_message, already_shown, message_timer, motivate

    if show_message and not already_shown:
        motivate = False
        if message_timer > 0:
            message_timer -= 1
            
            motiv_surf = large_font.render("new high score!", False, (200, 200, 80))
            motiv_rect = motiv_surf.get_rect(center = (800/2, 35))
            screen.blit(motiv_surf, motiv_rect)

        #reset timer once it reaches 0
    if message_timer == 0:
        message_timer = 90
        show_message = False
        already_shown = True

#some messages congratulating the player
motivation_list = ["Great job!", "Keep it up!", "Nice moves!", "buy more cat food", "Woah!", "Bravo!", "Astonishing!", "Formidable!", "Holy hotdog!"]
motivate = False
is_motivating = False
show_message = False
already_shown = False
message_timer = 90
motivation_timer = 90

#used for storing and checking the last message so it isn't repeated
prev_motivation_text = ""
motivation_text = ""

point_multiplier = 1

def increase_game_speed():
    global game_speed, point_multiplier, game_level
    game_speed = 4 + game_level
    game_level += 1
    if point_multiplier < 6: point_multiplier += 0.5

def game_loop():
    global music_started
    if not music_started:
        background_music.play(loops = -1)
        music_started = True

    #move ground and sky left at different speed for the illusion of depth
    draw_background()
            
    #display player and obstacles on screen
    obstacle_group.draw(screen)
    playerSingle.draw(screen)

    #update obstacles
    obstacle_group.update(game_speed)
    playerSingle.update(obstacle_group)
    display_score(score)

    #display motivational messages at certain score thresholds
    motivate_player()
    high_score_message()

def menu_loop():
    global sky_start, ground_start
    background_music.stop()
    draw_background()
    screen.blit(menu_image, menu_rect)

    if score == 0:     
        screen.blit(control_surf, control_rect)
        screen.blit(begin_surf, begin_rect)
    else:
        #display the current high score instead of controls
        high_score_text = "High Score: {}".format(high_score)
        high_score_surf = large_font.render(high_score_text, False, (200, 200, 80))
        high_score_rect = high_score_surf.get_rect(midleft = (795 - high_score_surf.get_width(), 30))
        screen.blit(high_score_surf, high_score_rect)
        screen.blit(replay_surf, replay_rect)

pygame.init()
screen = pygame.display.set_mode((800, 400))
pygame.display.set_caption("RUN RUNNER")
clock = pygame.time.Clock()

#initialise player sprite and class
player = Player()
playerSingle = pygame.sprite.GroupSingle()
playerSingle.add(player)

obstacle_group = pygame.sprite.Group()

default_font = pygame.font.Font("font/Pixeltype.ttf", 50)
large_font = pygame.font.Font("font/Pixeltype.ttf", 70)

#various prompts on starting screen
control_surf = large_font.render("WASD to move, and SPACE to jump!", False, (200, 200, 80))
control_rect = control_surf.get_rect(midleft = (795 - control_surf.get_width(), 30))
begin_surf = default_font.render("Press ENTER to begin!", False, (200, 200, 80))
begin_rect = begin_surf.get_rect(midleft = (795 - begin_surf.get_width(), 70))
replay_surf = default_font.render("Press ENTER to retry!", False, (200, 200, 80))
replay_rect = replay_surf.get_rect(midleft = (795 - replay_surf.get_width(), 70))
menu_image = pygame.image.load("graphics/menu.png").convert_alpha()
menu_rect = menu_image.get_rect()

sky_background = pygame.image.load("graphics/Sky.png").convert()
ground = pygame.image.load("graphics/ground.png").convert()
ground_start = 0
sky_start = 0

background_music = pygame.mixer.Sound("audio/music.wav")
background_music.set_volume(0.08)
music_started = False

point_timer = pygame.USEREVENT + 1
pygame.time.set_timer(point_timer, 500)

#periodically spawns enemies
spawn_timer = pygame.USEREVENT + 2
pygame.time.set_timer(spawn_timer, 1300)

#increases difficulty every set period
difficulty_timer = pygame.USEREVENT + 3
pygame.time.set_timer(difficulty_timer, 12000)

#set state and initial values
score = 0
high_score = 14
game_speed = 4
game_level = 1

#simplified pygame loop
while 1:
    check_events()
    if player.game_begin: game_loop()
    else: menu_loop()
    pygame.display.update()
    clock.tick(60)
