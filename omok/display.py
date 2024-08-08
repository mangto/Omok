import pygame, sys


plate = [ [0] * 15 ] * 15 # 15x15 plate

class display:
    def __init__(self,
                 resolution:tuple[int, int]=(720, 720),
                 ) -> None:
        
        '''
        ## Initiailize Display

        ### Parameters:
         - resoultion: tuple[int, int]: display resolution

        ### Returns:
         None
        '''

        self.resolution: tuple[int] = resolution
        self.display: pygame.Surface = pygame.display.set_mode(resolution, pygame.DOUBLEBUF)
        self.clock: pygame.Clock = pygame.time.Clock()

        pygame.display.set_caption("Delu Omok")

        pass
    
    def render(self) -> None:
        return
    
    def events(self) -> None:
        return
    
    def loop(self) -> None:
        return