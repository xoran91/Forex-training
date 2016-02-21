import ystockquote
import pymysql.cursors
import decimal
from unicurses import *

class FT:
    connection = pymysql.connect(host='db4free.net',
                                 user='xor4096',
                                 password='spass12-',
                                 db='forextr',
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)

    data = ''
    sql_request = "SELECT `lastPrice`,`accUsd`,`accRub`,`shortSize` FROM `data` WHERE 1"
    with connection.cursor() as cursor:
            cursor.execute(sql_request, ())
            data = cursor.fetchone()

    char = ','        
    basic_currency = float(data['accRub'])
    quote_currency = float(data['accUsd'])
    quote_price = float(ystockquote.get_price('USDRUB=X'))
    last_quote_price = float(data['lastPrice'])
    short = float(data['shortSize'])

    def get_quote_price(self):
        quote_price = float(ystockquote.get_price('USDRUB=X'))
        return quote_price

    def save_data(self):
        sql = "UPDATE `data` SET `accUsd`=%s,`accRub`=%s,`lastPrice`=%s,`shortSize`=%s WHERE 1;"
        with self.connection.cursor() as cursor:
            cursor.execute(sql, (self.quote_currency, self.basic_currency, self.last_quote_price, self.short))
        self.connection.commit()

    def format_value(self, value):
        temp = str(value).split('.')[0]
        result = temp[:len(temp) % 3]
        temp = temp[len(temp) % 3:]
        for i in range(1, len(temp) // 3 + 1):
            result += self.char + temp[(i-1)*3:i*3]
        return result.strip(self.char)
    
    def buy(self):
        self.quote_currency += self.basic_currency / self.get_quote_price()
        self.basic_currency = 0
        self.last_quote_price = self.get_quote_price()
        self.save_data()
        
    def sell(self):
        self.basic_currency += self.quote_currency * self.get_quote_price()
        self.quote_currency = 0
        self.last_quote_price = self.get_quote_price()
        self.save_data()