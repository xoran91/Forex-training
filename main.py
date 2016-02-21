from ftcore import FT
from unicurses import *
import rlib
import time
import threading

ft = FT()
stdscr = initscr()
curs_set(False)
noecho()
keypad(stdscr, True)
start_color()
init_pair(1, COLOR_WHITE, COLOR_BLACK)
init_pair(2, COLOR_CYAN, COLOR_BLACK)
init_pair(3, COLOR_WHITE, 9)
init_pair(4, COLOR_YELLOW, COLOR_BLACK)
def render():
    move(0, 0)
    clrtoeol()
    mvaddstr(0, 0, ft.format_value(ft.basic_currency) + ' R', color_pair(1) | A_BOLD)
    move(1, 0)
    clrtoeol()
    mvaddstr(1, 0, ft.format_value(ft.quote_currency) + ' $', color_pair(2))
    mvaddstr(4, 0, getmaxyx(stdscr)[1]*'-')
def render_income():
    buf = ft.get_quote_price()
    income = ft.quote_currency*buf - ft.quote_currency*ft.last_quote_price
    move(3, 0)
    clrtoeol()
    mvaddstr(3, 0, 'USD/RUB  ' + str(buf), color_pair(3) | A_BOLD)
    mvaddstr(3, 17, 'Income: ' + str(income).split('.')[0], color_pair(4) | A_BOLD)

menu_items = {'Buy': ft.buy, 'Sell': ft.sell}
menu = rlib.Menu(menu_items, 5, 3)

running = True
# Обрабатываем в два потока рендеринг и обработку нажатия клавиш
def handle_key():
    global menu
    global running
    while(running):
        key = getch()
        if(key == 27):
            running = False
            break
        if(chr(key) == 'ц'):
            menu.key_up()
        if(chr(key) == 'ы'):
            menu.key_down()
        if(key == 10):
            menu.key_enter()
            
t1 = threading.Thread(target=handle_key)
t1.start()
#t1.join()

while(running):
    render()
    render_income()
    refresh()
    time.sleep(0.01)
endwin()

