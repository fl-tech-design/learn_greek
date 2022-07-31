#!/usr/bin/python3

"""
this module is a first step to a big greek learning app.
"""

import sqlite3
import sys

import pygame as pg

# import time

pg.init()


# import time
class Fon:
    """this class defines the game fonts"""
    fo100 = pg.font.SysFont("Arial", 100)
    fo40 = pg.font.SysFont("Arial", 40)
    fo23 = pg.font.SysFont("Arial", 23)
    fo16 = pg.font.SysFont("Arial", 16)


def quit_game():
    """ quit the game and close the window"""
    pg.quit()
    sys.exit(0)


class MainApp:
    """the main class of the app"""

    def __init__(self):
        """start the window and initialize the String-vars"""
        self.n_stat = 0
        self.g_stat = 0
        self.w_nr = 0

        WordDict.create_table(WordDict())
        self.data = WordDict.read_data(WordDict())

        self.win = pg.display.set_mode((WIN_W, WIN_H))
        self.clock = pg.time.Clock()
        self.i_rect = pg.Rect(WIN_W + 25, WIN_H - 20, 90, 40)
        self.active = False
        self.u_text = ""
        self.w_ger = self.data[self.w_nr][0]
        self.w_gre = self.data[self.w_nr][1]
        self.w_des = self.data[self.w_nr][2]

        self.ger_words = WordDict.read_ger_words(WordDict())
        self.ger_w_list = []
        self.load_ger_words()
        self.main_loop()

    def load_ger_words(self):
        """make a list from all german words from the database"""
        for index, word in enumerate(self.ger_words):
            self.ger_w_list.append(list(self.ger_words[index]))
            print(f"index {index}: ", word)

    def new_word(self):
        """get the new word and save to the String-vars"""

        self.save_new_word()

    def save_new_word(self):
        """Write the new word in the database"""
        WordDict.insert_data(WordDict(), self.w_ger, self.w_gre, self.w_des)

    @staticmethod
    def change_word():
        """display all words in labels"""
        print("def change word finish")

    def next_word(self):
        self.w_nr += 1
        if self.w_nr >= len(self.data) - 1:
            self.w_nr = 0
        self.change_word()

    def event_control(self):
        """ handle the key events."""
        for event in pg.event.get():
            if event.type == pg.MOUSEBUTTONDOWN:
                if self.i_rect.collidepoint(event.pos):
                    self.active = True
                else:
                    self.active = False
            if event.type == pg.QUIT:
                quit_game()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    quit_game()
                if event.key == pg.K_SPACE:
                    self.w_nr += 1


    def entry_name(self):
        """ make a textfield for the high-score name"""
        self.n_stat = 1
        while self.n_stat:
            for event in pg.event.get():
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_RETURN:
                        self.u_text = self.u_text[:]
                        self.n_stat = 0
                    else:
                        self.u_text += event.unicode
                        print("self.u_text: ", self.u_text)
                        print("taste gedrückt")
                        self.show_text(self.u_text, FG_P, 300, 400, Fon.fo23)
        self.g_stat = 0

    def show_text(self, text, col, p_x, p_y, fo_st):
        """ a small def to create a textfield"""
        act_text = fo_st.render(text, True, pg.Color(col))
        rect_text = act_text.get_rect()
        rect_text.x = p_x
        rect_text.y = p_y
        self.win.blit(act_text, rect_text)

    def standard_view(self):
        """ show the start window"""
        self.win.fill(BG_G)
        self.show_text(self.data[self.w_nr][0], FG_P, 100, 100, Fon.fo23)
        self.show_text(self.data[self.w_nr][1], FG_P, 200, 200, Fon.fo40)
        self.show_text(self.data[self.w_nr][2], FG_P, 300, 300, Fon.fo16)

    def main_loop(self):
        """ this is the main loop"""
        while True:
            self.event_control()
            if self.g_stat == 0:
                self.show_word_loop()
            elif self.g_stat == 1:
                self.new_word_loop()
            pg.display.update()
            self.clock.tick(FPS)

    def show_word_loop(self):
        print("self.ger_w_list: ", self.ger_w_list)
        self.standard_view()

    def new_word_loop(self):
        self.entry_name()


class WordDict:
    """ the sql class"""

    def __init__(self):
        """ define the vars of the class"""
        self.conn = None
        self.cursor = None

    def start_connection(self):
        """open a connection to the database"""
        self.conn = sqlite3.connect('dictionary.db')
        self.cursor = self.conn.cursor()

    def stop_connection(self):
        """close the opened connection from database"""
        self.conn.commit()
        self.conn.close()

    def create_table(self):
        """Check if a database is there. if not, it'll be created"""
        self.start_connection()
        sql_instruction = """
        CREATE TABLE IF NOT EXISTS DICT (
        W_GE VARCHAR(30),
        W_GR VARCHAR(30),
        W_DIS VARCHAR(30)
        );"""
        self.cursor.execute(sql_instruction)
        self.stop_connection()

    def insert_data(self, w_ge, w_gr, w_di):
        """Preparing SQL queries to INSERT a record into the database."""
        self.start_connection()
        self.cursor.execute("INSERT INTO DICT(W_GE, W_GR, W_DIS) VALUES(?, ?, ?)",
                            (w_ge, w_gr, w_di))
        print("Records inserted........")
        self.stop_connection()

    def read_data(self):
        """ read all data from the database and return a list of all data"""
        self.start_connection()
        self.cursor.execute('''SELECT * from DICT''')
        data_dict = self.cursor.fetchall()
        self.stop_connection()
        print("data reader: ", data_dict)
        return data_dict

    def read_ger_words(self):
        """read all german words from the dictionary"""
        self.start_connection()
        self.cursor.execute('''SELECT W_GE from DICT''')
        ger_words = self.cursor.fetchall()
        self.stop_connection()
        return ger_words

    def delete_data(self, t_xt):
        """a delete function, whose deleting the given word"""
        self.start_connection()
        self.cursor.execute("DELETE FROM DICT WHERE W_GE=?", (t_xt,))
        self.stop_connection()


FG_A, FG_P, BG_G = (0, 255, 0), (225, 225, 225), (100, 100, 100)

WIN_W, WIN_H = 1000, 800
FPS = 10
if __name__ == "__main__":
    MainApp()
