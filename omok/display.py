import pygame, sys
from pygame import gfxdraw
from omok.engine import Engine

from omok.display_functions import *

class Display:

    def __init__(self,
                 resolution:tuple[int, int]=(900, 900),
                 ) -> None:
        
        '''
        ## Initiailize Display

        ### Parameters:
         - resoultion: tuple[int, int]: display resolution

        ### Returns:
         None
        '''

        self.resolution: tuple[int] = resolution
        self.window: pygame.Surface = pygame.display.set_mode(resolution, pygame.DOUBLEBUF|pygame.RESIZABLE)
        self.clock: pygame.Clock = pygame.time.Clock()
        self.plate: list[list[int]] = [[0 for _ in range(15)] for _ in range(15)]
        self.run: bool = True
        self.FPS: int = 60

        pygame.display.set_caption("Delu Omok")

        self.PlateSurf: pygame.Surface = pygame.Surface((800, 800), pygame.SRCALPHA)
        self.PlatePos: tuple[int] = (self.resolution[0]-800)//2, (self.resolution[1]-800)//2

        self.pointing: tuple[int] = None
        self.turn = -1

        self.InvalidPos: list[tuple[int, int]] = []

        self.render_plate()
        pass
    
    def calc_cord(self, cord:tuple[int]) -> list[int]:

        return list([50+cord[0]*50, 50+cord[1]*50])

    def render_plate(self) -> None:
        
        self.PlateSurf.fill((221, 191, 166)) # bg color
        self.InvalidPos: list[tuple[int, int]] = []

        for i in range(15): # draw lines
            pygame.draw.line(self.PlateSurf, (0, 0, 0), self.calc_cord((i, 0)), self.calc_cord((i, 14)))
            pygame.draw.line(self.PlateSurf, (0, 0, 0), self.calc_cord((0, i)), self.calc_cord((14, i)))

        pygame.draw.circle(self.PlateSurf, (0, 0, 0), self.calc_cord((3, 3)), 3)
        pygame.draw.circle(self.PlateSurf, (0, 0, 0), self.calc_cord((3, 11)), 3)
        pygame.draw.circle(self.PlateSurf, (0, 0, 0), self.calc_cord((11, 3)), 3)
        pygame.draw.circle(self.PlateSurf, (0, 0, 0), self.calc_cord((11, 11)), 3)

        # render stones
        for y, line in enumerate(self.plate):
            for x, status in enumerate(line):
                # (x, y) -> status
                color: tuple[int]
                pos = self.calc_cord((x, y))
                if (status == 0):
                    validity = Engine.check_valid_place(self.plate, self.turn, (x, y))
                    if (not validity):
                        pygame.draw.circle(self.PlateSurf, (255, 0, 0), pos, 10)
                        self.InvalidPos.append((x, y))
                    continue

                elif (status == 1): color = (255, 255, 255) # white
                else: color = (0, 0, 0) # black

                # draw.aacircle(self.PlateSurf, (128, 128, 128), self.calc_cord((x, y)), 25)
                draw.rrect(self.PlateSurf, [pos[0]-24, pos[1]-24, 48, 48], (128, 128, 128), .99)
                draw.rrect(self.PlateSurf, [pos[0]-23, pos[1]-23, 46, 46], color, .99)
        return
    
    def render(self) -> None:
        self.window.fill((255, 255, 255))
        self.window.blit(self.PlateSurf, self.PlatePos)

        if (self.pointing):
            pos = self.calc_cord(self.pointing)
            gfxdraw.aacircle(self.window, self.PlatePos[0]+pos[0], self.PlatePos[1]+pos[1], 24, (0, 0, 0))


        pygame.display.update()

        return
    
    def reset(self) -> None:
        self.plate: list[list[int]] = [[0 for _ in range(15)] for _ in range(15)]
        self.render_plate()
        self.turn = -1
    
    def event(self, events:list[pygame.Event]) -> None:

        for event in events:

            if (event.type == pygame.QUIT):
                pygame.quit()
                sys.exit()

            if (event.type == pygame.MOUSEBUTTONUP):
                if (event.button == 1 and self.pointing):
                    stone = self.plate[self.pointing[1]][self.pointing[0]]
                    if (stone == 0 and tuple(self.pointing) not in self.InvalidPos):
                        self.plate[self.pointing[1]][self.pointing[0]] = self.turn

                        win = Engine.check_win(self.plate, self.pointing)

                        if (win): print(f"{Engine.COLOR_MAP[self.turn]} Win!")

                        self.turn *= -1
                        self.render_plate()

                        

            if (event.type == pygame.KEYUP):
                if (event.key == pygame.K_F5):
                    self.reset()

        return
    
    def update(self) -> None:
        
        events = pygame.event.get()
        self.resolution = pygame.display.get_window_size()
        self.PlatePos = (self.resolution[0]-800)//2, (self.resolution[1]-800)//2

        mouse = pygame.mouse.get_pos()
        px, py = mouse[0]-self.PlatePos[0]-25, mouse[1]-self.PlatePos[1]-25
        px //= 50
        py //= 50

        if (px < 0 or px > 14 or py < 0 or py > 14):
            self.pointing = None
        else:
            self.pointing = (px, py)

        self.render()
        self.event(events)
        self.clock.tick(self.FPS)

        return
    
    def loop(self) -> None:

        hwnd = pygame.display.get_wm_info()['window']
        oldWndProc = win32gui.SetWindowLong(hwnd, win32con.GWL_WNDPROC, lambda *args: wndProc(oldWndProc, self.update, *args))

        while (self.run):

            self.update()

            continue

        pygame.quit()
        sys.exit()

        return
    
if __name__ == '__main__':
    display = Display()
    display.loop()