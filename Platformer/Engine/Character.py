import math

import pygame

from Engine.Sprites import sprites, sprite_speeds


class Character():
    def __init__(self, name, pos):
        self.name = name

        self.speed = [0, 0]  # speed in x,y notation (right and up)
        self.rect = pygame.Rect(*pos, 32, 32)
        self.collision_rect = pygame.Rect(*pos, 24, 32)
        self.jump_timer = 1000
        self.run_acceleration = 500*60
        self.jump_acceleration = 16 * 50 * 2 * 2
        self.gravity = 5 * 9.81 * 16  # 16 pixels = 1m

        self.animation_timer = 0
        self.animation_type = "idle_left"
        self.collisions = []

    @property
    def x(self):
        return self.rect.x

    @x.setter
    def x(self, val):
        self.rect.x = val
        self.collision_rect.x = val + 4

    @property
    def y(self):
        return self.rect.y

    @y.setter
    def y(self, val):
        self.rect.y = val
        self.collision_rect.y = val

    @property
    def pos(self):
        return (self.x, self.y)

    @pos.setter
    def pos(self, val):
        self.x = val[0]
        self.y = val[1]\

    @property
    def state(self):
        return (*self.pos, *self.speed)

    @state.setter
    def state(self, val):
        self.x = val[0]
        self.y = val[1]
        self.speed[0] = val[2]
        self.speed[1] = val[3]

    def updatePos(self, time_passed_s, collision_objects, key_state=None):
        if time_passed_s == 0:
            return
        self.animation_timer += time_passed_s
        self.jump_timer += time_passed_s
        self.speed[1] += self.gravity * time_passed_s
        if key_state is not None:
            self.speed[0] = 0
            if key_state.right:
                self.speed[0] += self.run_acceleration * time_passed_s
            if key_state.left:
                self.speed[0] -= self.run_acceleration * time_passed_s
            if key_state.up:
                # limits how long you can hold jump for and keep accelerating upwards, but allows you to do a small jump by tapping and hold for up to 0.2s for a longer jump
                if (self.jump_timer > 0.5) or (self.jump_timer < 0.2):
                    self.speed[1] -= self.jump_acceleration * time_passed_s
                    if self.jump_timer > 0.5:
                        self.jump_timer = 0

        MAXSPEED = 8 / time_passed_s

        self.speed[0] = min(MAXSPEED, max(-MAXSPEED, self.speed[0]))
        self.speed[1] = min(MAXSPEED, max(-MAXSPEED, self.speed[1]))
        if abs(self.speed[0]) > abs(self.speed[1]):
            self.x = self.x + float(self.speed[0]) * time_passed_s
            self.detect_collisions(collision_objects)
            self.y = self.y + float(self.speed[1]) * time_passed_s
            self.detect_collisions(collision_objects)
        else:
            self.y = self.y + float(self.speed[1]) * time_passed_s
            self.detect_collisions(collision_objects)
            self.x = self.x + float(self.speed[0]) * time_passed_s
            self.detect_collisions(collision_objects)

        last_animation = self.animation_type

        if self.speed[0] > 0:
            self.animation_type = "walk_right"
        elif self.speed[0] < 0:
            self.animation_type = "walk_left"
        else:
            if 'left' in self.animation_type:
                self.animation_type = 'idle_left'
            else:
                self.animation_type = 'idle_right'

        if abs(self.speed[1]) > 10:
            if self.speed[0] > 0:
                self.animation_type = "jump_right"
            elif self.speed[0] < 0:
                self.animation_type = "jump_left"
            else:
                if 'left' in self.animation_type:
                    self.animation_type = 'jump_left'
                else:
                    self.animation_type = 'jump_right'

        if self.animation_type != last_animation:
            self.animation_timer = 0

    def detect_collisions(self, collision_objects):
        #     self.collision_rect = self.rect.copy()
        #     self.collision_rect.width = 24
        #     # self.collision_rect.width = 24
        #     self.collision_rect.center = self.rect.center
        self.collisions = sorted([r for r in collision_objects if self.collision_rect.colliderect(r)],
                                 key=lambda x: math.hypot(x.centerx - self.collision_rect.centerx,
                                                          x.centery - self.collision_rect.centery))
        collision_counter = 0
        while self.collisions:
            if collision_counter > 10:
                break
            collision_counter += 1
            for collision in self.collisions:

                if self.collision_rect.centery < collision.top:
                    self.speed[1] = 0
                    self.collision_rect.bottom = collision.top
                    self.rect.center = self.collision_rect.center
                    self.collisions = sorted([r for r in collision_objects if self.collision_rect.colliderect(r)],
                                             key=lambda x: math.hypot(x.centerx - self.collision_rect.centerx,
                                                                      x.centery - self.collision_rect.centery))
                    break
                if self.collision_rect.centerx < collision.left:
                    self.speed[0] = 0
                    self.collision_rect.right = collision.left
                    self.rect.center = self.collision_rect.center
                    self.collisions = sorted([r for r in collision_objects if self.collision_rect.colliderect(r)],
                                             key=lambda x: math.hypot(x.centerx - self.collision_rect.centerx,
                                                                      x.centery - self.collision_rect.centery))
                    break
                if self.collision_rect.centerx > collision.right:
                    self.speed[0] = 0
                    self.collision_rect.left = collision.right
                    self.rect.center = self.collision_rect.center
                    self.collisions = sorted([r for r in collision_objects if self.collision_rect.colliderect(r)],
                                             key=lambda x: math.hypot(x.centerx - self.collision_rect.centerx,
                                                                      x.centery - self.collision_rect.centery))
                    break
                if self.collision_rect.centery > collision.bottom:
                    self.speed[1] = 0
                    self.collision_rect.top = collision.bottom
                    self.rect.center = self.collision_rect.center
                    self.collisions = sorted([r for r in collision_objects if self.collision_rect.colliderect(r)],
                                             key=lambda x: math.hypot(x.centerx - self.collision_rect.centerx,
                                                                      x.centery - self.collision_rect.centery))
                    break
                # if self.collision_rect.centery > collision.top:
                #     self.speed[1] = 0
                #     self.collision_rect.top = collision.bottom
                #     self.collisions = sorted([r for r in collision_objects if self.collision_rect.colliderect(r)],
                #                              key=lambda x: math.hypot(x.centerx - self.collision_rect.centerx,
                #                                                       x.centery - self.collision_rect.centery))

                print("Collision Iteration : {}".format(collision_counter))
                break

    def updateDraw(self, display, minimap, scroll):
        # display.blit(pygame.font.SysFont('Arial', 10).render('{:.1f}'.format(self.speed[0]), True, (0, 0, 0)),
        #              (self.rect.x - scroll[0], self.rect.y - scroll[1] - 10))
        # display.blit(pygame.font.SysFont('Arial', 10).render('{:.1f}'.format(self.speed[1]), True, (0, 0, 0)),
        #              (self.rect.x - scroll[0] + 24, self.rect.y - scroll[1] - 10))
        display.blit(sprites[self.name][self.animation_type][
                         int(self.animation_timer * sprite_speeds[self.name][self.animation_type]) % len(sprites[self.name][self.animation_type])],
                     (self.x - scroll[0], self.y - scroll[1]))

        if minimap is not None:
            if self.collisions:
                pygame.draw.rect(minimap, (255, 0, 0), self.rect)
                # minimap.blit(pygame.font.SysFont('Arial', 20).render('{}'.format(len(self.collisions)), True, (0, 0, 0)),
                #              (self.rect.centerx - 4, self.rect.centery - 10))
            else:
                pygame.draw.rect(minimap, (0, 255, 0), self.rect)
                pygame.draw.rect(minimap, (0, 0, 255), self.collision_rect)
