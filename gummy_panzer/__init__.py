from __future__ import absolute_import

import pygame
from . import settings
from .sprites import player

def main(argv):
    pygame.init()
    screen = pygame.display.set_mode((settings.SCREEN_WIDTH,
                                    settings.SCREEN_HEIGHT))
    pygame.display.set_caption('Roflmao test')
    clock = pygame.time.Clock()
    my_player = player.Player()
    extra_sprites = []
    while True:
        clock.tick(settings.FRAMES_PER_SECOND)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                break
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    break
            my_player.handle_event(event)
        else:
            extra_sprites.extend(my_player.update())
            screen.blit(my_player.image, my_player.rect.topleft)
            for sprite in extra_sprites:
                sprite.update()
                screen.blit(sprite.image, sprite.rect.topleft)
            continue
        pygame.quit()
        return

__all__ = ['main', 'sprites']
