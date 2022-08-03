#!/usr/bin/python3
# pylint: disable=no-member
"""
this module is a first step to a big greek learning app.
"""

import sqlite3
import sys

import pygame as pg

import but_rect
import config as conf

pg.init()
pg.mixer.init()


def quit_game():
    """ quit the game and close the window"""
    pg.quit()
    sys.exit(0)


class MainApp:
    """the main class of the app"""

    def __init__(self):
        """start the window and initialize the String-vars"""
        self.d_impo, self.d_verb, self.d_alph, self.d_info = (None,) * 4
        self.app_stat, self.mouse_pos = 0, None

        self.word_categories = ["ALPHABET", "VERBS", "ADJECTIVE", "VIP"]
        self.cr_word_tables()
        self.act_w_category = self.word_categories[0]

        self.full_alphabet = []
        self.load_full_tablar("ALPHABET")
        self.len_full_alphabet = len(self.full_alphabet)

        self.ger_w_list = []
        self.actualize_ger_w_list()
        self.len_ger_w_list = len(self.ger_w_list)

        self.win = pg.display.set_mode((conf.WIN_W, conf.WIN_H))
        self.clock = pg.time.Clock()

        self.w_numb = 0

        print("self.len_of_ger_word_list: ", self.len_ger_w_list)
        print(self.ger_w_list[0])
        print(self.full_alphabet[0][1])

        self.len_info_list = 0
        self.check_ger_w_length()
        self.main_loop()

    def actualize_ger_w_list(self):
        self.ger_w_list = WordDict.r_ger_w(WordDict(), self.act_w_category, "W_GER")

    def cr_word_tables(self):
        for i in range(len(self.word_categories)):
            WordDict.cr_n_word_in_sql(WordDict(), self.word_categories[i])

    def load_full_tablar(self, word_category):
        print("load full tablar: ", word_category)
        self.full_alphabet = WordDict.r_data(WordDict(), "*", word_category)
        self.len_full_alphabet = len(self.full_alphabet)

    def check_ger_w_length(self):
        self.len_ger_w_list = len(self.ger_w_list)

    def cr_but(self, rect, text, p_x, p_y, fo=conf.FO23):
        """create a button at the inserted position"""
        pg.draw.ellipse(self.win, conf.BG_G, rect)
        if rect.collidepoint(self.mouse_pos):
            ExT.show_text(self.win, text, fo, p_x, p_y)
        else:
            ExT.show_text(self.win, text, fo, p_x, p_y, 1)

    def event_control(self):
        """ handle the key events."""
        for event in pg.event.get():
            self.mouse_pos = pg.mouse.get_pos()
            if event.type == pg.MOUSEBUTTONDOWN:
                if but_rect.main.collidepoint(self.mouse_pos):
                    self.app_stat = 0
                if but_rect.voca.collidepoint(self.mouse_pos):
                    self.app_stat = 1
                if but_rect.alph.collidepoint(self.mouse_pos):
                    self.app_stat = 2
                if but_rect.verb.collidepoint(self.mouse_pos):
                    self.app_stat = 3
                if but_rect.vip.collidepoint(self.mouse_pos):
                    self.app_stat = 4
                if but_rect.n_word.collidepoint(self.mouse_pos):
                    self.new_word()
                if but_rect.next.collidepoint(self.mouse_pos):
                    self.save_end_of_voc_list(0)
                    ExT.play_audio_word(self.ger_w_list[self.w_numb])
                if but_rect.back.collidepoint(self.mouse_pos):
                    self.save_end_of_voc_list(1)
                    ExT.play_audio_word(self.ger_w_list[self.w_numb])
                if but_rect.play.collidepoint(self.mouse_pos):
                    ExT.play_audio_word(self.ger_w_list[self.w_numb])
                    self.win.blit(conf.hf_pas, (but_rect.b_play_x - 9, but_rect.b_play_y - 9))
            if but_rect.play.collidepoint(self.mouse_pos):
                self.win.blit(conf.hf_pas, (but_rect.b_play_x - 9, but_rect.b_play_y - 9))
            if event.type == pg.QUIT:
                quit_game()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    quit_game()
                if event.key == pg.K_RIGHT:
                    self.save_end_of_voc_list(0)
                    ExT.play_audio_word(str(self.ger_w_list[self.w_numb]))
                if event.key == pg.K_LEFT:
                    self.save_end_of_voc_list(1)
                    ExT.play_audio_word(str(self.ger_w_list[self.w_numb]))
                if event.key == pg.K_n:
                    self.new_word()
                if event.key == pg.K_d:
                    WordDict.delete_data(WordDict())

    @staticmethod
    def new_word():
        """get the new word and save to the String-vars"""
        cat = input("Kategorie eingeben: ")
        n_w_ger = input("german word: ")
        n_w_gre = input("greek word: ")
        n_w_des = input("description: ")
        n_w_pho = input("phonetic: ")
        n_w_exa = input("example: ")
        WordDict.ins_full_word(WordDict(), n_w_ger, n_w_gre, n_w_des, n_w_pho, n_w_exa, cat)

    def save_end_of_voc_list(self, stat):
        """ take the end of the vocabulary list state """
        if stat == 0:
            self.check_ger_w_length()
            if self.w_numb < self.len_ger_w_list - 1:
                self.w_numb += 1
            else:
                self.w_numb = self.w_numb
        else:
            if self.w_numb > 0:
                self.w_numb -= 1
            else:
                self.w_numb = 0

    def main_loop(self):
        """ this is the main loop"""
        while True:
            self.win.fill(conf.BG_G)
            self.event_control()
            self.load_full_tablar(self.act_w_category)
            self.actualize_ger_w_list()
            if self.app_stat == 0:
                self.start_loop()
            if self.app_stat == 1:
                self.voc_menu_loop()
            if self.app_stat == 2:
                print("show alphabet")
                self.act_w_category = "ALPHABET"
                self.show_word_loop()
            if self.app_stat == 3:
                print("show verbs")
                self.act_w_category = "VERBS"
                self.show_word_loop()
            if self.app_stat == 4:
                print("show VIP")
                self.act_w_category = "VIP"
                self.show_word_loop()

            pg.display.update()
            self.clock.tick(conf.FPS)

    def start_loop(self):
        """show the start-window with buttons for the functions of the app. App_stat: 1"""
        print("start_loop")
        self.win.blit(conf.flag_ger, (25, 25))
        self.win.blit(conf.flag_gre, (5, 5))
        ExT.show_text(self.win, "griechisch lernen", conf.FO40, 350, 25)
        self.show_a_long_string()

        self.cr_but(but_rect.voca, "Vokabular", but_rect.voca_x + 100, but_rect.voca_y + 4)
        self.cr_but(but_rect.n_word, "Neues Wort", but_rect.n_word_x + 80, but_rect.n_word_y + 4)

    def show_a_long_string(self):
        counter = 0
        y_pos = 150
        for i in range(self.len_info_list % 5):
            ExT.show_text(self.win, "self.format_a_string(counter)", conf.FO23, 250, y_pos)
            y_pos += 30
            counter += 5

    def voc_menu_loop(self):
        """shows a window for the vocabulary choice"""
        print("voc_menu_loop")
        ExT.show_text(self.win, "Vokabeln:", conf.FO40, conf.WIN_W / 2, 25)
        self.cr_but(but_rect.alph, "Alphabet", but_rect.alph_x + 80, but_rect.alph_y + 4)
        self.cr_but(but_rect.verb, "Verben", but_rect.verb_x + 80, but_rect.verb_y + 4)
        self.cr_but(but_rect.vip, "Wichtige Wörter", but_rect.vip_x + 80, but_rect.vip_y + 4)
        self.cr_but(but_rect.main, "Hauptmenü", but_rect.main_x + 80, but_rect.main_y + 4)

    def show_word_loop(self):
        """show the words in diverse fields. App_stat: 1"""
        print("show_word_loop")
        fonts = [conf.FO40, conf.FO100, conf.FO23, conf.FO23, conf.FO40]
        y_pos = [50, 130, 400, 350, 275]

        ExT.show_text(self.win, self.full_alphabet[self.w_numb][0], fonts[0], conf.W_MID, y_pos[0])
        ExT.show_text(self.win, self.full_alphabet[self.w_numb][1], fonts[1], conf.W_MID, y_pos[1])
        ExT.show_text(self.win, self.full_alphabet[self.w_numb][3], fonts[3], conf.W_MID, y_pos[3])
        ExT.show_text(self.win, self.full_alphabet[self.w_numb][4], fonts[4], conf.W_MID, y_pos[4])
        if len(self.full_alphabet[self.w_numb][2]) > 40:
            ExT.show_text(self.win, self.full_alphabet[self.w_numb][2], conf.FO16, conf.W_MID, y_pos[2])
        else:
            ExT.show_text(self.win, self.full_alphabet[self.w_numb][2], conf.FO23, conf.W_MID, y_pos[2])
        self.cr_but(but_rect.next, "next →", but_rect.b_next_x + 90, but_rect.b_next_y - 4, conf.FO40)
        self.cr_but(but_rect.back, "← back", but_rect.b_back_x + 80, but_rect.b_back_y - 4, conf.FO40)
        self.cr_but(but_rect.main, "Hauptmenü", but_rect.main_x + 80, but_rect.main_y + 4)
        self.cr_but(but_rect.play, "", but_rect.b_play_x + 80, but_rect.b_play_y + 4)
        self.win.blit(conf.hf_act, (but_rect.b_play_x - 9, but_rect.b_play_y - 9))


