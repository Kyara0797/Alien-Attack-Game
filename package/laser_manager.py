import pygame, sys, os

class LaserManager:
    def __init__(self, game):
        self.game = game
        self.laser_surf = pygame.image.load(os.path.join('images', 'laser.png'))
        self.laser_list = []
        self.can_shoot = True
        self.shoot_time = None
        self.shot_delay = 500  # milliseconds

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and self.can_shoot:
            self.shoot()

    def shoot(self):
        laser_rect = self.laser_surf.get_rect(midbottom=self.game.ship.rect.midtop)
        self.laser_list.append(laser_rect)
        self.can_shoot = False
        self.shoot_time = pygame.time.get_ticks()
        self.game.laser_sound.play()

    def update(self):
        for rect in self.laser_list[:]:
            rect.y -= 300 * self.game.dt  # move laser upwards

            if rect.bottom < 0:  # remove if out of screen
                self.laser_list.remove(rect)

        self.update_timer()

    def update_timer(self):
        if not self.can_shoot:
            current_time = pygame.time.get_ticks()
            if current_time - self.shoot_time > self.shot_delay:
                self.can_shoot = True

    def draw(self, surface):
        for rect in self.laser_list:
            surface.blit(self.laser_surf, rect)
