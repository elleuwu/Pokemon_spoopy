import ctypes

class Config:
    def __init__(self):
        self.user32 = ctypes.windll.user32
        self.screen_width = self.user32.GetSystemMetrics(0)    
        self.screen_height = self.user32.GetSystemMetrics(1)

        self.map = ["BBBBBBBBBB",
                    "B........B",
                    "B........B",
                    "B........B",
                    "B........B"]

