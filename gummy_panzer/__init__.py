from __future__ import absolute_import

import logging
logging.basicConfig(level=logging.INFO)
LOG = logging.getLogger(__name__)

import pygame, random
from . import settings
from .sprites import player, hud, effects, util, enemies, buildings

def main(argv):
    pygame.init()
    LOG.info("Starting game")
    screen = pygame.display.set_mode((settings.SCREEN_WIDTH,
                                    settings.SCREEN_HEIGHT));
    pygame.display.set_caption('Roflmao test')
    clock = pygame.time.Clock()

    my_player = player.Player()
    TEST_BUILDING1 = buildings.Building(1)
    TEST_BUILDING0 = buildings.Building(0)
    
    TEST_ENEMY = enemies.AerialEnemy('enemy_sprite.png',(screen.get_width(),300))
    my_hud = hud.Hud(100, 0, 0, 0)

    building_sprites = [TEST_BUILDING1, TEST_BUILDING0]
    enemy_sprites = [TEST_ENEMY]
    while True:
        building_gen=random.randint(1, 50)
        building_lev=random.randint(0,1)
        if building_gen==2:
            new_building=buildings.Building(building_lev)
            building_sprites.append(new_building)
        clock.tick(settings.FRAMES_PER_SECOND)
        pygame.display.update()
        screen.fill((0, 0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                break
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    break
                elif event.key == pygame.K_SPACE:
                    my_hud.score -= 1
            my_player.handle_event(event)
        else:
            enemy_sprites.extend(my_player.update())
            building_sprites.extend(my_player.update())
            screen.blit(my_player.image, my_player.rect.topleft)
            my_hud.draw_hud(screen)
            my_hud.time = pygame.time.get_ticks()/1000    #test timer code
            for building in building_sprites:
                building.update()
                if hasattr(building, "draw_area"):
                    screen.blit(building.image, building.rect.topleft, building.draw_area)
                else:
                    screen.blit(building.image, building.rect.topleft)
            for enemy in enemy_sprites:
                enemy.update()
                if hasattr(enemy, "draw_area"):
                    screen.blit(enemy.image, enemy.rect.topleft, enemy.draw_area)
                else:
                    screen.blit(enemy.image, enemy.rect.topleft)
            continue
        pygame.quit()
        return

__all__ = ['main']
