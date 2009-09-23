from __future__ import absolute_import
import logging
logging.basicConfig(level=logging.INFO)
LOG = logging.getLogger(__name__)

import pygame, random
from gummy_panzer import settings
from gummy_panzer.sprites import player, hud, effects, weapons, explosion_effect
from gummy_panzer.sprites import util, enemies, buildings, pedestrian, wave


class EndOfGameException(Exception):
    pass


class Game(object):

    def __init__(self):
        pygame.init()
        LOG.info("Starting Game")
        self.screen = pygame.display.set_mode((settings.SCREEN_WIDTH,
                                              settings.SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()

        self.player = pygame.sprite.GroupSingle(player.Player())
        self.player.sprite.rect.top = settings.SCREEN_HEIGHT * 2 / 5
        self.player.sprite.rect.left = settings.SCREEN_WIDTH * 1 / 5
        self.player_bullets = pygame.sprite.Group()

        self.buildings_front = pygame.sprite.LayeredUpdates()
        self.buildings_back = pygame.sprite.LayeredUpdates()
        
        self.waves = []

        wave_one = wave.Wave(200)
        wave_one.add(enemies.Enemy('enemy_sprite.png',
                     (150, 300)))
        wave_one.add(enemies.Enemy('fred.png',
                     (settings.SCREEN_WIDTH, 300)))
        wave_one.add(enemies.Enemy('bernard.png',
                     (settings.SCREEN_WIDTH, 485)))
        self.waves.append(wave_one)
        
        wave_two = wave.Wave(800)
        wave_two.add(enemies.Enemy('fred.png',
                     (settings.SCREEN_WIDTH, 100)))
        wave_two.add(enemies.Enemy('fred.png',
                     (settings.SCREEN_WIDTH, 300)))
        wave_two.add(enemies.Enemy('bernard.png',
                     (settings.SCREEN_WIDTH, 485)))
        self.waves.append(wave_two)
        
        wave_three = wave.Wave(1400)
        wave_three.add(enemies.Enemy('fred.png',
                     (settings.SCREEN_WIDTH, 100)))
        wave_three.add(enemies.Enemy('fred.png',
                     (settings.SCREEN_WIDTH, 300)))
        self.waves.append(wave_three)
        
        wave_four = wave.Wave(2000)
        wave_four.add(enemies.Enemy('fred.png',
                     (settings.SCREEN_WIDTH, 100)))
        wave_four.add(enemies.Enemy('fred.png',
                     (settings.SCREEN_WIDTH, 200)))
        wave_four.add(enemies.Enemy('fred.png',
                     (settings.SCREEN_WIDTH, 300)))
        wave_four.add(enemies.Enemy('fred.png',
                     (settings.SCREEN_WIDTH, 400)))
        self.waves.append(wave_four)
        
        wave_five = wave.Wave(2600)
        wave_five.add(enemies.Enemy('fred.png',
                     (settings.SCREEN_WIDTH, 100)))
        wave_five.add(enemies.Enemy('fred.png',
                     (settings.SCREEN_WIDTH, 200)))
        wave_five.add(enemies.Enemy('fred.png',
                     (settings.SCREEN_WIDTH, 300)))
        self.waves.append(wave_five)
        
        wave_six = wave.Wave(3200)
        wave_six.add(enemies.Enemy('fred.png',
                     (settings.SCREEN_WIDTH, 200)))
        wave_six.add(enemies.Enemy('fred.png',
                     (settings.SCREEN_WIDTH, 300)))
        wave_six.add(enemies.Enemy('fred.png',
                     (settings.SCREEN_WIDTH, 400)))
        self.waves.append(wave_six)
        
        wave_seven = wave.Wave(3800)
        wave_seven.add(enemies.Enemy('fred.png',
                     (settings.SCREEN_WIDTH, 100)))
        wave_seven.add(enemies.Enemy('fred.png',
                     (settings.SCREEN_WIDTH, 200)))
        wave_seven.add(enemies.Enemy('fred.png',
                     (settings.SCREEN_WIDTH, 300)))
        wave_seven.add(enemies.Enemy('bernard.png',
                     (settings.SCREEN_WIDTH, 485)))
        self.waves.append(wave_seven)
        

        self.enemy_bullets = pygame.sprite.Group()

        self.hud = hud.Hud(self.player.sprite, self.screen)
        self.blasteffects = pygame.sprite.Group()
        self.pedestrians = pygame.sprite.Group()
        self.__background1_image = util.load_image("background1.png")
        self.__background2_image = util.load_image("background2.png")
        self.__hud_image = util.load_image("healthbar.png")
        self.background1_pos = 0
        self.background2_pos = 0

    def _generate_random_elements(self):
        if random.random() < settings.FRONT_BUILDING_FREQ:
            LOG.debug("Generate Building - Generated front")
            self.buildings_front.add(buildings.Building(0))
        if random.random() < settings.BACK_BUILDING_FREQ:
            LOG.debug("Generate Building - Generated back")
            self.buildings_back.add(buildings.Building(1))
        if random.random() < settings.ALIEN_FREQ:
            random_height = random.randint(1, 40)
            new_pedestrian = pedestrian.Alien(random.randint(0, 1))
            new_pedestrian.rect.bottomleft = (settings.SCREEN_WIDTH,
                    int(settings.SCREEN_HEIGHT) - random_height)
            self.pedestrians.add(new_pedestrian)
        if random.random() < settings.HUMAN_FREQ:
            random_height = random.randint(1, 40)
            new_pedestrian = pedestrian.Human(random.randint(0, 1))
            new_pedestrian.rect.bottomleft = (settings.SCREEN_WIDTH,
                    int(settings.SCREEN_HEIGHT) - random_height)
            self.pedestrians.add(new_pedestrian)
        if random.randint(1, 600) <= 1:
            random_height = random.randint(1, 40)
            new_pedestrian = pedestrian.Health(2)
            new_pedestrian.rect.bottomleft = (settings.SCREEN_WIDTH,
                    int(settings.SCREEN_HEIGHT) - random_height)
            self.pedestrians.add(new_pedestrian)

    def tick(self):
        LOG.debug("Game Tick")
        self._generate_random_elements()
        self.clock.tick(settings.FRAMES_PER_SECOND)
        pygame.display.update()
        for event in pygame.event.get():
            self._handle_event(event)
        self._update()
        self._check_collisions()
        self._remove_offscreen_sprites()
        self._draw()

    def _check_collisions(self):
        # Player's Bullets
        for wave in self.waves:
            if wave.distance <= 0:
                enemy_collisions = pygame.sprite.groupcollide(
                        wave, self.player_bullets, False, True)
                for enemy, bullets in enemy_collisions.iteritems():
                    for bullet  in bullets:
                        self.blasteffects.add(explosion_effect.ExplosionEffect((bullet.rect.left,bullet.rect.top),'largea'))
                        if isinstance(bullet, weapons.Emp):
                            pass
                        elif enemy.damage(bullet.damage_done):
                            enemy.kill()
                            self.hud.score += enemy.points
                            break

        player_collisions = pygame.sprite.groupcollide(
                self.player, self.enemy_bullets, False, True)
        for a_player, bullets in player_collisions.iteritems():
            for bullet  in bullets:
                if a_player.damage(bullet.damage_done):
                    self._handle_death()

        # Enemy x Player
        for wave in self.waves:
            if wave.distance <= 0:
                player_collisions = pygame.sprite.groupcollide(self.player,
                        wave, False, False)
                for player, enemies in player_collisions.iteritems():
                    for enemy in enemies:
                        if player.damage(10):
                            self._handle_death()
                        if enemy.damage(10):
                            enemy.kill()

    def _remove_offscreen_sprites(self):
        # Kill left
        for wave in self.waves:
            if wave.distance <= 0:
                for group in (self.buildings_back,
                              self.buildings_front,
                              self.pedestrians,
                              self.enemy_bullets,
                              wave):
                    for sprite in group:
                        if sprite.rect.right < 0:
                            sprite.kill()
        # Kill Right
        for group in (self.player_bullets,
                      self.enemy_bullets):
            for sprite in group:
                if sprite.rect.left > settings.SCREEN_WIDTH + 100:
                    sprite.kill()

    def _update(self):
        # Player update
        bullets = self.player.sprite.update()
        map(self.player_bullets.add, bullets)
        emps = filter(lambda x: isinstance(x, weapons.Emp), self.player_bullets)
        for emp in emps:
            if emp.rect.x > settings.SCREEN_WIDTH * 0.65:
                emp.kill()

        # Enemies update
        for wave in self.waves:
            map(self.enemy_bullets.add, wave.update())

        for group in (self.pedestrians, self.player_bullets, self.enemy_bullets,
                self.buildings_front, self.buildings_back):
            group.update()
        # hud
        self.hud.time = pygame.time.get_ticks()/1000
        # Scroll background
        self.background1_pos -=0.5
        if self.background1_pos == -1200:
            self.background1_pos = 0
        self.background2_pos -=1
        if self.background2_pos == -1200:
            self.background2_pos = 0
        # Tractor Beam
        if self.player.sprite is not None:
            tractor_beam = self.player.sprite._tractor_beam
            # Find all pedestrians to be beamed up
            if tractor_beam.extended:
                for person in self.pedestrians:
                    if person.rect.x <= tractor_beam.rect.centerx \
                            and person.rect.x >= tractor_beam.rect.centerx - 40:
                        person.beam_me_up()
            # Consume any pedestrians that are being beamed
            for person in self.pedestrians:    
                if person.rect.y <= self.player.sprite.rect.centery and \
                        person.beaming == 1:
                    if isinstance(person, pedestrian.Human):
                        self.hud.score +=5
                    elif isinstance(person, pedestrian.Alien):
                        self.player.sprite.energy +=5
                    else:
                        self.player.sprite.health +=2
                    person.kill()
        for person in self.pedestrians:
            if person.beaming == 1:
                person.rect.x = self.player.sprite.rect.centerx - 18
        self.blasteffects.update()
    def _draw(self):
        self.__draw_background(self.background1_pos, self.background2_pos)
        # Back
        for group in (self.buildings_back,):
            self.__draw_spritegroup(group)
        # Middle

        for wave in self.waves:
            if wave.distance <= 0:
                self.__draw_spritegroup(wave)
            self.__draw_spritegroup(self.pedestrians)
        if self.player.sprite is not None:
            self.__draw_sprite(self.player.sprite._tractor_beam)	
        for group in (self.player,
                      self.player_bullets,
                      self.enemy_bullets):
            self.__draw_spritegroup(group)
        # Front
        self.__draw_spritegroup(self.blasteffects)
        for group in (self.buildings_front,):
            self.__draw_spritegroup(group)
        self.hud.draw_hud(self.screen)
        self.screen.blit(self.__hud_image, (0, 0))
        self.hud._draw_value("Score", self.hud.score, (700, 18), (255, 0, 0))
        self.hud._draw_value("Time", self.hud.time, (620, 18), (255, 0, 0))

    def __draw_background(self, background1_pos, background2_pos):
        back_rect1 = self.__background1_image.get_rect()
        back_rect1.x = background1_pos
        self.screen.blit(self.__background1_image, back_rect1.topleft)
        self.screen.blit(self.__background1_image, back_rect1.topright)
        back_rect2 = self.__background2_image.get_rect()
        back_rect2.x = background2_pos
        self.screen.blit(self.__background2_image, back_rect2.topleft)
        self.screen.blit(self.__background2_image, back_rect2.topright)

    def __draw_spritegroup(self, group):
        for sprite in group:
            #if isinstance(sprite, weapons.Emp):
            #    surf = pygame.Surface((sprite.rect.width, sprite.rect.height))
            #    surf.fill((120,120,120))
            #    self.screen.blit(surf, sprite.rect.topleft)
            self.__draw_sprite(sprite)

    def __draw_sprite(self, sprite):
        if hasattr(sprite, "draw_area"):
            self.screen.blit(sprite.image,
                    sprite.rect.topleft,
                    sprite.draw_area)
        else:
            self.screen.blit(sprite.image, sprite.rect.topleft)

    def _handle_event(self, event):
        if event.type == pygame.QUIT:
            raise EndOfGameException("Quit")
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                raise EndOfGameException("Quit")
            # Reduce player's score by one for each attempt at firing
            elif event.key == pygame.K_SPACE:
                self.hud.score -= 1
        assert self.player.sprite is not None
        self.player.sprite.handle_event(event)

    def _handle_death(self):
        pygame.display.set_caption("DEATH")
        death_image1 = util.load_image("death1.png")
        death_rect1 = death_image1.get_rect()
        self.screen.blit(death_image1,death_rect1)
        pygame.display.update()
        pygame.time.delay(1000)
        while 1:
            for event in pygame.event.get():
                self._handle_event(event)

__all__ = ['Game']
