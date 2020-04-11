import math
from abc import ABC, abstractmethod

import pygame

from Engine.Sprites import sprites, sprite_speeds


class CharacterBase(ABC):
    def __init__(self, name, start_pos):
        self.name = name

        self.speed = [0, 0]  # speed in x,y notation (right and up)
        self.movement = [0, 0]
        self.rect = pygame.Rect(*start_pos, 32, 32)
        self.last_pos = self.pos
        self.collision_rect = pygame.Rect(*start_pos, 24, 32)

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
        return self.x, self.y

    @pos.setter
    def pos(self, val):
        self.x = val[0]
        self.y = val[1]

    @property
    def state(self):
        return (*self.pos, *self.speed)

    @state.setter
    def state(self, val):
        self.x = val[0]
        self.y = val[1]
        self.speed[0] = val[2]
        self.speed[1] = val[3]

    @property
    def animation_frame(self):
        animation_speed = sprite_speeds[self.name][self.animation_type]
        return sprites[self.name][self.animation_type][
            int(self.animation_timer * animation_speed) % len(sprites[self.name][self.animation_type])]

    def updateDraw(self, display, minimap, scroll):
        # display.blit(pygame.font.SysFont('Arial', 10).render('{:.1f}'.format(self.speed[0]), True, (0, 0, 0)),
        #              (self.rect.x - scroll[0], self.rect.y - scroll[1] - 10))
        # display.blit(pygame.font.SysFont('Arial', 10).render('{:.1f}'.format(self.speed[1]), True, (0, 0, 0)),
        #              (self.rect.x - scroll[0] + 24, self.rect.y - scroll[1] - 10))

        self.updateAnimationType()
        display.blit(self.animation_frame,
                     (self.x - scroll[0], self.y - scroll[1]))

        if minimap is not None:
            if self.collisions:
                pygame.draw.rect(minimap, (255, 0, 0), self.rect)
                # minimap.blit(pygame.font.SysFont('Arial', 20).render('{}'.format(len(self.collisions)), True, (0, 0, 0)),
                #              (self.rect.centerx - 4, self.rect.centery - 10))
            else:
                pygame.draw.rect(minimap, (0, 255, 0), self.rect)
                pygame.draw.rect(minimap, (0, 0, 255), self.collision_rect)

    @abstractmethod
    def updateState(self, time_passed_s, collision_objects, key_state=None):
        pass

    @abstractmethod
    def detectCollisions(self, collidable_objects):
        pass

    @abstractmethod
    def updateAnimationType(self):
        pass


def load_character(name, pos):
    characters = {"Batman": FlyingCharacter,
                  "Scuttlefish": SliderCharacter}

    return characters.get(name, NormalCharacter)(name, pos)


class NormalCharacter(CharacterBase):
    def __init__(self, name, start_pos):
        super().__init__(name, start_pos)
        self.run_acceleration = 2000 # a quick boost of acceleration
        self.run_speed = 250 # max speed, previous: 250
        self.jump_speed = 6 * 32
        self.keyheld_gravity = 9.81 * 40 # gravity if moving downwards
        self.normal_gravity = 9.81 * 100 # gravity if moving upwards

    def updateState(self, time_passed_s, collision_objects, key_state=None):
        self.last_pos = self.pos
        if time_passed_s == 0:
            return
        self.animation_timer += time_passed_s
        gravity = self.normal_gravity
        if key_state is not None:
            if key_state.right:
                self.speed[0] += self.run_acceleration * time_passed_s
                self.speed[0] = min(self.run_speed,self.speed[0])
            elif key_state.left:
                self.speed[0] -= self.run_acceleration * time_passed_s
                self.speed[0] = max(-self.run_speed,self.speed[0])
            else: 
                self.speed[0] = 0
            if key_state.up_K_DOWN:
                gravity = self.keyheld_gravity
                # limits how long you can hold jump for and keep accelerating upwards, but allows you to do a small jump by tapping and hold for up to 0.2s for a longer jump
                if (self.speed[1] == 0):
                    self.speed[1] -= self.jump_speed
            if ((key_state.up)and(self.speed[1]<0)): #if holding up key and moving up
                gravity = self.keyheld_gravity

        self.speed[1] += gravity * time_passed_s

