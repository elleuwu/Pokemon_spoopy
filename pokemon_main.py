import pygame,sys
from pokemon_config import *
from pokemon_sprites import *

class mainGame:
    
    """Class to manage the game assets and behaviour"""

    def __init__(self):
        pygame.init()

        self.config = Config()
        self.player_sprites = SpriteSheet("sprites//character.png")
        self.env_sprites = SpriteSheet("sprites//terrain.png")
        
        self.all_sprite_group = pygame.sprite.Group()
        self.player_sprite_group = pygame.sprite.Group()
        self.env_sprite_group = pygame.sprite.Group()

        self.screen = pygame.display.set_mode((self.config.screen_width, self.config.screen_height))
        pygame.display.set_caption("Pokemon Remake Early Alpha Test 01")

        self.background = background_env(self,self.config)
        self.background.add(self.all_sprite_group,self.env_sprite_group)

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

        self.background.blit_env()



    def updates(self):
        pygame.display.flip()

if __name__ == "__main__":
    game = mainGame()
    game.run_game()