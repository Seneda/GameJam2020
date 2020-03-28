import os
import pygame

SPRITES_DIR = os.path.join(os.path.dirname(os.path.realpath(__file__)), "..", "sprites")

class Character():
    def __init__(self,screen,name):
        """Initialise the monkey and set its starting position"""
        self.screen = screen
        self.name = name

        self.sprites = self.LoadSprites()

        #Load image and get its rect.
        # self.image = pygame.image.load('../sprites/' +name +'_walk' +'.png')
        # self.rect = self.image.get_rect()
        # self.screen_rect = screen.get_rect()

        self.centerxfloat = 0
        self.centeryfloat = 0
        # self.rect.centerx = 0
        # self.rect.centery = 0

        self.speed = [0,0] # speed in x,y notation (right and up)
        self.pos = [50,50]

    def LoadSprites(self):
        print("Loading Sprites...")
        sprites = {}
        for _, sprite_dirs, _ in os.walk(SPRITES_DIR):
            for sprite_name in sprite_dirs:
                print("Loading {}".format(sprite_name))
                sprites.setdefault(sprite_name, {})
                for _, _, animation_files in os.walk(os.path.join(SPRITES_DIR, sprite_name)):
                    for animation_name in animation_files:
                        try:
                            print("Loading {}".format(animation_name))
                            print(animation_name)
                            animation_type = animation_name.split('_')[0]
                            animation_num = animation_name.split('_')[1].replace('.png', '')
                            sprites[sprite_name].setdefault(animation_type, {})[int(animation_num)] = pygame.image.load(
                                os.path.join(SPRITES_DIR, sprite_name, animation_name))
                        except Exception as e:
                            print("Couldn't load {}".format(animation_name))
                            print(e)
        print(sprites)
        return sprites

    def updatePos(self,key_state,time_passed_ms):
        acceleration = 1
        jump_speed = 20
        gravity = 10

        if key_state['Right']:
            self.speed[0] += (acceleration)*(time_passed_ms)
        if key_state['Left']:
            self.speed[0] -= (acceleration)*(time_passed_ms)
        # if key_state['Down']:
     #      self.speed[1] += (acceleration)*(time_passed_ms)
        if key_state['Up']:
            self.speed[1] = -jump_speed

        self.speed[1] += gravity*time_passed_ms
        self.pos[0] = self.pos[0] + self.speed[0]
        self.pos[1] = self.pos[1] + self.speed[1]
        print(self.pos)

    def updateDraw(self,display):
        display.blit(self.sprites[self.name]['walk'][0], self.pos)