class ExT:
    """include some functions for the main app"""

    @staticmethod
    def show_text(win, text, font, p_x, p_y, act=0):
        """create a text-field who changed the color if collided"""
        if act == 0:
            title = font.render(text, True, pg.Color(conf.FG_P))
        else:
            title = font.render(text, True, pg.Color(conf.FG_A))
        title_rect = title.get_rect()
        title_rect.midtop = (p_x, p_y)
        win.blit(title, title_rect)

    @staticmethod
    def play_audio_word(word):
        """play a soundfile from the word."""
        pg.mixer.music.load("Audio/" + word + ".mp3")
        pg.mixer.music.set_volume(0.7)
        pg.mixer.music.play()


class WordDict:
    """ the sql class"""

    def __init__(self):
        """ define the vars of the class"""
        self.conn = None
        self.cursor = None

    def cr_n_word_in_sql(self, new_word):
        """Check if a database is there. if not, it'll be created"""
        self.start_connection()
        sql_instruction = "CREATE TABLE IF NOT EXISTS " + new_word + " ( W_GER VARCHAR(30)," \
                                                                     "W_GRE VARCHAR(30)," \
                                                                     "W_DES VARCHAR(40)," \
                                                                     "W_PHO VARCHAR(30)," \
                                                                     "W_EXA VARCHAR(30)," \
                                                                     "W_POS INT)"
        self.cursor.execute(sql_instruction)
        self.stop_connection()

    def cr_n_list_in_sql(self, new_list):
        """Check if a database is there. if not, it'll be created"""
        self.start_connection()
        self.cursor.execute("CREATE TABLE IF NOT EXISTS " + new_list + " ( LIST VARCHAR(300)")
        self.stop_connection()

    def ins_full_word(self, w_ge, w_gr, w_di, w_ph, w_ex, cat):
        """Preparing SQL queries to INSERT a record into the database."""
        self.start_connection()
        self.cursor.execute(
            "INSERT INTO " + cat + "(W_GER, W_GRE, W_DES, W_PHO, W_EXA, W_POS ) VALUES(?, ?, ?, ?, ?, ?)",
            (w_ge, w_gr, w_di, w_ph, w_ex, 0))
        print("Records inserted......IN: ")
        self.stop_connection()

    def change_word_state(self, step):
        """the word state increase if the word is learned"""
        self.start_connection()
        self.cursor.execute("UPDATE ALPHA SET W_POS=? WHERE W_GER=?", (step, "sdf"))
        self.stop_connection()

    def r_data(self, key_w, dic):
        """ read all data from the database and return a list of all data"""
        self.start_connection()
        self.cursor.execute("SELECT " + key_w + " from " + dic)
        data_dict = self.cursor.fetchall()
        self.stop_connection()
        return data_dict

    def r_ger_w(self, cat, tab):
        """read all german words from the dictionary"""
        self.start_connection()
        self.cursor.execute("SELECT " + tab + " from " + cat)
        ger_words = self.cursor.fetchall()
        print(ger_words)
        ge_w_str = str(ger_words)
        characters = "[]()',"
        for x in range(len(characters)):
            ge_w_str = ge_w_str.replace(characters[x], "")
        ger_w_list = ge_w_str.split()
        self.stop_connection()
        return ger_w_list

    def start_connection(self):
        """open a connection to the database"""
        self.conn = sqlite3.connect('dictionary.db')
        self.cursor = self.conn.cursor()

    def stop_connection(self):
        """close the opened connection from database"""
        self.conn.commit()
        self.conn.close()

    def delete_data(self):
        """a delete function, whose deleting the given word"""
        word = input("Wort-Kategorie eingeben: ")
        t_xt = input("insert word to delete: ")
        self.start_connection()
        self.cursor.execute("DELETE FROM " + word + " WHERE W_GER=?", (t_xt,))
        self.stop_connection()


objects = []
if __name__ == "__main__":
    MainApp()
