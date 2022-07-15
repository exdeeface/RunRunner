import pygame

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
    
        #define player images
        self.player_walk1 = pygame.image.load("graphics/Player/player_walk_1.png").convert_alpha()
        self.player_walk2 = pygame.image.load("graphics/Player/player_walk_2.png").convert_alpha()
        self.player_jump = pygame.image.load("graphics/Player/jump.png").convert_alpha()

        #player walk cycle images
        self.player_walk = [self.player_walk1, self.player_walk2]
        self.walk_index = 0

        #set initial sprite image
        self.image = pygame.image.load("graphics/Player/player_walk_1.png").convert_alpha()
        self.rect = self.image.get_rect(midbottom = (80, 300))

        self.jump_audio = pygame.mixer.Sound("audio/jump.mp3")
        self.jump_audio.set_volume(0.05)

        #initialise player gravity and movement
        self.grav = 0
        self.speed = 0
        self.left = False
        self.right = False
        
        #check if player jumping or in the air already
        self.is_jump = False
        self.disable_jump = True
        self.in_pit = False

        self.game_begin = False

    def player_input(self):
        #check state of all keys
        keys = pygame.key.get_pressed()

        #check pressed keys and change values accordingly
        if keys[pygame.K_SPACE]:
            #check if player is already in the air, if so do nothing
            if self.disable_jump == True: pass
            else:
                #changes gravity to move player sprite upwards
                self.jump_audio.play()
                self.is_jump = True
                self.grav = -15

        #set boolean value to true if pressing left
        if keys[pygame.K_a]: self.left = True
        else: self.left = False

        #set boolean value to true if pressing right
        if keys[pygame.K_d]: self.right = True
        else: self.right = False

    #changes y sprite value by the current gravity value
    def apply_grav(self):

        #increase by 1 each frame
        self.grav += 1
        self.rect.y += self.grav
    
        #gravity doesn't increase when in contact with the floor (and not in a pit)
        if self.in_pit == False:
            if self.rect.bottom >= 300:
                self.rect.bottom = 300
                self.grav = 0
        
        #if player falls into a pit the game is over
        #this check can be moved somewhere more appropriate
        if self.rect.top >= 425: self.game_begin = False

    #updates player sprite based on current horizontal speed
    def apply_movement(self):

        #increase speed in desired direction
        if self.right == True: self.speed += 2
        if self.left == True: self.speed -= 2

        #set a max speed for both directions
        if self.speed > 12: self.speed = 12
        if self.speed < -12: self.speed = -12

        #disable jump if already in the air (no double jumps here) :-(
        if self.is_jump == True: self.disable_jump = True

        #reset boolean upon contact wit the floor
        if self.rect.bottom == 300: self.disable_jump = False

        #force player to remain on the screen
        if self.rect.left < 0: self.rect.left = 0
        if self.rect.right > 800: self.rect.right = 800

        #decrease speed upon letting go of either horizontal keys
        if self.right == False and self.speed > 0:
            self.speed += -1
            #horizontal speed will return to 0
            if self.speed < 0: self.speed = 0

        if self.left == False and self.speed < 0:
            self.speed += 1
            if self.speed > 0: self.speed = 0

        #update sprite with speed
        self.rect.x += self.speed

    #check if player sprite collides with any obstacles
    def check_player_collision(self, obstacle_group):

        #check for each obstacle on screen if the player rect collides
        for each in obstacle_group:
            if self.rect.colliderect(each):

                #400 is the y value of pits, where we want the player to fall a little before game over
                if each.rect.bottom == 400:

                    #values are extended a little to make the collision feel a bit more natural
                    if self.rect.left > each.rect.left - 12 and self.rect.right < each.rect.right + 12:
                        self.in_pit = True
                        break

                #end game upon collision with an enemy
                else: self.game_begin = False

    #change player image depending on the current state
    def animate_player(self):
        #set sprite to jump image
        if self.rect.bottom < 300: self.image = self.player_jump
        else:

            #increase walk cycle by float and read as an integer so it is updated every few frames rather than each frame
            self.walk_index += 0.3
            if self.walk_index > len(self.player_walk): self.walk_index = 0
            self.image = self.player_walk[int(self.walk_index)]

    #set initial states for the next attempt
    def reset(self):
        self.rect.bottom = 0
        self.rect.left = 80
        self.grav = 0
        self.speed = 0
        self.left = False
        self.right = False
        self.is_jump = False
        self.disable_jump = True
        self.in_pit = False

    #update player sprite entirely    
    def update(self, obstacle_group):      
        self.player_input()
        self.apply_grav()
        self.apply_movement()
        self.animate_player()
        self.check_player_collision(obstacle_group)
        if self.game_begin == False: self.reset()