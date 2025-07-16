import pygame, sys, os
from random import randint, uniform

class AlienManager:
    def __init__(self, game):
        self.game = game
        self.alien_surf = pygame.image.load(os.path.join('images', 'alien2.png'))
        self.alien_list = []
        self.alien_timer = pygame.event.custom_type()
        pygame.time.set_timer(self.alien_timer, 500)

    def handle_event(self, event):
        if event.type == self.alien_timer:
            self.spawn_alien()

    def spawn_alien(self):
        x_pos = randint(-100, self.game.WINDOW_WIDTH + 100)
        y_pos = randint(-100, -50)

        alien_rect = self.alien_surf.get_rect(center=(x_pos, y_pos))
        direction = pygame.math.Vector2(uniform(-0.5, 0.5), 1)
        self.alien_list.append((alien_rect, direction))

    def update(self):
        for alien_tuple in self.alien_list[:]:
            direction = alien_tuple[1]
            alien_rect = alien_tuple[0]

            alien_rect.center += direction * 300 * self.game.dt

            if alien_rect.top > self.game.WINDOW_HEIGHT:
                self.alien_list.remove(alien_tuple)

    def draw(self, surface):
        for alien_tuple in self.alien_list:
            surface.blit(self.alien_surf, alien_tuple[0])
