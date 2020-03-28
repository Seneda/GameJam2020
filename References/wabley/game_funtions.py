import sys

import pygame

def check_keydown_events(event, car):
    """Respond to keypresses."""
    if event.key == pygame.K_RIGHT:
        #rotate car clockwise
        car.rotating_clockwise = True
    elif event.key == pygame.K_LEFT:
        #rotate car anticlockwise
        car.rotating_anticlockwise = True
    elif event.key == pygame.K_UP:
        #move the car forward
        car.forward_motion = True

def check_keyup_events(event, car):
    if event.key == pygame.K_RIGHT:
        car.rotating_clockwise = False
    elif event.key == pygame.K_LEFT:
        car.rotating_anticlockwise = False
    elif event.key == pygame.K_UP:
        car.forward_motion = False

def check_events(car):
    """Respond to keypresses and mouse events"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, car)

        elif event.type == pygame.KEYUP:
            check_keyup_events(event, car)

def update_screen(fm_settings, screen, car,monkeys, pieces):
    """Update images on the screen and flip to the new screen."""
    #Redraw the screen during each pass through the loop.
    screen.fill(fm_settings.screen_bg_colour)
    for piece in pieces.sprites():
        piece.draw_piece()


    car.blitme()
    for monkey in monkeys:
        # monkey.update(car.rect.centerx,car.rect.centery)
        monkey.blitme()

    #Make the most recent screen visible.
    pygame.display.flip()