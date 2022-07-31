#!/usr/bin/python3

"""
this module is a first step to a big greek learning app.
"""

import sqlite3
import sys
import tkinter as tk

import pygame as pg


# import time

def quit_game():
    """ quit the game and close the window"""
    pg.quit()
    sys.exit(0)


class Window:
    """the window class include all win configs"""

    def __init__(self):
        """start the main window a set the config function"""
        self.win_main = tk.Tk()

        self.set_configs()

    def set_configs(self):
        """set the main title, geometry and oder settings"""
        self.win_main.title("Learn Greek")
        self.win_main.geometry("500x500")
        self.win_main.config(bg="black")


class MainApp:
    """the main class of the app"""

    def __init__(self):
        """start the window and initialize the String-vars"""
        self.g_stat = 0
        self.l_dis, self.l_gre, self.l_ger = (None,) * 3

        self.but_del, self.but_new, self.but_nxt = (None,) * 3

        self.w_number = 0
        self.win = pg.display.set_mode((WIN_W, WIN_H))
        self.clock = pg.time.Clock()
        self.i_rect = pg.Rect(WIN_W + 25, WIN_H - 20, 90, 40)
        self.active = False

        self.w_ger, self.w_gre, self.w_descr = (None,) * 3

        WordDict.create_table(WordDict())
        self.data = WordDict.read_data(WordDict())
        self.ger_words = WordDict.read_ger_words(WordDict())
        self.g_w_list = []
        self.load_ger_words()
        self.main_loop()

    def load_ger_words(self):
        """make a list from all german words from the database"""
        for index, word in enumerate(self.ger_words):
            self.g_w_list.append(list(self.ger_words[index]))
            print(f"index {index}: ", word)

    def new_word(self):
        """get the new word and save to the String-vars"""
        self.w_ger = input("eingeben")
        self.w_gre.set(input("eingeben"))
        self.w_descr.set(input("eingeben"))
        self.save_new_word()

    def save_new_word(self):
        """Write the new word in the database"""
        WordDict.insert_data(WordDict(), self.w_ger.get(), self.w_gre.get(), self.w_descr.get())

    @staticmethod
    def change_word():
        """display all words in labels"""
        print("def change word finish")

    def next_word(self):
        self.w_number += 1
        if self.w_number >= len(self.data) - 1:
            self.w_number = 0
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
                    self.g_stat = 1

    def main_loop(self):
        """ this is the main loop"""
        while True:
            self.event_control()
            if self.g_stat == 0:
                self.start_loop()
            elif self.g_stat == 1:
                self.game_loop()
            elif self.g_stat == 2:
                self.end_loop()
            pg.display.update()
            self.clock.tick(FPS)

    def start_loop(self):
        print("Start_Loop")
        pass

    def end_loop(self):
        print("End_Loop")

        pass

    def game_loop(self):
        print("Game_Loop")
        pass


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


pg.init()

WIN_W, WIN_H = 500, 500
FPS = 10
if __name__ == "__main__":
    MainApp()
