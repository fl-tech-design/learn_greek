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
class ApC:
    """this class defines the game fonts"""
    FO100 = pg.font.SysFont("Arial", 100)
    FO40 = pg.font.SysFont("Arial", 40)
    FO23 = pg.font.SysFont("Arial", 23)
    FO16 = pg.font.SysFont("Arial", 16)
    FG_A, FG_P, BG_G = (0, 0, 200), (180, 180, 180), (25, 25, 25)
    RED, GREEN = (255, 0, 0), (0, 255, 0)
    WIN_W, WIN_H = 700, 650
    FPS = 10
    flag_gre = pg.image.load("Picture/flag_gre.png")
    flag_ger = pg.image.load("Picture/flag_ger.png")
    hf_act = pg.image.load("Picture/hf.png")
    hf_pas = pg.image.load("Picture/hf_d.png")


class ButRect:
    main_x, main_y = 20, ApC.WIN_H - 40
    voca_x, voca_y = 100, 300

    alph_x, alph_y = 40, 150
    verb_x, verb_y = ApC.WIN_W / 2 - 80, 150
    vip_x, vip_y = ApC.WIN_W / 2 + 150, 150

    b_next_x, b_next_y = ApC.WIN_W / 2, 500
    b_back_x, b_back_y = ApC.WIN_W / 2 - 180, 500
    b_play_x, b_play_y = 600, 500

    main = pg.Rect(main_x, main_y, 160, 30)
    next = pg.Rect(b_next_x, b_next_y, 160, 30)
    back = pg.Rect(b_back_x, b_back_y, 160, 30)
    voca = pg.Rect(voca_x, voca_y, 200, 30)
    play = pg.Rect(b_play_x, b_play_y, 32, 32)
    alph = pg.Rect(alph_x, alph_y, 160, 30)
    verb = pg.Rect(verb_x, verb_y, 160, 30)
    vip = pg.Rect(vip_x, vip_y, 160, 30)


def quit_game():
    """ quit the game and close the window"""
    pg.quit()
    sys.exit(0)


