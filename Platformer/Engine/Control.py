import sys

import pygame


class KeyState:
  def __init__(self):
    self.up = False
    self.down = False
    self.left = False
    self.right = False


def ProcessPygameEvents(controllers, key_states):
    controllerKeys = [[pygame.locals.K_UP,pygame.locals.K_DOWN,pygame.locals.K_LEFT,pygame.locals.K_RIGHT],\
                [pygame.locals.K_w,pygame.locals.K_s,pygame.locals.K_a,pygame.locals.K_d]]
    game_state = {"Exit": False}
    for event in pygame.event.get():  # event loop
        if event.type == pygame.locals.QUIT:
            game_state['Exit'] = True
        for controller in controllers:
            if event.type == pygame.locals.KEYDOWN:
                if event.key == controllerKeys[controller][0]:
                    key_states[controller].up = True
                if event.key == controllerKeys[controller][1]:
                    key_states[controller].down = True
                if event.key == controllerKeys[controller][2]:
                    key_states[controller].left = True
                if event.key == controllerKeys[controller][3]:
                    key_states[controller].right = True
            if event.type == pygame.locals.KEYUP:
                if event.key == controllerKeys[controller][0]:
                    key_states[controller].up = False
                if event.key == controllerKeys[controller][1]:
                    key_states[controller].down = False
                if event.key == controllerKeys[controller][2]:
                    key_states[controller].left = False
                if event.key == controllerKeys[controller][3]:
                    key_states[controller].right = False

    return game_state, key_states