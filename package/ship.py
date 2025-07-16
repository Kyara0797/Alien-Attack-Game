import pygame, sys, os

class Ship:
    def __init__(self, game):
        self.game = game
        self.image = pygame.image.load(os.path.join('images','ship2.png'))
        self.rect=self.image.get_rect(center=(
            (game.WINDOW_WIDTH/2, game.WINDOW_HEIGHT/2)
        ))
        
    def update(self):
        self.rect.center = pygame.mouse.get_pos()
    
    def draw(self, surface):
        surface.blit(self.image, self.rect)
        