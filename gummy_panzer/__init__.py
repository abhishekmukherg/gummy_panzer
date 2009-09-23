from __future__ import absolute_import
import logging
logging.basicConfig(level=logging.INFO)
LOG = logging.getLogger(__name__)

import pygame, random
from gummy_panzer import settings, waves_generator
from gummy_panzer.sprites import player, hud, effects, weapons, explosion_effect
from gummy_panzer.sprites import util, enemies, buildings, pedestrian, wave
from gummy_panzer.sprites import enemy_info, boss


SUPER_HYPER_SEIZURE_MODE = False

TICKS_TILL_BOSS = 1


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
        
        self.waves = waves_generator.waves()

        self.enemies = pygame.sprite.Group()
        self.enemy_bullets = pygame.sprite.Group()

        self.hud = hud.Hud(self.player.sprite, self.screen)
        self.blasteffects = pygame.sprite.Group()
        self.pointeffects = pygame.sprite.Group()
        self.pedestrians = pygame.sprite.Group()
        self.__background1_image = util.load_image("background1.png")
        self.__background2_image = util.load_image("background2.png")
        self.__road_image = util.load_image("road.png")
        self.__hud_image = util.load_image("healthbar.png")
        self.background1_pos = 0
        self.background2_pos = 0
        self.road_pos = 0
        self.__ticks = 0
        self.boss = pygame.sprite.GroupSingle()

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
        self.__ticks += 1
        if self.__ticks > TICKS_TILL_BOSS:
            return False
        else:
            return True

    def boss_tick(self):
        LOG.debug("Boss Tick")
        self.clock.tick(settings.FRAMES_PER_SECOND)
        if not self.boss:
            self.waves = []
            LOG.info("Creating boss")
            self.boss.add(boss.Boss((600, 400)))
        pygame.display.update()
        for e in pygame.event.get():
            self._handle_event(e)
        self._update()
        self._draw()

    def _check_collisions(self):
        exploding_emps = pygame.sprite.Group(*filter(
            lambda x: isinstance(x, weapons.Emp), self.player_bullets))
        exploding_emps = pygame.sprite.Group(*filter(
            lambda x: x.exploding, exploding_emps))
        non_emps = pygame.sprite.Group(*filter(
            lambda x: not isinstance(x, weapons.Emp), self.player_bullets))
        # Player's Bullets
        for wave in self.waves:
            if wave.distance <= 0:
                # Non emp bullet collisions
                enemy_collisions = pygame.sprite.groupcollide(
                        wave, non_emps, False, True)
                for enemy, bullets in enemy_collisions.iteritems():
                    for bullet in bullets:
                        self.blasteffects.add(explosion_effect.ExplosionEffect(
                            (bullet.rect.left,bullet.rect.top),'small'))
                        assert not isinstance(bullet, weapons.Emp)
                        # Kill enemies if needed
                        if enemy.damage(bullet.damage_done):
                            if not enemy.dying():
                                enemy.dying()
                                self.hud.score += enemy.points
                                self.pointeffects.add(
                                        explosion_effect.PointEffect(
                                            (bullet.rect.left,bullet.rect.top),
                                        enemy.points,25))
                        self.blasteffects.add(explosion_effect.ExplosionEffect((bullet.rect.left,bullet.rect.top),'small'))
                        
                        if enemy.damage(bullet.damage_done):
                            if not enemy.dying():
                                enemy.dying()
                                self.hud.score += enemy.points
                                self.pointeffects.add(explosion_effect.PointEffect((bullet.rect.left,bullet.rect.top),enemy.points,25))
                            break
                enemy_collisions = pygame.sprite.groupcollide(
                        wave, exploding_emps, False, False)
                for enemy, bullets in enemy_collisions.iteritems():
                    for bullet in bullets:
                        assert isinstance(bullet, weapons.Emp)
                        rect = pygame.Rect(0, 0, 0, 0)
                        rect.topright = bullet.rect.center
                        rect.bottomleft = enemy.rect.center
                        loc = [0,0]
                        loc[0] = random.randint(enemy.rect.left,enemy.rect.right)
                        loc[1] = random.randint(enemy.rect.top,enemy.rect.bottom)

                        self.blasteffects.add(explosion_effect.ExplosionEffect(
                            loc,'small'))
                        loc[0] = random.randint(enemy.rect.left,enemy.rect.right)
                        loc[1] = random.randint(enemy.rect.top,enemy.rect.bottom)
                        self.blasteffects.add(explosion_effect.ExplosionEffect(
                            loc,'small'))
                        loc[0] = random.randint(enemy.rect.left,enemy.rect.right)
                        loc[1] = random.randint(enemy.rect.top,enemy.rect.bottom)

                        self.blasteffects.add(explosion_effect.ExplosionEffect(
                            loc,'small'))
                        if enemy.damage(bullet.damage_done):
                            enemy.dying()
                            self.hud.score += enemy.points
                            self.pointeffects.add(explosion_effect.PointEffect(
                                rect.center,enemy.points,25))
                            break

        player_collisions = pygame.sprite.groupcollide(
                self.player, self.enemy_bullets, False, True)
        for a_player, bullets in player_collisions.iteritems():
            for bullet  in bullets:
                self.blasteffects.add(explosion_effect.ExplosionEffect((bullet.rect.left,bullet.rect.top),'small'))
                if a_player.damage(bullet.damage_done):
                    self._handle_death()

        # Enemy x Player
        for wave in self.waves:
            if wave.distance <= 0:
                player_collisions = pygame.sprite.groupcollide(self.player,
                        wave, False, False)
                for player, enemies in player_collisions.iteritems():
                    for enemy in enemies:
                        if enemy.e_state != enemy_info.STATE_DYING:
                            if player.damage(10):
                                self._handle_death()
                            if enemy.damage(10):
                                enemy.dying()
                for enemy in wave:
                    if enemy.e_state == enemy_info.STATE_DYING:
                        self._enemy_hits_ground(enemy)

    def _enemy_hits_ground(self, enemy):
        if enemy.rect.y >= ((settings.SCREEN_HEIGHT * .92) - enemy.rect.height):
            self.blasteffects.add(explosion_effect.ExplosionEffect(
                                    enemy.rect.center,'large'))
            pygame.time.delay(25)
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
            t_bullets = wave.update()
            if t_bullets != tuple():
                map(self.enemy_bullets.add, t_bullets)

        for group in (self.pedestrians, self.player_bullets, self.enemy_bullets,
                self.buildings_front, self.buildings_back):
            group.update()
        if self.boss.sprite is not None:
            boss_dict = self.boss.sprite.update()
            self.enemies.add(*boss_dict["enemies"])
            self.enemy_bullets.add(*boss_dict["bullets"])
        # hud
        self.hud.time = pygame.time.get_ticks()/1000
        # Scroll background
        self.background1_pos -=0.5
        if self.background1_pos == -1200:
            self.background1_pos = 0
        self.background2_pos -=1
        if self.background2_pos == -1200:
            self.background2_pos = 0
        self.road_pos-=2
        if self.road_pos == -800:
            self.road_pos = 0

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
                        self.hud.score += 10
                        ploc = self.player.sprite.rect.midtop
                        ploc = (ploc[0],ploc[1]+10)
                        self.pointeffects.add(explosion_effect.PointEffect(ploc,10,15))
                    elif isinstance(person, pedestrian.Alien):
                        self.player.sprite.energy +=5
                    else:
                        self.player.sprite.health +=5
                    person.kill()
        for person in self.pedestrians:
            if person.beaming == 1:
                person.rect.x = self.player.sprite.rect.centerx - 18
        self.blasteffects.update()
        self.pointeffects.update()
        
    def _draw(self):
        self.__draw_background(self.background1_pos, self.background2_pos)
        # Back
        
        for group in (self.buildings_back,):
            self.__draw_spritegroup(group)
        # Middle
        road_rect = self.__road_image.get_rect()
        road_rect.x = self.road_pos
        road_rect.y = 480
        self.screen.blit(self.__road_image,road_rect.topleft)
        self.screen.blit(self.__road_image, road_rect.topright)
        for wave in self.waves:
            if wave.distance <= 0:
                self.__draw_spritegroup(wave)
            self.__draw_spritegroup(self.pedestrians)
        if self.player.sprite is not None:
            self.__draw_sprite(self.player.sprite._tractor_beam)	
        for group in (self.player,
                      self.player_bullets,
                      self.enemy_bullets,
                      self.boss):
            self.__draw_spritegroup(group)
        # Front
        self.__draw_spritegroup(self.blasteffects)
        self.__draw_spritegroup(self.pointeffects)
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
        if SUPER_HYPER_SEIZURE_MODE:
            pygame.draw.rect(self.screen,(random.randint(0,255),
                    random.randint(0,255),random.randint(0,255)), sprite.rect)

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
