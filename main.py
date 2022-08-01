#!/usr/bin/python3
# pylint: disable=no-member
"""
this module is a first step to a big greek learning app.
"""

import sqlite3
import sys
import time

import pygame as pg

# import time

pg.init()
pg.mixer.init()


# import time
class AppCon:
    """this class defines the game fonts"""
    fo100 = pg.font.SysFont("Arial", 100)
    fo40 = pg.font.SysFont("Arial", 40)
    fo23 = pg.font.SysFont("Arial", 23)
    fo16 = pg.font.SysFont("Arial", 16)
    FG_A, FG_P, BG_G = (200, 200, 200), (225, 225, 225), (25, 25, 25)
    RED, GREEN = (255, 0, 0), (0, 255, 0)
    WIN_W, WIN_H = 700, 650
    FPS = 10


def quit_game():
    """ quit the game and close the window"""
    pg.quit()
    sys.exit(0)


class MainApp:
    """the main class of the app"""

    def __init__(self):
        """start the window and initialize the String-vars"""
        self.new_w_state = 0
        self.app_stat = 0
        self.w_nr, self.w_nr_old = 0, 0
        WordDict.create_table(WordDict())
        self.data = WordDict.read_data(WordDict())

        self.win = pg.display.set_mode((AppCon.WIN_W, AppCon.WIN_H))

        self.clock = pg.time.Clock()
        self.i_rect = pg.Rect(AppCon.WIN_W + 25, AppCon.WIN_H - 20, 90, 40)
        self.active = False
        self.n_w_ger, self.n_w_gre, self.n_w_des, self.n_w_pho, self.n_w_exa = "", "", "", "", ""

        self.ger_w_list = []
        self.load_ger_words()
        self.main_loop()

    def load_ger_words(self):
        """make a list from all german words from the database"""
        ger_words = WordDict.read_ger_words(WordDict())
        length = len(ger_words)
        for index in range(length):
            self.ger_w_list.append(list(ger_words[index]))
        print(length)

    def new_word(self):
        """get the new word and save to the String-vars"""
        self.n_w_ger = input("Deutsches Wort eingeben")
        self.n_w_gre = input("Griechisches Wort eingeben")
        self.n_w_des = input("Beschreibung eingeben")
        self.n_w_pho = input("phonetik eingeben")
        self.n_w_exa = input("example eingeben")
        WordDict.insert_data(WordDict(), self.n_w_ger, self.n_w_gre, self.n_w_des, self.n_w_pho, self.n_w_exa)
        self.data = WordDict.read_data(WordDict())

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
                if event.key == pg.K_RIGHT:
                    if self.w_nr >= len(self.ger_w_list) - 1:
                        self.w_nr = len(self.ger_w_list) - 1
                    else:
                        self.w_nr += 1
                    self.play_audio_word(str(self.ger_w_list[self.w_nr]))

                if event.key == pg.K_LEFT:
                    if self.w_nr <= 0:
                        self.w_nr = 0
                    else:
                        self.w_nr -= 1
                    self.play_audio_word(str(self.ger_w_list[self.w_nr]))
                if event.key == pg.K_n:
                    self.new_word()
                if event.key == pg.K_d:
                    WordDict.delete_data(WordDict(), input("Wort zum löschen eingeben"))
                if event.key == pg.K_a:
                    self.play_audio_word(str(self.ger_w_list[self.w_nr]))

    def en_w_ger(self):
        """ make a textfield for the high-score name"""
        self.new_w_state = 1
        while self.new_w_state:
            for event in pg.event.get():
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_RETURN:
                        self.n_w_ger = self.n_w_ger[:]
                        ShowWords.show_ger_word(self.win, self.n_w_ger)
                        self.new_w_state = 0
                        time.sleep(2)
                        self.app_stat = 0
                    else:
                        self.n_w_ger += event.unicode
                        print("self.u_text: ", self.n_w_ger)
                        ShowWords.show_ger_word(self.win, self.n_w_ger)
                        pg.display.flip()

    def main_loop(self):
        """ this is the main loop"""
        self.play_audio_word(str(self.ger_w_list[self.w_nr]))

        while True:
            self.win.fill(AppCon.BG_G)
            self.event_control()
            if self.app_stat == 0:
                self.show_word_loop()
            elif self.app_stat == 1:
                self.new_word_loop()
            pg.display.update()
            self.clock.tick(AppCon.FPS)

    def show_word_loop(self):

        ShowWords.show_ger_word(self.win, self.data[self.w_nr][0])
        ShowWords.show_gre_word(self.win, self.data[self.w_nr][1])
        ShowWords.show_decription(self.win, self.data[self.w_nr][2])
        ShowWords.show_phonetic(self.win, self.data[self.w_nr][3])
        ShowWords.show_example(self.win, self.data[self.w_nr][4])

    def new_word_loop(self):
        pass

    @staticmethod
    def play_audio_word(word):
        word_str = word
        print(word_str)
        pg.mixer.music.load("Audio/" + word_str + ".mp3")
        pg.mixer.music.set_volume(0.7)
        pg.mixer.music.play()


