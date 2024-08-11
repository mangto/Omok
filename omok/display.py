import pygame, sys, win32con, win32gui, os
from pygame import gfxdraw
from pathlib import Path

path = Path(__file__).parent.absolute()

pygame.font.init()

LocalFonts = os.listdir( str(path) + "\\fonts" )
SystemFonts = os.listdir( "C:\\Windows\\Fonts" )


def find_fonts(name:str, FontList:list) -> str:
    assert type(name) == str, f"Invalid font name type, {type(name)}"
    assert type(FontList) in (tuple, list), f"Invalid font FontList type, {type(FontList)}"
    
    if ('.' in name): name = name[:name.rfind('.')]
    
    for font in FontList:
        if ('.' in font): rfont = font[:font.rfind('.')]
        else: rfont = font
        
        if (rfont.lower() == name.lower()): return font
        
        
    return ''

def Font(name:str, size:int,
         bold:bool=False, italic:bool=False,
         underline:bool=False, strikethrough:bool=False) -> pygame.Font:
    
    assert type(name) == str, f"Invalid font name type, {type(name)}"
    assert type(size) in (int, float), f"Invalid font size type, {type(size)}"
    assert type(bold) in (int, bool), f"Invalid font bold type, {type(bold)}"
    assert type(italic) in (int, bool), f"Invalid font italic type, {type(italic)}"
    assert type(underline) in (int, bool), f"Invalid font underline type, {type(underline)}"
    assert type(strikethrough) in (int, bool), f"Invalid font strikethrough type, {type(strikethrough)}"
    
    if ('.' in name): name = name[:name.rfind('.')]
    
    local = find_fonts(name, LocalFonts)
    if (local): font_path = str(path) + "\\fonts\\" + local
    else:
        system = find_fonts(name, SystemFonts)
        if (system): font_path = "C:\\Windows\\Fonts\\" + system
        else: font_path = "C:\\Windows\\Fonts\\Arial.ttf"
    
    font = pygame.Font(font_path, size)
    font.set_bold(bold)
    font.set_italic(italic)
    font.set_underline(underline)
    font.set_strikethrough(strikethrough)
    
    return font


def wndProc(oldWndProc, draw_callback, hWnd, message, wParam, lParam):
    if message == win32con.WM_SIZE:
        draw_callback()
        win32gui.RedrawWindow(hWnd, None, None, win32con.RDW_INVALIDATE | win32con.RDW_ERASE)
    return win32gui.CallWindowProc(oldWndProc, hWnd, message, wParam, lParam)

class draw:
    def rrect(surface, rect, color, radius=0.4):
        rect         = pygame.Rect(rect)
        color        = pygame.Color(*color)
        alpha        = color.a
        color.a      = 0
        pos          = rect.topleft
        rect.topleft = 0,0
        rectangle    = pygame.Surface(rect.size,pygame.SRCALPHA)
        circle       = pygame.Surface([min(rect.size)*3]*2,pygame.SRCALPHA)
        pygame.draw.ellipse(circle,(0,0,0),circle.get_rect(),0)
        circle       = pygame.transform.smoothscale(circle,[int(min(rect.size)*radius)]*2)
        radius              = rectangle.blit(circle,(0,0))
        radius.bottomright  = rect.bottomright
        rectangle.blit(circle,radius)
        radius.topright     = rect.topright
        rectangle.blit(circle,radius)
        radius.bottomleft   = rect.bottomleft
        rectangle.blit(circle,radius)

        rectangle.fill((0,0,0),rect.inflate(-radius.w,0))
        rectangle.fill((0,0,0),rect.inflate(0,-radius.h))

        rectangle.fill(color,special_flags=pygame.BLEND_RGBA_MAX)
        rectangle.fill((255,255,255,alpha),special_flags=pygame.BLEND_RGBA_MIN)
        return surface.blit(rectangle,pos)
    
    def text(text:str, font:pygame.Font, window:pygame.Surface, x:int, y:int, cenleft="center", color=(0,0,0)):
        text_obj = font.render(text, True, color)
        text_rect=text_obj.get_rect()
        if(cenleft == "center"):
            text_rect.centerx = x
            text_rect.centery = y
        elif(cenleft == "left"):
            text_rect.left=x
            text_rect.top=y
        elif(cenleft == "right"):
            text_rect.right=x
            text_rect.top=y
        elif(cenleft == "cenleft"):
            text_rect.left=x
            text_rect.centery=y
        elif(cenleft == "cenright"):
            text_rect.right=x
            text_rect.centery=y
        window.blit(text_obj, text_rect)
        
    def gettsize(text, font):
        return font.render(text,True,(0,0,0)).get_rect().size


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
        self.render_plate()

        self.pointing: tuple[int] = None
        self.turn = -1

        pass
    
    def calc_cord(self, cord:tuple[int]) -> list[int]:

        return list([50+cord[0]*50, 50+cord[1]*50])

    def render_plate(self) -> None:
        
        self.PlateSurf.fill((221, 191, 166)) # bg color

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
                if (status == 0): continue
                elif (status == 1): color = (255, 255, 255) # white
                else: color = (0, 0, 0) # black

                # draw.aacircle(self.PlateSurf, (128, 128, 128), self.calc_cord((x, y)), 25)
                draw.rrect(self.PlateSurf, [pos[0]-24, pos[1]-24, 48, 48], (128, 128, 128), .99)
                draw.rrect(self.PlateSurf, [pos[0]-23, pos[1]-23, 46, 46], color, 1.)
        return
    
    def render(self) -> None:
        self.window.fill((255, 255, 255))
        self.window.blit(self.PlateSurf, self.PlatePos)

        if (self.pointing):
            pos = self.calc_cord(self.pointing)
            gfxdraw.aacircle(self.window, self.PlatePos[0]+pos[0], self.PlatePos[1]+pos[1], 24, (0, 0, 0))


        pygame.display.update()

        return
    
    def event(self, events:list[pygame.Event]) -> None:

        for event in events:

            if (event.type == pygame.QUIT):
                pygame.quit()
                sys.exit()

            if (event.type == pygame.MOUSEBUTTONUP):
                if (event.button == 1 and self.pointing):
                    stone = self.plate[self.pointing[1]][self.pointing[0]]
                    if (stone == 0):
                        self.plate[self.pointing[1]][self.pointing[0]] = self.turn
                        self.render_plate()
                        self.turn *= -1

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