import pygame
import math

class Monkey():
    total_latched = 0
    
    def __init__(self, screen,color):
        """Initialise the monkey and set its starting position"""
        self.screen = screen

        #Load image and get its rect.
        self.image = pygame.image.load('images/monkey_' +color +'.png')
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()

        #Set monkey off screen (top left)
        self.centerxfloat = -50
        self.centeryfloat = -50
        self.rect.centerx = -50
        self.rect.centery = -50

        #Set monkey speed and angle (from vertical that it's travelling), pixels per ms for speed
        self.speed = 0.1
        self.max_flying_speed = 0.2
        self.flying_speed = 0.0
        self.flying_deceleration = 0.001 
        self.flying_angle = 0

        # If monkey is on the car
        self.monkey_latched = False
        # If monkey has been flung off car
        self.monkey_flying = False
        self.monkey_latched_xoffset = 50.0
        self.monkey_latched_yoffset = 50.0



    def update(self,car,time_passed_ms):
        if (self.monkey_latched):
            self.centerxfloat = car.rect.centerx +math.cos(math.radians(car.angle))*self.monkey_latched_xoffset\
                +math.sin(math.radians(car.angle))*self.monkey_latched_yoffset
            self.centeryfloat = car.rect.centery +math.cos(math.radians(car.angle))*self.monkey_latched_yoffset\
                -math.sin(math.radians(car.angle))*self.monkey_latched_xoffset
            if ((self.monkey_latched_xoffset >= 0)and(car.rotating_anticlockwise)):
                self.monkey_latched = False
                Monkey.total_latched -= 1
                self.monkey_flying = True
                self.flying_angle = car.angle+270
                self.flying_speed = self.max_flying_speed
            elif ((self.monkey_latched_xoffset < 0)and(car.rotating_clockwise)):
                self.monkey_latched = False
                Monkey.total_latched -= 1
                self.monkey_flying = True
                self.flying_angle = car.angle+90
                self.flying_speed = self.max_flying_speed
        elif (self.monkey_flying):
            self.centerxfloat += ((math.sin(math.radians(self.flying_angle))*self.flying_speed*time_passed_ms)*-1)
            self.centeryfloat += ((math.cos(math.radians(self.flying_angle))*self.flying_speed*time_passed_ms)*-1)
            self.flying_speed -= self.flying_deceleration
            if (self.flying_speed <= 0):
                self.monkey_flying = False

        else:
            x_diff = car.rect.centerx - self.rect.centerx
            y_diff = car.rect.centery - self.rect.centery

            if (((x_diff*math.cos(math.radians(car.angle))) < car.width/2)and((x_diff*math.sin(math.radians(car.angle))) < car.height/2)\
                and((x_diff*math.cos(math.radians(car.angle))) > -car.width/2)and((x_diff*math.sin(math.radians(car.angle))) > -car.height/2)\
                and((y_diff*math.sin(math.radians(car.angle))) < car.width/2)and((y_diff*math.cos(math.radians(car.angle))) < car.height/2)\
                and((y_diff*math.sin(math.radians(car.angle))) > -car.width/2)and((y_diff*math.cos(math.radians(car.angle))) > -car.height/2)):
                self.monkey_latched = True
                Monkey.total_latched += 1
                self.monkey_latched_xoffset = -(math.cos(math.radians(car.angle))*x_diff)+(math.sin(math.radians(car.angle))*y_diff)
                self.monkey_latched_yoffset = -(math.cos(math.radians(car.angle))*y_diff)-(math.sin(math.radians(car.angle))*x_diff)
            # Angle is clockwise from vertical
            car_monkey_angle = None
            # Monkey right of car (angle between pi and 3(pi)/4), sin -ve, cos -ve
            if (x_diff <= 0):
                # Above
                if (y_diff > 0):
                    car_monkey_angle = math.pi-math.atan(x_diff/y_diff)
                # Below
                elif (y_diff < 0):
                    car_monkey_angle = -(math.atan(x_diff/y_diff))
                #  y == 0
                else:
                    car_monkey_angle = (3*math.pi)/4
            # Monkey left
            elif (x_diff > 0):
                # Above
                if (y_diff > 0):
                    car_monkey_angle = math.pi-math.atan(x_diff/y_diff)
                # Below
                elif (y_diff < 0):
                    car_monkey_angle = -(math.atan(x_diff/y_diff))
                # y == 0 
                else:
                    car_monkey_angle = 0
            else:
                car_monkey_angle = None

            if not (car_monkey_angle == None):
                self.centerxfloat -= ((math.sin(car_monkey_angle)*self.speed*time_passed_ms)*-1)
                self.centeryfloat += ((math.cos(car_monkey_angle)*self.speed*time_passed_ms)*-1)

        self.rect.centerx = round(self.centerxfloat,3)
        self.rect.centery = round(self.centeryfloat,3)



    def blitme(self):
        """Draw the monkey at its current location."""
        self.screen.blit(self.image, self.rect)

    def set_position(self,monkey_num,num_monkeys,monkey_radius):
        x_from_center = math.sin(math.radians(monkey_num*(360/num_monkeys)))*monkey_radius
        y_from_center = math.cos(math.radians(monkey_num*(360/num_monkeys)))*monkey_radius
        self.rect.centerx = self.screen_rect.centerx +x_from_center
        self.centerxfloat = self.rect.centerx
        self.rect.centery = self.screen_rect.centery +y_from_center
        self.centeryfloat = self.rect.centery
