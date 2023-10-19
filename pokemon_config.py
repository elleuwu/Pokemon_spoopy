
from re import S


class Config:
    def __init__(self):
        
        self.mapWidth = 1248
        self.mapHeight = 736
       
        self.groundLayer = 1
        self.wallLayer = 2
        self.grassLayer = 3
        self.trnrLayer = 3
        self.playerLayer = 4
        
        self.tileSize = 32
           
    def loadMap(self,mapPath):
        
        with open(mapPath, "r+") as mapToLoad:
            self.map = mapToLoad.read()
            self.mapList = []
            self.tempList = []
            for elem in self.map:
                if elem == ",":
                    self.mapList.append(self.tempList)
                    self.tempList = []
                elif elem == "\n":
                    pass
                else:
                    self.tempList.append(elem)

        mapToLoad.close()
        return self.mapList
                    
        