# ToDo: probably should know if this or something else is capping the speed (otherwise our speed depends on the framerate)
        # MAXSPEED = 8 / time_passed_s

        # self.speed[0] = min(MAXSPEED, max(-MAXSPEED, self.speed[0]))
        # self.speed[1] = min(MAXSPEED, max(-MAXSPEED, self.speed[1]))

        if abs(self.speed[0]) > abs(self.speed[1]):
            self.x = self.x + float(self.speed[0]) * time_passed_s
            self.detectCollisions(collision_objects)
            self.y = self.y + float(self.speed[1]) * time_passed_s
            self.detectCollisions(collision_objects)
        else:
            self.y = self.y + float(self.speed[1]) * time_passed_s
            self.detectCollisions(collision_objects)
            self.x = self.x + float(self.speed[0]) * time_passed_s
            self.detectCollisions(collision_objects)

        self.movement = [self.pos[i] - self.last_pos[i] for i in range(len(self.pos))]

    def updateAnimationType(self):
        last_animation = self.animation_type

        if self.movement[0] > 0:
            self.animation_type = "walk_right"
        elif self.movement[0] < 0:
            self.animation_type = "walk_left"
        else:
            if 'left' in self.animation_type:
                self.animation_type = 'idle_left'
            else:
                self.animation_type = 'idle_right'

        if abs(self.speed[1]) > 0:
            if self.movement[0] > 0:
                self.animation_type = "jump_right"
            elif self.movement[0] < 0:
                self.animation_type = "jump_left"
            else:
                if 'left' in self.animation_type:
                    self.animation_type = 'jump_left'
                else:
                    self.animation_type = 'jump_right'

        if self.name == "Batman":
            print(self.name, self.animation_type, self.speed)

        if self.animation_type != last_animation:
            self.animation_timer = 0

    def detectCollisions(self, collidable_objects):
        #     self.collision_rect = self.rect.copy()
        #     self.collision_rect.width = 24
        #     # self.collision_rect.width = 24
        #     self.collision_rect.center = self.rect.center
        self.collisions = sorted([r for r in collidable_objects if self.collision_rect.colliderect(r)],
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
                    self.collisions = sorted([r for r in collidable_objects if self.collision_rect.colliderect(r)],
                                             key=lambda x: math.hypot(x.centerx - self.collision_rect.centerx,
                                                                      x.centery - self.collision_rect.centery))
                    break
                if self.collision_rect.centerx < collision.left:
                    self.speed[0] = 0
                    self.collision_rect.right = collision.left
                    self.rect.center = self.collision_rect.center
                    self.collisions = sorted([r for r in collidable_objects if self.collision_rect.colliderect(r)],
                                             key=lambda x: math.hypot(x.centerx - self.collision_rect.centerx,
                                                                      x.centery - self.collision_rect.centery))
                    break
                if self.collision_rect.centerx > collision.right:
                    self.speed[0] = 0
                    self.collision_rect.left = collision.right
                    self.rect.center = self.collision_rect.center
                    self.collisions = sorted([r for r in collidable_objects if self.collision_rect.colliderect(r)],
                                             key=lambda x: math.hypot(x.centerx - self.collision_rect.centerx,
                                                                      x.centery - self.collision_rect.centery))
                    break
                if self.collision_rect.centery > collision.bottom:
                    self.speed[1] = 0
                    self.collision_rect.top = collision.bottom
                    self.rect.center = self.collision_rect.center
                    self.collisions = sorted([r for r in collidable_objects if self.collision_rect.colliderect(r)],
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


class DoubleJumpCharacter(NormalCharacter):

    def updateState(self, time_passed_s, collision_objects, key_state=None):
        self.last_pos = self.pos
        if time_passed_s == 0:
            return
        self.animation_timer += time_passed_s
        self.jump_timer += time_passed_s
        if key_state is not None:
            self.speed[0] = 0
            if key_state.right:
                self.speed[0] += self.run_acceleration * time_passed_s
            if key_state.left:
                self.speed[0] -= self.run_acceleration * time_passed_s
            if key_state.up:
                gravity = keyheld_gravity
                # limits how long you can hold jump for and keep accelerating upwards, but allows you to do a small jump by tapping and hold for up to 0.2s for a longer jump
                if (abs(self.speed[1]) < 1):
                    self.speed[1] -= self.jump_speed

        self.speed[1] += gravity * time_passed_s

        MAXSPEED = 8 / time_passed_s

        self.speed[0] = min(MAXSPEED, max(-MAXSPEED, self.speed[0]))
        self.speed[1] = min(MAXSPEED, max(-MAXSPEED, self.speed[1]))
        if abs(self.speed[0]) > abs(self.speed[1]):
            self.x = self.x + float(self.speed[0]) * time_passed_s
            self.detectCollisions(collision_objects)
            self.y = self.y + float(self.speed[1]) * time_passed_s
            self.detectCollisions(collision_objects)
        else:
            self.y = self.y + float(self.speed[1]) * time_passed_s
            self.detectCollisions(collision_objects)
            self.x = self.x + float(self.speed[0]) * time_passed_s
            self.detectCollisions(collision_objects)

        self.movement = [self.pos[i] - self.last_pos[i] for i in range(len(self.pos))]


class SliderCharacter(NormalCharacter):

    def updateState(self, time_passed_s, collision_objects, key_state=None):
        self.last_pos = self.pos
        if time_passed_s == 0:
            return
        self.animation_timer += time_passed_s
        gravity = self.normal_gravity
        if key_state is not None:
            # self.speed[0] = 0
            if key_state.right:
                self.speed[0] += self.run_acceleration * time_passed_s
            if key_state.left:
                self.speed[0] -= self.run_acceleration * time_passed_s
            if key_state.up:
                gravity = keyheld_gravity
                # limits how long you can hold jump for and keep accelerating upwards, but allows you to do a small jump by tapping and hold for up to 0.2s for a longer jump
                if (self.speed[1] == 0):
                    self.speed[1] -= self.jump_speed

        self.speed[1] += gravity * time_passed_s

        MAXSPEED = 8 / time_passed_s

        self.speed[0] = min(MAXSPEED, max(-MAXSPEED, self.speed[0]))
        self.speed[1] = min(MAXSPEED, max(-MAXSPEED, self.speed[1]))
        if abs(self.speed[0]) > abs(self.speed[1]):
            self.x = self.x + float(self.speed[0]) * time_passed_s
            self.detectCollisions(collision_objects)
            self.y = self.y + float(self.speed[1]) * time_passed_s
            self.detectCollisions(collision_objects)
        else:
            self.y = self.y + float(self.speed[1]) * time_passed_s
            self.detectCollisions(collision_objects)
            self.x = self.x + float(self.speed[0]) * time_passed_s
            self.detectCollisions(collision_objects)

        self.movement = [self.pos[i] - self.last_pos[i] for i in range(len(self.pos))]


class FlyingCharacter(NormalCharacter):

    def __init__(self, name, start_pos):
        super().__init__(name, start_pos)
        self.flying_acceleration = 100
        self.jump_timer = 0

    def updateState(self, time_passed_s, collision_objects, key_state=None):
        self.last_pos = self.pos
        if time_passed_s == 0:
            return
        self.animation_timer += time_passed_s
        self.jump_timer += time_passed_s
        if key_state is not None:
            if key_state.right:
                self.speed[0] += self.flying_acceleration * time_passed_s
            if key_state.left:
                self.speed[0] -= self.flying_acceleration * time_passed_s
            if key_state.up:
                self.speed[1] -= self.flying_acceleration * time_passed_s
            if key_state.down:
                self.speed[1] += self.flying_acceleration * time_passed_s

        self.speed[1] += gravity * time_passed_s

        MAXSPEED = 8 / time_passed_s

        self.speed[0] = min(MAXSPEED, max(-MAXSPEED, self.speed[0]))
        self.speed[1] = min(MAXSPEED, max(-MAXSPEED, self.speed[1]))
        if abs(self.speed[0]) > abs(self.speed[1]):
            self.x = self.x + float(self.speed[0]) * time_passed_s
            self.detectCollisions(collision_objects)
            self.y = self.y + float(self.speed[1]) * time_passed_s
            self.detectCollisions(collision_objects)
        else:
            self.y = self.y + float(self.speed[1]) * time_passed_s
            self.detectCollisions(collision_objects)
            self.x = self.x + float(self.speed[0]) * time_passed_s
            self.detectCollisions(collision_objects)

        self.movement = [self.pos[i] - self.last_pos[i] for i in range(len(self.pos))]

    def updateAnimationType(self):
        last_animation = self.animation_type

        if self.movement[0] > 0:
            self.animation_type = "walk_right"
        elif self.movement[0] < 0:
            self.animation_type = "walk_left"
        else:
            if 'left' in self.animation_type:
                self.animation_type = 'idle_left'
            else:
                self.animation_type = 'idle_right'

        if abs(self.speed[1]) > 0:
            if self.jump_timer < 1.25:
                if self.movement[0] > 0:
                    self.animation_type = "jump_right"
                elif self.movement[0] < 0:
                    self.animation_type = "jump_left"
                else:
                    if 'left' in self.animation_type:
                        self.animation_type = 'jump_left'
                    else:
                        self.animation_type = 'jump_right'
            else:
                if self.movement[0] > 0:
                    self.animation_type = "fly_right"
                elif self.movement[0] < 0:
                    self.animation_type = "fly_left"
                else:
                    if 'left' in self.animation_type:
                        self.animation_type = 'fly_left'
                    else:
                        self.animation_type = 'fly_right'
        # if 'fly' not in self.animation_type:
        #     self.jump_timer = 0
        if self.animation_type != last_animation:
            self.animation_timer = 0