class MainApp:
    """the main class of the app"""

    def __init__(self):
        """start the window and initialize the String-vars"""
        self.d_impo, self.d_verb, self.d_alph, self.d_info = (None,) * 4
        self.w_nr, self.app_stat, self.mouse_pos = 0, 0, None

        self.word_cat_list = ["DICT", "VERBS", "IMPORTED", "INFO"]
        self.word_dict_list = [self.d_impo, self.d_verb, self.d_alph]

        for i in range(len(self.word_cat_list)):
            WordDict.create_table(WordDict(), self.word_cat_list[i])

        self.load_all_dicts()

        self.win = pg.display.set_mode((ApC.WIN_W, ApC.WIN_H))
        self.clock = pg.time.Clock()

        self.ger_w_list = []
        self.act_cat = "DICT"
        self.ger_words = WordDict().r_ger_w(self.act_cat)
        self.end_of_voc_list = len(WordDict().r_ger_w(self.act_cat))
        self.load_ger_w_to_list()
        print("self.end_of_voc_list: ", self.end_of_voc_list)
        self.main_loop(0)

    def load_ger_w_to_list(self):
        """make a list from all german words from the database"""
        length = len(self.ger_words)
        print("length from l_ger_w function: ", length)
        for index in range(length):
            self.ger_w_list.append(list(self.ger_words[index]))

    def new_word(self):
        """get the new word and save to the String-vars"""
        cat = input("Kategorie eingeben: ")
        n_w_ger = input("german word: ")
        n_w_gre = input("greek word: ")
        n_w_des = input("description: ")
        n_w_pho = input("phonetic: ")
        n_w_exa = input("example: ")
        WordDict.ins_full_word(WordDict(), n_w_ger, n_w_gre, n_w_des, n_w_pho, n_w_exa, cat)
        self.load_all_dicts()

    def load_all_dicts(self):
        self.d_alph = WordDict.r_data(WordDict(), "*", self.word_cat_list[0])
        self.d_verb = WordDict.r_data(WordDict(), "*", self.word_cat_list[1])
        self.d_impo = WordDict.r_data(WordDict(), "*", self.word_cat_list[2])
        self.d_info = WordDict.r_data(WordDict(), "*", self.word_cat_list[3])
        print(self.d_alph), print(self.d_verb), print(self.d_impo), print(self.d_info)

    def save_end_of_voc_list(self, stat):
        """ take the end of the vocabulary list.
            state
        """
        if stat == 0:
            if self.w_nr >= self.end_of_voc_list - 1:
                self.w_nr = self.end_of_voc_list - 1
            else:
                self.w_nr += 1
        else:
            if self.w_nr <= 0:
                self.w_nr = 0
            else:
                self.w_nr -= 1

    def event_control(self):
        """ handle the key events."""
        for event in pg.event.get():
            self.mouse_pos = pg.mouse.get_pos()
            if event.type == pg.MOUSEBUTTONDOWN:
                if ButRect.main.collidepoint(self.mouse_pos):
                    self.app_stat = 0
                if ButRect.voca.collidepoint(self.mouse_pos):
                    self.app_stat = 1
                if ButRect.alph.collidepoint(self.mouse_pos):
                    self.act_cat = "DICT"
                    self.ger_words = WordDict().r_ger_w(self.act_cat)
                    self.app_stat = 2
                if ButRect.verb.collidepoint(self.mouse_pos):
                    self.app_stat = 3
                    self.act_cat = "VERBS"
                    self.ger_words = WordDict().r_ger_w(self.act_cat)
                if ButRect.vip.collidepoint(self.mouse_pos):
                    self.act_cat = "IMPORTED"
                    self.app_stat = 4
                if ButRect.next.collidepoint(self.mouse_pos):
                    ExT.play_audio_word(str(self.ger_w_list[self.w_nr]))
                if ButRect.back.collidepoint(self.mouse_pos):
                    self.save_end_of_voc_list(1)
                    ExT.play_audio_word(str(self.ger_w_list[self.w_nr]))
                if ButRect.play.collidepoint(self.mouse_pos):
                    ExT.play_audio_word(str(self.ger_w_list[self.w_nr]))
                    self.win.blit(ApC.hf_pas, (ButRect.b_play_x - 9, ButRect.b_play_y - 9))
            if ButRect.play.collidepoint(self.mouse_pos):
                self.win.blit(ApC.hf_pas, (ButRect.b_play_x - 9, ButRect.b_play_y - 9))
            if event.type == pg.QUIT:
                quit_game()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    quit_game()
                if event.key == pg.K_RIGHT:
                    self.save_end_of_voc_list(0)
                    ExT.play_audio_word(str(self.ger_w_list[self.w_nr]))
                if event.key == pg.K_LEFT:
                    self.save_end_of_voc_list(1)
                    ExT.play_audio_word(str(self.ger_w_list[self.w_nr]))
                if event.key == pg.K_n:
                    self.new_word()
                if event.key == pg.K_d:
                    WordDict.delete_data(WordDict())

    def cr_but(self, rect, text, p_x, p_y):
        """create a button at the inserted position"""
        if rect.collidepoint(self.mouse_pos):
            pg.draw.ellipse(self.win, ApC.FG_A, rect)
            ExT.show_text(self.win, text, ApC.FO23, p_x, p_y)
        else:
            pg.draw.rect(self.win, ApC.BG_G, rect)
            ExT.show_text(self.win, text, ApC.FO23, p_x, p_y, 1)

    def main_loop(self, delay):
        """ this is the main loop"""
        while True:
            self.win.fill(ApC.BG_G)
            self.event_control()
            if self.app_stat == 0:
                self.start_loop()
            elif self.app_stat == 1:
                self.voc_men_loop()
            elif self.app_stat >= 2:
                self.show_word_loop()
            pg.display.update()
            self.clock.tick(ApC.FPS)
            print("self.ger_words from m_loop: ", self.ger_words)
            print("len(self.ger_words) from m_loop: ", len(self.ger_words))

            time.sleep(delay)

    def start_loop(self):
        """show the start-window with buttons for the functions of the app. App_stat: 1"""
        self.win.blit(ApC.flag_ger, (25, 25))
        self.win.blit(ApC.flag_gre, (5, 5))
        ExT.show_text(self.win, "griechisch lernen...", ApC.FO40, 350, 25)
        self.cr_but(ButRect.voca, "Vokabular", ButRect.voca_x + 100, ButRect.voca_y + 4)

    def voc_men_loop(self):
        """shows a window for the vocabulary choice"""
        ExT.show_text(self.win, "Vokabeln:", ApC.FO40, ApC.WIN_W / 2, 25)
        ExT.show_text(self.win, "Hier kannst Du unter verschiedenen Kategorien auswählen.", ApC.FO23, 350, 75)

        self.cr_but(ButRect.alph, "Alphabet", ButRect.alph_x + 80, ButRect.alph_y + 4)
        self.cr_but(ButRect.verb, "Verben", ButRect.verb_x + 80, ButRect.verb_y + 4)
        self.cr_but(ButRect.vip, "Wichtige Wörter", ButRect.vip_x + 80, ButRect.vip_y + 4)
        self.cr_but(ButRect.main, "Hauptmenü", ButRect.main_x + 80, ButRect.main_y + 4)

    def show_word_loop(self):
        """show the words in diverse fields. App_stat: 1"""
        f_list = [ApC.FO40, ApC.FO100, ApC.FO40, ApC.FO23, ApC.FO23]
        y_pos = [220, 100, 300, 400, 450]

        for index in range(5):
            if self.app_stat == 2:
                ExT.show_text(self.win, self.d_alph[self.w_nr][index], f_list[index], ApC.WIN_W / 2, y_pos[index])
            if self.app_stat == 3:
                ExT.show_text(self.win, self.d_verb[self.w_nr][index], f_list[index], ApC.WIN_W / 2, y_pos[index])
            if self.app_stat == 4:
                ExT.show_text(self.win, self.d_impo[self.w_nr][index], f_list[index], ApC.WIN_W / 2, y_pos[index])

        self.cr_but(ButRect.next, "next", ButRect.b_next_x + 80, ButRect.b_next_y + 4)
        self.cr_but(ButRect.back, "back", ButRect.b_back_x + 80, ButRect.b_back_y + 4)
        self.cr_but(ButRect.main, "Hauptmenü", ButRect.main_x + 80, ButRect.main_y + 4)
        self.cr_but(ButRect.play, "", ButRect.b_play_x + 80, ButRect.b_play_y + 4)
        self.win.blit(ApC.hf_act, (ButRect.b_play_x - 9, ButRect.b_play_y - 9))


