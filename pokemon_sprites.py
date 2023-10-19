import pygame,random

class spritesheet:
    def __init__(self,sheetPath):
        
        self.sheetPath = pygame.image.load(sheetPath)
        
    def singleSprite(self,rect,colorkey):
        
        spriteRect = pygame.Rect(rect)
        spriteImgSurf = pygame.Surface(spriteRect.size)

        spriteImgSurf.blit(self.sheetPath,(0,0),spriteRect)
        spriteImgSurf.set_colorkey(colorkey)

        return spriteImgSurf

    def multiSprite(self,rects,colorkey):
        
        sprites = []
        for elem in rects:
            sprites.append(self.singleSprite((elem),(colorkey)))
        return sprites
    
class wallBlock(pygame.sprite.Sprite):
    def __init__(self,mainGame,rectX,rectY,colCheck):

        self.mainGame = mainGame
        self.config = mainGame.config
        self._layer = self.config.wallLayer
        self.isCollide = colCheck
        
        if self.isCollide == True:
            self.layeredGroup = self.mainGame.allSpritesGroup, self.mainGame.envSpritesGroupCol1, self.mainGame.overworldSpritesGroup
        if self.isCollide == False:
            self.layeredGroup = self.mainGame.allSpritesGroup, self.mainGame.envSpritesGroupCol0, self.mainGame.overworldSpritesGroup
            
        pygame.sprite.Sprite.__init__(self,self.layeredGroup)

        self.x = rectX * self.config.tileSize
        self.y = rectY * self.config.tileSize
        self.width = self.config.tileSize
        self.height = self.config.tileSize

        self.image = self.mainGame.envSprites.singleSprite((32,0,32,32),(0,0,0))
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        
class groundBlock(pygame.sprite.Sprite):
    def __init__(self,mainGame,rectX,rectY):

        self.mainGame = mainGame
        self.config = mainGame.config
        self._layer = self.config.groundLayer
        self.layeredGroup = self.mainGame.allSpritesGroup, self.mainGame.envSpritesGroupCol0, self.mainGame.overworldSpritesGroup
            
        pygame.sprite.Sprite.__init__(self,self.layeredGroup)

        self.x = rectX * self.config.tileSize
        self.y = rectY * self.config.tileSize
        self.width = self.config.tileSize
        self.height = self.config.tileSize

        self.image = self.mainGame.envSprites.singleSprite((64,0,32,32),(0,0,0))
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        
class grassBlock(pygame.sprite.Sprite):
    def __init__(self,mainGame,rectX,rectY):

        self.mainGame = mainGame
        self.config = mainGame.config
        self._layer = self.config.grassLayer
        self.layeredGroup = self.mainGame.allSpritesGroup, self.mainGame.grassSpritesGroup, self.mainGame.overworldSpritesGroup
            
        pygame.sprite.Sprite.__init__(self,self.layeredGroup)

        self.x = rectX * self.config.tileSize
        self.y = rectY * self.config.tileSize
        self.width = self.config.tileSize
        self.height = self.config.tileSize

        self.image = self.mainGame.envSprites.singleSprite((32,0,32,32),(0,0,0))
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        
class overworldTrnrClass(pygame.sprite.Sprite):
    def __init__(self,mainGame,rectX,rectY):

        self.mainGame = mainGame
        self.config = mainGame.config
        self._layer = self.config.trnrLayer
        self.layeredGroup = self.mainGame.allSpritesGroup, self.mainGame.overworldTrnrLayer, self.mainGame.overworldSpritesGroup
            
        pygame.sprite.Sprite.__init__(self,self.layeredGroup)

        self.x = rectX * self.config.tileSize
        self.y = rectY * self.config.tileSize
        self.width = self.config.tileSize
        self.height = self.config.tileSize

        self.image = self.mainGame.overworldTrainerSprites.singleSprite((random.ranrange(),32,32),(0,0,0))
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        
class playerClass(pygame.sprite.Sprite):
    def __init__(self,mainGame,rectX,rectY):
        
        self.mainGame = mainGame
        self.config = mainGame.config
        self._layer = self.config.playerLayer
        self.layeredGroup = self.mainGame.allSpritesGroup, self.mainGame.playerSpritesGroup, self.mainGame.overworldSpritesGroup
        
        pygame.sprite.Sprite.__init__(self,self.layeredGroup)
        
        self.imagesFront = self.mainGame.playerSprites.multiSprite([(172,2,32,32),(206,2,32,32),(274,2,32,32)],(136,184,176))
        self.imagesBack = self.mainGame.playerSprites.multiSprite([(172,36,32,32),(206,36,32,32),(274,36,32,32)],(136,184,176))
        self.imagesLeft = self.mainGame.playerSprites.multiSprite([(172,104,32,32),(206,104,32,32),(274,104,32,32)],(136,184,176))
        self.imagesRight = self.mainGame.playerSprites.multiSprite([(172,70,32,32),(206,70,32,32),(274,70,32,32)],(136,184,176))
        
        self.x = rectX * self.config.tileSize
        self.y = rectY * self.config.tileSize
        self.width = self.config.tileSize
        self.height = self.config.tileSize
        self.image = self.imagesFront[0]
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        self.speed = 4
        self.xChange = 0
        self.yChange = 0
        self.index = 0
        self.maxAnimFrames = 4
        self.currentAnimFrame = 0
        
    def update(self):
        
        self.playerMovement()
        
        self.rect.x += self.xChange
        self.playerCollideWall("x")
        self.playerCollideTrainer("x")
        self.rect.y += self.yChange
        self.playerCollideWall("y")
        self.playerCollideTrainer("y")
        
        self.xChange = 0
        self.yChange = 0
        
    def playerMovement(self):
        
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            for sprite in self.mainGame.overworldSpritesGroup:
                sprite.rect.x += self.speed
            self.xChange-=self.speed
            self.currentAnimFrame+=1
            if self.currentAnimFrame >= self.maxAnimFrames:
                self.currentAnimFrame = 0
                self.index = (self.index + 1) % len(self.imagesRight)
                self.image = self.imagesRight[self.index]
        elif keys[pygame.K_d]:
            for sprite in self.mainGame.overworldSpritesGroup:
                sprite.rect.x -= self.speed
            self.xChange+=self.speed
            self.currentAnimFrame+=1
            if self.currentAnimFrame >= self.maxAnimFrames:
                self.currentAnimFrame = 0
                self.index = (self.index + 1) % len(self.imagesLeft)
                self.image = self.imagesLeft[self.index]
        elif keys[pygame.K_w]:
            for sprite in self.mainGame.overworldSpritesGroup:
                sprite.rect.y += self.speed
            self.yChange-=self.speed
            self.currentAnimFrame+=1
            if self.currentAnimFrame >= self.maxAnimFrames:
                self.currentAnimFrame = 0
                self.index = (self.index + 1) % len(self.imagesBack)
                self.image = self.imagesBack[self.index]
        elif keys[pygame.K_s]:
            for sprite in self.mainGame.overworldSpritesGroup:
                sprite.rect.y -= self.speed
            self.yChange+=self.speed
            self.currentAnimFrame+=1
            if self.currentAnimFrame >= self.maxAnimFrames:
                self.currentAnimFrame = 0
                self.index = (self.index + 1) % len(self.imagesFront)
                self.image = self.imagesFront[self.index]
                
    def playerCollideWall(self,direction):
        hits = pygame.sprite.spritecollide(self,self.mainGame.envSpritesGroupCol1,False)
        if direction == "x":
            if hits:
                if self.xChange > 0:
                    self.rect.x = hits[0].rect.left - self.rect.width
                    for sprite in self.mainGame.overworldSpritesGroup:
                        sprite.rect.x += self.speed
                if self.xChange < 0:
                    self.rect.x = hits[0].rect.right
                    for sprite in self.mainGame.overworldSpritesGroup:
                        sprite.rect.x -= self.speed
        if direction == "y":
            if hits:
                if self.yChange > 0:
                    self.rect.y = hits[0].rect.top - self.rect.width
                    for sprite in self.mainGame.overworldSpritesGroup:
                        sprite.rect.y += self.speed
                if self.yChange < 0:
                    self.rect.y = hits[0].rect.bottom
                    for sprite in self.mainGame.overworldSpritesGroup:
                        sprite.rect.y -= self.speed
                        
    def playerCollideTrainer(self,direction):
        hits = pygame.sprite.spritecollide(self,self.mainGame.overworldTrnrSpritesGroup,False)
        if direction == "x":
            if hits:
                if self.xChange > 0:
                    self.rect.x = hits[0].rect.left - self.rect.width
                    for sprite in self.mainGame.overworldSpritesGroup:
                        sprite.rect.x += self.speed
                if self.xChange < 0:
                    self.rect.x = hits[0].rect.right
                    for sprite in self.mainGame.overworldSpritesGroup:
                        sprite.rect.x -= self.speed
        if direction == "y":
            if hits:
                if self.yChange > 0:
                    self.rect.y = hits[0].rect.top - self.rect.width
                    for sprite in self.mainGame.overworldSpritesGroup:
                        sprite.rect.y += self.speed
                if self.yChange < 0:
                    self.rect.y = hits[0].rect.bottom
                    for sprite in self.mainGame.overworldSpritesGroup:
                        sprite.rect.y -= self.speed