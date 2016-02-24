from unicurses import *
from collections import *
elements = []

class Text:
    content = ''
    y = 0
    x = 0
    attr = 0
    def __init__(self, content, atrr, y, x):
        global elements
        elements.append(self)
        self.y = y
        self.x = x
        self.content = content
        self.attr = atrr
        
    def render(self):
        mvaddstr(self.y, self.x, self.content, self.attr)
        
class Menu:
    menu_items = OrderedDict()
    menu_items_texts = []
    y = 0
    x = 0
    is_visible = True
    is_enabled = True
    active_item = 0
    def __init__(self, menu_items, y, x):
        global elements
        elements.append(self)
        self.menu_items = menu_items
        self.menu_items_texts = list(menu_items.keys())
        self.y = y
        self.x = x
        self.active_item = 0

    def key_up(self):
        if (self.is_enabled == False): return
        self.active_item = (self.active_item - 1) % len(self.menu_items)

    def key_down(self):
        if (self.is_enabled == False): return
        self.active_item = (self.active_item + 1) % len(self.menu_items)

    def key_enter(self):
        if (self.is_enabled == False): return
        index = self.menu_items_texts[self.active_item]
        self.menu_items[index]()

    def render(self):
        if (self.is_visible == False): return
        y_t = self.y
        for i in range(0,len(self.menu_items)):
            mvaddstr(y_t, self.x, self.menu_items_texts[i], A_BOLD)
            y_t += 1
        y = self.y + self.active_item
        x = self.x
        mvaddstr(y, x - 2, '->' + self.menu_items_texts[self.active_item], color_pair(2) | A_BOLD)
