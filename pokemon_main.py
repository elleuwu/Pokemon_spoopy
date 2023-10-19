import pygame,os,sys
from pokemon_config import *
from pokemon_sprites import *

class mainGame:
    def __init__(self):
        
        pygame.init()
        self.config = Config()
    
        self.fontHollow = pygame.font.Font("Data//Fonts//Pokemon Hollow.ttf",50)
        self.fontSolid = pygame.font.Font("Data//Fonts//Pokemon Solid.ttf",50)
        self.fontSolid_2 = pygame.font.Font("Data//Fonts//Pokemon Solid.ttf",54)
        self.fontPixel = pygame.font.Font("Data//Fonts//pokemon_pixel_font.ttf",60)
        
        self.battleBackgroundSprites = spritesheet("Sprites//BattleBackgroundElements.png")
        self.fightElementSprites = spritesheet("Sprites//BattleElements.png")
        self.playerSprites = spritesheet("Sprites//DawnTrainer.png")
        self.impTrainerSprites = spritesheet("Sprites//GymLeadE4.png")
        self.heldItemSprites = spritesheet("Sprites//HeldItems.png")
        self.moveSymbolSprites = spritesheet("Sprites//MoveSymbols.png")
        self.overworldTrainerSprites = spritesheet("Sprites//OverworldTrainers.png")
        self.pokemonBackSprites = spritesheet("Sprites//PKMN-Back.png")
        self.pokemonFrontSprites1 = spritesheet("Sprites//PKMN-Front1.png")
        self.pokemonFrontSprites2 = spritesheet("Sprites//PKMN-Front2.png")
        self.pokemonCentreSprites = spritesheet("Sprites//PkmnCentre.png")
        self.envSprites = spritesheet("Sprites//PokemonTerrainSprites.png")
        self.TextBoxSprites = spritesheet("Sprites//TextBoxes.png")
        self.TextEntrySprites = spritesheet("Sprites//TextEntry.png")
        self.trainerBattleSprites = spritesheet("Sprites//TrainerFront.png")
        
        self.StartScreenImage = "StartScreenHOOH.gif"
        
        self.allSpritesGroup = pygame.sprite.LayeredUpdates()
        self.playerSpritesGroup = pygame.sprite.LayeredUpdates()
        self.envSpritesGroupCol1 = pygame.sprite.LayeredUpdates()
        self.envSpritesGroupCol0 = pygame.sprite.LayeredUpdates()
        self.overworldTrnrSpritesGroup = pygame.sprite.LayeredUpdates()
        self.grassSpritesGroup = pygame.sprite.LayeredUpdates()
        self.playerPkmnSpritesGroup = pygame.sprite.LayeredUpdates()
        self.battleSpritesGroup = pygame.sprite.LayeredUpdates()
        self.trnrBattleSpritesGroup = pygame.sprite.LayeredUpdates()
        self.trnrPkmnSpritesGroup = pygame.sprite.LayeredUpdates()
        self.overworldSpritesGroup = pygame.sprite.LayeredUpdates()
        
        os.environ['SDL_VIDEO_CENTERED'] = '1'
        self.mainScreen = pygame.display.set_mode((self.config.mapWidth,self.config.mapHeight),pygame.FULLSCREEN|pygame.SCALED,pygame.RESIZABLE)
        pygame.display.set_caption("Pokemon Hollow Nexus V1.0.1-Alpha")
        self.mainScreenRect = self.mainScreen.get_rect()
        
        self.pygameClock = pygame.time.Clock()
        self.gameFPS = 30

        self.zoomScale = 2.0
        self.internalSurfSize = (self.config.mapWidth,self.config.mapHeight)
        self.internalSurf = pygame.surface.Surface((self.config.mapWidth,self.config.mapHeight),pygame.SRCALPHA)
        self.internalSurfRect = self.internalSurf.get_rect(center = (self.config.mapWidth//2,self.config.mapHeight//2))
        self.internalSurfSizeVector = pygame.math.Vector2(self.internalSurfSize)
        self.internalOffsetVector = pygame.math.Vector2()
        
        self.mapOne = Config.loadMap(self,"Data//Maps//map1.txt")
        
    def runGame(self):
        self.drawLevel()
        while True:
            self.events()
            self.overworldUpdates()
            self.drawScreenOverworld()
        
    def events(self):
       for event in pygame.event.get():
           if event.type == pygame.QUIT:
               sys.exit()
           if event.type == pygame.KEYDOWN:
               if event.key == pygame.K_q:
                   sys.exit()
                   
    def overworldUpdates(self):
        self.overworldSpritesGroup.update()
                   
    def drawScreenOverworld(self):
        
        self.mainScreen.fill((0,0,0))
        self.internalSurf.fill((0,0,0))
        
        self.overworldSpritesGroup.draw(self.internalSurf)
        
        scaledSurf = pygame.transform.scale(self.internalSurf,self.internalSurfSizeVector * self.zoomScale)
        scaledRect = scaledSurf.get_rect(center = (self.config.mapWidth//2,self.config.mapHeight//2))

        self.mainScreen.blit(scaledSurf,scaledRect)

        pygame.display.update()
        self.pygameClock.tick(self.gameFPS)
        print(self.pygameClock)
        
    def drawLevel(self):
        for i,row in enumerate(self.mapOne):
            for j,column in enumerate(row):
                groundBlock(self,j,i)
                if column == "B":
                    wallBlock(self,j,i,True)
                if column == "G":
                    grassBlock(self,j,i)
                if column == "P":
                    self.playerObject = playerClass(self,j,i)
                if column == "T":
                    
    
if __name__ == "__main__":
    game = mainGame()

    game.runGame()