from core import Core
from unicurses import *
from collections import *
import rlib
import time
import threading

ft = Core()
stdscr = initscr()
curs_set(False)
noecho()
keypad(stdscr, True)
start_color()
init_pair(1, COLOR_WHITE, COLOR_BLACK)
init_pair(2, COLOR_CYAN, COLOR_BLACK)
init_pair(3, COLOR_WHITE, COLOR_GREEN)
init_pair(5, COLOR_WHITE, COLOR_RED)
init_pair(4, COLOR_YELLOW, COLOR_BLACK)

def render_screen():
    for i in rlib.elements:
        i.render()
        basic_text.content = ft.format_value(ft.basic_currency) + ft.b_char
        quote_text.content = ft.format_value(ft.quote_currency) + ft.q_char
        mvaddstr(4, 0, getmaxyx(stdscr)[1]*'-')

buffer_price = ft.get_quote_price()        
def update_price():
    while (True):
        ''' ИНДУССКИЙ КОД! ''' 
        global buffer_price
        global price_text
        buf = ft.get_quote_price()
        income = ft.quote_currency*buf - ft.quote_currency*ft.last_quote_price
        price_color = 1
        if (buffer_price < buf): price_color = 3
        if (buffer_price > buf): price_color = 5
        buffer_price = buf
        price_text.content = str(buf)
        price_text.attr = color_pair(price_color) | A_BOLD
        if(ft.last_quote_price!=0):
            income_text.content = 'Income: ' + str(income).split('.')[0]
        if(ft.short_size!=0):
            short_income = ((ft.short_size / buf) - 3000) * 0.90
            income_text.content = 'Income: ' + str(short_income).split('.')[0]
        if(ft.last_quote_price==0 and ft.short_size==0):
            income_text.content = ''
        time.sleep(1)  


menu_switching = False
def set_pair_menu_enabled():
    global pair_menu
    global menu
    global menu_switching
    pair_menu.is_visible = True
    pair_menu.is_enabled = True
    menu.is_enabled = False
    menu_switching = True
def set_pair_menu_disabled():
    global pair_menu
    global menu
    global menu_switching
    pair_menu.is_visible = False
    pair_menu.is_enabled = False
    menu.is_enabled = True
    menu_switching = True
menu_items = OrderedDict()
menu_items['BUY'] = ft.buy
menu_items['SELL'] = ft.sell
menu_items['OPEN SHORT'] = ft.open_short
menu_items['CLOSE SHORT'] = ft.close_short
menu_items['SELECT PAIR'] = set_pair_menu_enabled
pair_menu_items = OrderedDict()
pair_menu_items['USDRUB'] = ft.select_usdrub
pair_menu_items['EURUSD'] = ft.select_eurusd
pair_menu_items['BACK'] = set_pair_menu_disabled
menu = rlib.Menu(menu_items, 5, 3)
pair_menu = rlib.Menu(pair_menu_items, 7, 17)
pair_menu.is_visible = False
pair_menu.is_enabled = False
basic_text = rlib.Text(ft.format_value(ft.basic_currency) + ft.b_char, color_pair(1) | A_BOLD, 0, 0)
quote_text = rlib.Text(ft.format_value(ft.quote_currency) + ft.q_char, color_pair(2), 1, 0)
price_text = rlib.Text(buffer_price, color_pair(1) | A_BOLD, 3, 0)
income_text = rlib.Text('', color_pair(4) | A_BOLD, 3, 17)

running = True
def handle_key():
    global menu
    global pair_menu
    global running
    global menu_switching
    while(running):
        key = getch()
        if(key == 27):
            running = False
            break
        if(chr(key) == 'ц'):
            menu.key_up()
            pair_menu.key_up()
        if(chr(key) == 'ы'):
            menu.key_down()
            pair_menu.key_down()
        if(key == 10):
            ''' Костыль! '''
            if(not menu_switching):
                pair_menu.key_enter()
            if(not menu_switching):
                menu.key_enter()
            if(menu_switching):
                menu_switching = False
            
t1 = threading.Thread(target=handle_key)
t1.start()
update_price_thread = threading.Thread(target=update_price)
update_price_thread.start()
#t1.join()

while(running):
    erase()
    render_screen()
    refresh()
    time.sleep(0.1)
endwin()

