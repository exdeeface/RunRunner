import pygame
from random import randint

class Obstacle(pygame.sprite.Sprite):
    def __init__(self, game_level):
        super().__init__()

        self.game_level = game_level

    #remove the sprite from memory if it reaches a certain value offscreen
    def destroy(self):
        if self.rect.x <= -100: self.kill()

    #increase sprite index by a float and read as an int to proceed to the next image every x frames
    def animate(self):
        self.animation_index += 0.1
        if self.animation_index > 2: self.animation_index = 0
        self.image = self.animation_frames[int(self.animation_index)]

    #update sprite entirely
    def update(self, game_speed):
        self.animate()
        self.rect.x -= game_speed
        self.destroy()

class Fly(Obstacle):
    def __init__(self, game_level):
        super().__init__(game_level)

        self.fly1 = pygame.image.load("graphics/Fly/fly1.png").convert_alpha()
        self.fly2 = pygame.image.load("graphics/Fly/fly2.png").convert_alpha()

        self.animation_frames = [self.fly1, self.fly2]
        self.animation_index = 0
        
        self.image = self.animation_frames[self.animation_index]
        self.rect = self.image.get_rect(midbottom = (randint(850, 1000 + game_level * 50), randint(125, 180)))

class Snail(Obstacle):
    def __init__(self, game_level):
        super().__init__(game_level)

        self.snail1 = pygame.image.load("graphics/Snail/snail1.png").convert_alpha()
        self.snail2 = pygame.image.load("graphics/Snail/snail2.png").convert_alpha()
        
        self.animation_frames = [self.snail1, self.snail2]
        self.animation_index = 0
        
        self.image = self.animation_frames[self.animation_index]
        self.rect = self.image.get_rect(midbottom = (randint(850, 1000 + game_level * 50), 300))

class Pit(Obstacle):
    def __init__(self, game_level):
        super().__init__(game_level)
 
        self.image = pygame.image.load("graphics/pit.png").convert_alpha()
        self.rect = self.image.get_rect(midbottom = (randint(850, 1000 + game_level * 50), 400))

    def animate(self): pass