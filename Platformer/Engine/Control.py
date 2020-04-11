import sys

import pygame


class KeyState:

    def __init__(self):
        self.up = False
        self.up_K_DOWN = False
        self.up_K_UP = False
        self.down = False
        self.up_K_DOWN = False
        self.up_K_UP = False
        self.left = False
        self.up_K_DOWN = False
        self.up_K_UP = False
        self.right = False
        self.up_K_DOWN = False
        self.up_K_UP = False


def ProcessPygameEvents(controllers, key_states):
    controllerKeys = [[pygame.locals.K_UP,pygame.locals.K_DOWN,pygame.locals.K_LEFT,pygame.locals.K_RIGHT],\
                [pygame.locals.K_w,pygame.locals.K_s,pygame.locals.K_a,pygame.locals.K_d]]
    game_state = {"Exit": False}
    for controller in controllers:
        key_states[controller].up_K_DOWN = False
        key_states[controller].up_K_UP = False
        key_states[controller].down_K_DOWN = False
        key_states[controller].down_K_UP = False
        key_states[controller].left_K_DOWN = False
        key_states[controller].left_K_UP = False
        key_states[controller].right_K_DOWN = False
        key_states[controller].right_K_UP = False
    for event in pygame.event.get():  # event loop
        if event.type == pygame.locals.QUIT:
            game_state['Exit'] = True
        for controller in controllers:
            if event.type == pygame.locals.KEYDOWN:
                if event.key == controllerKeys[controller][0]:
                    key_states[controller].up = True
                    key_states[controller].up_K_DOWN = True
                if event.key == controllerKeys[controller][1]:
                    key_states[controller].down = True
                    key_states[controller].down_K_DOWN = True
                if event.key == controllerKeys[controller][2]:
                    key_states[controller].left = True
                    key_states[controller].left_K_DOWN = True
                if event.key == controllerKeys[controller][3]:
                    key_states[controller].right = True
                    key_states[controller].right_K_DOWN = True
            if event.type == pygame.locals.KEYUP:
                if event.key == controllerKeys[controller][0]:
                    key_states[controller].up = False
                    key_states[controller].up_K_UP = True
                if event.key == controllerKeys[controller][1]:
                    key_states[controller].down = False
                    key_states[controller].down_K_UP = True
                if event.key == controllerKeys[controller][2]:
                    key_states[controller].left = False
                    key_states[controller].left_K_UP = True
                if event.key == controllerKeys[controller][3]:
                    key_states[controller].right = False
                    key_states[controller].right_K_UP = True

    return game_state, key_states