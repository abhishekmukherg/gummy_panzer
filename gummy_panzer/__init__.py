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
            my_player.handle_event(event)
        else:
            my_player.update()
            screen.blit(my_player.image, my_player.rect.topleft)
            continue
        pygame.quit()
        return

__all__ = ["main"]
