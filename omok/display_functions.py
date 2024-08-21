import pygame, win32con, win32gui, os
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