class ExT:
    """include some functions for the main app"""

    @staticmethod
    def show_text(win, text, font, p_x, p_y, act=0):
        """create a text-field who changed the color if collided"""
        if act == 0:
            title = font.render(text, True, pg.Color(ApC.FG_P))
        else:
            title = font.render(text, True, pg.Color(ApC.FG_A))
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

    def start_connection(self):
        """open a connection to the database"""
        self.conn = sqlite3.connect('dictionary.db')
        self.cursor = self.conn.cursor()

    def stop_connection(self):
        """close the opened connection from database"""
        self.conn.commit()
        self.conn.close()

    def create_table(self, cat):
        """Check if a database is there. if not, it'll be created"""
        self.start_connection()
        sql_instruction = "CREATE TABLE IF NOT EXISTS " + cat + " ( W_GER VARCHAR(30)," \
                                                                "W_GRE VARCHAR(30)," \
                                                                "W_DES VARCHAR(30)," \
                                                                "W_PHO VARCHAR(30)," \
                                                                "W_EXA VARCHAR(30)," \
                                                                "W_POS INT)"
        self.cursor.execute(sql_instruction)
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
        self.cursor.execute("UPDATE DICT SET W_POS=? WHERE W_GER=?", (step, "sdf"))
        self.stop_connection()

    def r_data(self, key_w, dic):
        """ read all data from the database and return a list of all data"""
        self.start_connection()
        self.cursor.execute("SELECT " + key_w + " from " + dic)
        data_dict = self.cursor.fetchall()
        self.stop_connection()
        return data_dict

    def r_ger_w(self, cat):
        """read all german words from the dictionary"""
        self.start_connection()
        self.cursor.execute("SELECT W_GER from " + cat)
        ger_words = self.cursor.fetchall()
        self.stop_connection()
        print("ger_words from r_ger_w: ", ger_words)
        return ger_words

    def r_act_descr(self, cat):
        """read all german words from the dictionary"""
        self.start_connection()
        self.cursor.execute("SELECT W_DES from " + cat)
        descr = self.cursor.fetchall()
        des_str = str(descr)
        print("len(des_str): ", len(des_str))
        des_str_split = des_str.split()
        print("des_str_split: ", des_str_split)
        self.stop_connection()
        for i in range(len(des_str_split)):
            print("des_str_split[i]: ", des_str_split[i])
        return descr

    def delete_data(self):
        """a delete function, whose deleting the given word"""
        dic = input("Wort-Kategorie eingeben: ")
        t_xt = input("insert word to delete: ")
        self.start_connection()
        self.cursor.execute("DELETE FROM " + dic + " WHERE W_GER=?", (t_xt,))
        self.stop_connection()


objects = []
if __name__ == "__main__":
    MainApp()
