import os

import pygame

SPRITES_DIR = os.path.join(os.path.dirname(os.path.realpath(__file__)), "..", "Resources", "sprites")

def LoadSprites():
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

sprites = LoadSprites()