import pygame, sys, os
from package.ship import Ship
from package.laser_manager import LaserManager
from package.alien_manager import AlienManager

class Game:
    def __init__(self):
        pygame.init()
        self.WINDOW_WIDTH = 1280
        self.WINDOW_HEIGHT = 720

        self.display_surface = pygame.display.set_mode(
            (self.WINDOW_WIDTH, self.WINDOW_HEIGHT)
        )

        pygame.display.set_caption('Alien Attack')
        self.clock = pygame.time.Clock()
        self.dt = 0

        self.load_assets()

        self.ship = Ship(self)
        self.laser_manager = LaserManager(self)
        self.alien_manager = AlienManager(self)

        self.running = True

    def load_assets(self):
        self.bg_surf = pygame.image.load(os.path.join('images', 'background.png'))
        self.font = pygame.font.Font('./images/subatomic.ttf', 50)

        self.laser_sound = pygame.mixer.Sound(os.path.join('sounds', 'laser.ogg'))
        self.explosion_sound = pygame.mixer.Sound(
            os.path.join('sounds', 'explosion.wav')
        )

        self.background_music = pygame.mixer.Sound(
            os.path.join('sounds', 'music.wav')
        )

        self.background_music.play(loops=-1)

    def run(self):
        # This method will run the game
        # That is, it will open the window
        # The window should appear on your computer screen
        self.show_start_screen()

        while self.running:
            self.dt = self.clock.tick(120) / 1000
            self.handle_events()
            self.update()
            self.draw()

    def display_score(self):
        score_text = f'Score {pygame.time.get_ticks() // 1000}'

        text_surf = self.font.render(score_text, True, (255, 255, 255))

        text_rect = text_surf.get_rect(
            midbottom=(self.WINDOW_WIDTH / 2, self.WINDOW_HEIGHT - 80)
        )

        self.display_surface.blit(text_surf, text_rect)

        pygame.draw.rect(
            self.display_surface,
            (255, 255, 255),
            text_rect.inflate(30, 30),
            width=8,
            border_radius=5
        )

    def draw(self):
        self.display_surface.fill((0, 0, 0))

        self.display_surface.blit(self.bg_surf, (0, 0))

        # I would like to display the score
        self.display_score()

        self.laser_manager.draw(self.display_surface)
        self.alien_manager.draw(self.display_surface)
        self.ship.draw(self.display_surface)

        pygame.display.update()

    def update(self):
        self.ship.update()
        self.laser_manager.update()
        self.alien_manager.update()
        self.check_collision()

    def check_collision(self):
        for alien in self.alien_manager.alien_list:
            if self.ship.rect.colliderect(alien[0]):
                pygame.quit()
                sys.exit()

        for laser in self.laser_manager.laser_list[:]:
            for alien in self.alien_manager.alien_list[:]:
                if laser.colliderect(alien[0]):
                    self.alien_manager.alien_list.remove(alien)
                    self.laser_manager.laser_list.remove(laser)
                    self.explosion_sound.play()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            self.laser_manager.handle_event(event)
            self.alien_manager.handle_event(event)

    def show_start_screen(self):
        title_font = pygame.font.Font('./images/subatomic.ttf', 60)
        start_font = pygame.font.Font('./images/subatomic.ttf', 40)

        title_text = title_font.render('ALIEN ATTACK', True, (255, 255, 255))
        start_text = start_font.render('Right click or press SPACE to Start',
                                       True,
                                       (255, 255, 255)
                                       )

        title_rect = title_text.get_rect(
            midtop=(self.WINDOW_WIDTH / 2, self.WINDOW_HEIGHT / 4)
        )

        start_rect = start_text.get_rect(
            midbottom=(self.WINDOW_WIDTH / 2, self.WINDOW_HEIGHT * 3 / 4)
        )

        waiting = True

        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
                    waiting = False
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    waiting = False

            self.display_surface.fill((0, 0, 0))
            self.display_surface.blit(self.bg_surf, (0, 0))

            self.display_surface.blit(title_text, title_rect)
            self.display_surface.blit(start_text, start_rect)

            pygame.display.update()
            self.clock.tick(60)
