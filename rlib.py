from unicurses import *

class Menu:
    menu_items = {}
    menu_items_texts = {}
    y = 0
    x = 0
    active_item = 0
    def __init__(self, menu_items, y, x):
        self.menu_items = menu_items
        self.menu_items_texts = list(menu_items.keys())
        self.menu_items_texts.reverse()
        self.y = y
        self.x = x
        y_t = y
        for i in range(0,len(menu_items)):
            mvaddstr(y_t, x, self.menu_items_texts[i], A_BOLD)
            y_t += 1
        self.active_item = 0
        mvaddstr(y, x - 2, '->' + self.menu_items_texts[0], color_pair(2) | A_BOLD)

    def key_up(self):
        self.active_item = (self.active_item - 1) % len(self.menu_items)
        self.redraw_menu()

    def key_down(self):
        self.active_item = (self.active_item + 1) % len(self.menu_items)
        self.redraw_menu()

    def key_enter(self):
            index = self.menu_items_texts[self.active_item]
            self.menu_items[index]()

    def redraw_menu(self):
        y = self.y + self.active_item
        y0 = self.y + ((self.active_item - 1) % len(self.menu_items))
        x = self.x
        move(y0, 0)
        clrtoeol()
        mvaddstr(y0, x, self.menu_items_texts[self.active_item - 1], A_BOLD)
        mvaddstr(y, x - 2, '->' + self.menu_items_texts[self.active_item], color_pair(2) | A_BOLD)
