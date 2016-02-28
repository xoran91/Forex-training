import ystockquote
import pymysql.cursors
import decimal
import time
import threading
from unicurses import *

class Core:

    connection = pymysql.connect(host='db4free.net',
                                 user='xor4096',
                                 password='spass12-',
                                 db='forextr',
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)



    ''' CLASS FIELDS '''

    data = ''
    sql_request = "SELECT `USDRUB_LASTPRICE`,`USD`,`RUB`,`shortSize` FROM `data` WHERE 1"
    with connection.cursor() as cursor:
            cursor.execute(sql_request, ())
            data = cursor.fetchone()

    b_char = ' R'
    q_char = ' $'
    pair = 'USDRUB=X'

    quote_currency = float(data['USD'])
    basic_currency = float(data['RUB'])
    quote_price = float(ystockquote.get_price('USDRUB=X'))
    last_quote_price = float(data['USDRUB_LASTPRICE'])
    short_size = float(data['shortSize'])


    ''' INPUT / OUTPUT '''

    def get_quote_price(self):
        quote_price = float(ystockquote.get_price(self.pair))
        return quote_price

    def get_data(self):
        data = ''
        sql_request = "SELECT `{0}`, `{1}`, `{2}`, `shortSize` FROM `data` WHERE 1".format(self.pair[:6]+'_LASTPRICE', self.pair[:3], self.pair[3:6])
        with self.connection.cursor() as cursor:
                cursor.execute(sql_request, ())
                data = cursor.fetchone()
        self.quote_currency = float(data[self.pair[:3]])
        self.basic_currency = float(data[self.pair[3:6]])
        self.last_quote_price = float(data[self.pair[:6]+'_LASTPRICE'])
            
    def save_data(self):
        sql = "UPDATE `data` SET `{0}`=%s,`{1}`=%s,`{2}`=%s, `shortSize`=%s WHERE 1;".format(self.pair[:3], self.pair[3:6], self.pair[:6]+'_LASTPRICE')
        with self.connection.cursor() as cursor:
            cursor.execute(sql, (self.quote_currency, self.basic_currency, self.last_quote_price, self.short_size))
        self.connection.commit()
    

    ''' CURRENCY OPERATIONS (LOGIC) '''

    def buy(self):
        self.get_data()
        self.quote_currency += self.basic_currency / self.get_quote_price()
        self.basic_currency = 0
        self.last_quote_price = self.get_quote_price()
        self.save_data()
        
    def sell(self):
        self.get_data()        
        self.basic_currency += self.quote_currency * self.get_quote_price()
        self.quote_currency = 0
        self.last_quote_price = 0
        self.save_data()

    def open_short(self):
        self.get_data()
        _price = self.get_quote_price()
        self.short_size = 3000 * _price
        self.save_data()

    def close_short(self):
        self.get_data()
        _price = self.get_quote_price()
        _income = ((self.short_size / _price) - 3000) * 0.90
        self.short_size = 0
        self.quote_currency += _income
        self.save_data()

    def select_usdrub(self):
        self.save_data
        self.pair = 'USDRUB=X'
        self.b_char = ' R'
        self.q_char = ' $'
        self.get_data()

    def select_eurusd(self):
        self.save_data
        self.pair = 'EURUSD=X'
        self.b_char = ' $'
        self.q_char = ' E'
        self.get_data()


    ''' SECONDARY FUNCTIONS '''
    
    ''' Casts a string to the form ххх,ххх,ххх '''
    def format_value(self, value):
        temp = str(value).split('.')[0]
        result = temp[:len(temp) % 3]
        temp = temp[len(temp) % 3:]
        for i in range(1, len(temp) // 3 + 1):
            result += ',' + temp[(i-1)*3:i*3]
        return result.strip(',')    
