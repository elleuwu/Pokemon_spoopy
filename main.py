import pygame,sys
from config import *
from sprites import *

class mainGame:
    
    """Class to manage the game assets and behaviour"""

    def __init__(self):
        pygame.init()

        self.config = Config()
        self.sprites = SpriteSheet("img//character.png")
        
        self.all_sprite_group = pygame.sprite.Group()
        self.player_sprite_group = pygame.sprite.Group()
        self.env_sprite_group = pygame.sprite.Group()

        self.screen = pygame.display.set_mode((self.config.screen_width, self.config.screen_height),pygame.FULLSCREEN)
        pygame.display.set_caption("Pokemon Remake Early Alpha Test 01")

    def run_game(self):
        while True:
            self.events()
            self.updates()

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    sys.exit()

        self.spritesheet.image_at(0,0,32,32)


    def updates(self):
        pygame.display.flip()

if __name__ == "__main__":
    game = mainGame()
    game.run_game()