class ShowWords:
    @staticmethod
    def show_ger_word(win, text):
        ger_word = AppCon.fo40.render(text, True, pg.Color(AppCon.FG_P))
        ger_word_rect = ger_word.get_rect()
        ger_word_rect.midtop = (AppCon.WIN_W / 2, AppCon.WIN_H / 2 - 150)
        win.blit(ger_word, ger_word_rect)

    @staticmethod
    def show_gre_word(win, text):
        gre_word = AppCon.fo100.render(text, True, pg.Color(AppCon.FG_P))
        gre_word_rect = gre_word.get_rect()
        gre_word_rect.midtop = (AppCon.WIN_W / 2, AppCon.WIN_H / 2 - 250)
        win.blit(gre_word, gre_word_rect)

    @staticmethod
    def show_decription(win, text):
        descr = AppCon.fo23.render(text, True, pg.Color(AppCon.FG_P))
        descr_rect = descr.get_rect()
        descr_rect.midtop = (AppCon.WIN_W / 2, AppCon.WIN_H / 2)
        win.blit(descr, descr_rect)

    @staticmethod
    def show_phonetic(win, text):
        phon = AppCon.fo23.render(text, True, pg.Color(AppCon.FG_P))
        phon_rect = phon.get_rect()
        phon_rect.midtop = (AppCon.WIN_W / 2, AppCon.WIN_H / 2 - 100)
        win.blit(phon, phon_rect)

    @staticmethod
    def show_example(win, text):
        example = AppCon.fo23.render(text, True, pg.Color(AppCon.FG_P))
        example_rect = example.get_rect()
        example_rect.midtop = (AppCon.WIN_W / 2, AppCon.WIN_H / 2 + 200)
        win.blit(example, example_rect)


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
        W_GER VARCHAR(30),
        W_GRE VARCHAR(30),
        W_DES VARCHAR(30),
        W_PHO VARCHAR(30),
        W_EXA VARCHAR(30)
        );"""
        self.cursor.execute(sql_instruction)
        self.stop_connection()

    def insert_data(self, w_ge, w_gr, w_di, w_ph, w_ex):
        """Preparing SQL queries to INSERT a record into the database."""
        self.start_connection()
        self.cursor.execute("INSERT INTO DICT(W_GER, W_GRE, W_DES, W_PHO, W_EXA ) VALUES(?, ?, ?, ?, ?)",
                            (w_ge, w_gr, w_di, w_ph, w_ex))
        print("Records inserted........")
        self.stop_connection()

    def read_data(self):
        """ read all data from the database and return a list of all data"""
        self.start_connection()
        self.cursor.execute('''SELECT * from DICT''')
        data_dict = self.cursor.fetchall()
        self.stop_connection()
        return data_dict

    def read_ger_words(self):
        """read all german words from the dictionary"""
        self.start_connection()
        self.cursor.execute('''SELECT W_GER from DICT''')
        ger_words = self.cursor.fetchall()
        self.stop_connection()
        return ger_words

    def delete_data(self, t_xt):
        """a delete function, whose deleting the given word"""
        self.start_connection()
        self.cursor.execute("DELETE FROM DICT WHERE W_GER=?", (t_xt,))
        self.stop_connection()


if __name__ == "__main__":
    MainApp()
