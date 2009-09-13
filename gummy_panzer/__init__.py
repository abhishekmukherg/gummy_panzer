from __future__ import absolute_import

import pygame
from .sprites import player

def main(argv):
    pygame.init()
    screen = pygame.display.set_mode((640, 480))
    pygame.display.set_caption('Roflmao test')
    clock = pygame.time.Clock()
    my_player = player.Player()
    while True:
        clock.tick(30)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                break
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    break
                elif event.key == pygame.K_d:
                    my_player.move_right()
                elif event.key == pygame.K_a:
                    my_player.move_left()
                elif event.key == pygame.K_w:
                    my_player.move_up()
                elif event.key == pygame.K_s:
                    my_player.move_down()
            elif event.type == pygame.KEYUP:
                if event.key in (pygame.K_a, pygame.K_d):
                    # check key pressed
                    my_player.stop_horizontal()
                elif event.key in (pygame.K_w, pygame.K_s):
                    my_player.stop_vertical()
        else:
            my_player.update()
            screen.blit(my_player.image, my_player.rect.topleft)
            continue
        pygame.quit()
        return

__all__ = ["main"]
