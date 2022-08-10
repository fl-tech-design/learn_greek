#!/usr/bin/python3
# pylint: disable=no-member
"""
this module is a first step to a big greek learning app.
"""

import random
import time

import pygame as pg

import but_func as buf
import config as con
import data_func as daf

pg.init()
pg.mixer.init()


def new_word_func():
    """get the new word and save to the String-vars"""
    new_cat_name = input("geben sie neuen Kategorien Name in Kleinbuchstaben ein: ")
    n_w_ger = input("german word: ")
    n_w_ger_s = n_w_ger.split(" ")
    n_w_ger = n_w_ger_s[0]
    print("n_w_ger_s: ", n_w_ger_s)
    for i in range(1, len(n_w_ger_s)):
        n_w_ger += "_"
        n_w_ger += n_w_ger_s[i]
    print("n_w_ger: ", n_w_ger)
    n_w_gre = input("greek word: ")
    n_w_des = input("description: ")
    n_w_pho = input("phonetic: ")
    n_w_exa = input("example: ")
    daf.add_new_cat_name(new_cat_name, new_cat_name + ".db")
    daf.WordDict.cr_word_db(daf.WordDict(), new_cat_name + ".db")
    daf.WordDict.ins_w_to_db(daf.WordDict(), n_w_ger, n_w_gre, n_w_des, n_w_pho, n_w_exa,
                             daf.ret_db_datafiles_val(new_cat_name))
    MainApp.load_db_file_names(MainApp())


class MainApp:
    """the main class of the app"""

    def __init__(self):
        """start the window and initialize the String-vars"""
        self.u_points = None
        self.db_file_names, self.f_n_keys = [], []
        self.app_stat, self.mouse_pos = 0, None
        self.load_db_file_names()
        print(self.f_n_keys)
        self.dict_number = 0
        self.d_alpha, self.d_verbs, self.d_have, self.d_go, self.d_be, self.d_zahlen = ([],) * 6
        self.word_dict = [self.d_alpha, self.d_verbs, self.d_have, self.d_go, self.d_be, self.d_zahlen]
        self.load_all_dicts()
        self.json_dict = daf.ret_json_full()
        self.cd_counter = 3

        self.act_sql_dict = daf.WordDict.ret_db_compl(daf.WordDict(), daf.ret_db_datafiles_val("alphabet"))

        self.win = pg.display.set_mode((con.WIN_W, con.WIN_H))
        self.clock = pg.time.Clock()


        self.w_numb = 0
        self.loop_main()

    def load_ponits(self):
        self.u_points = daf.ret_u_data_val("points")


    def change_word(self, stat):
        """ take the end of the vocabulary list state """
        if stat == 0:
            if self.w_numb >= len(self.word_dict[self.dict_number]) - 1:
                self.w_numb = self.w_numb
            else:
                self.w_numb += 1
        else:
            if self.w_numb <= 0:
                self.w_numb = 0
            else:
                self.w_numb -= 1

    def events_main(self):
        """ handle the key events."""
        for event in pg.event.get():
            if event.type == pg.MOUSEBUTTONDOWN:
                if buf.b_alph.collidepoint(self.mouse_pos) and self.app_stat == 0:
                    self.dict_number = 0
                    self.app_stat = 1
                    self.play_audio_word(self.word_dict[self.dict_number][self.w_numb][0])
                if buf.digit.collidepoint(self.mouse_pos) and self.app_stat == 0:
                    self.dict_number = 5
                    self.app_stat = 1
                    self.play_audio_word(self.word_dict[self.dict_number][self.w_numb][0])
                if buf.b_sel_word_game.collidepoint(self.mouse_pos) and self.app_stat == 0:
                    self.app_stat = 2
                if buf.b_main.collidepoint(self.mouse_pos) and self.app_stat > 0:
                    self.app_stat = 0
                if buf.n_word.collidepoint(self.mouse_pos) and self.app_stat == 0:
                    new_word_func()
                if buf.b_next.collidepoint(self.mouse_pos) and self.app_stat == 1:
                    self.change_word(0)
                    self.play_audio_word(str(self.word_dict[self.dict_number][self.w_numb][0]))
                if buf.b_back.collidepoint(self.mouse_pos) and self.app_stat == 1:
                    self.change_word(1)
                    self.play_audio_word(str(self.word_dict[self.dict_number][self.w_numb][0]))
                if buf.b_play.collidepoint(self.mouse_pos) and self.app_stat == 1:
                    self.play_audio_word(self.word_dict[self.dict_number][self.w_numb][0])
            if event.type == pg.QUIT:
                buf.quit_game()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    buf.quit_game()
                if event.key == pg.K_RIGHT and self.app_stat == 1:
                    self.change_word(0)
                    self.play_audio_word(str(self.word_dict[self.dict_number][self.w_numb][0]))
                if event.key == pg.K_LEFT and self.app_stat == 1:
                    self.change_word(1)
                    self.play_audio_word(str(self.word_dict[self.dict_number][self.w_numb][0]))
                if event.key == pg.K_n:
                    new_word_func()

    def load_all_dicts(self):
        for i in range(len(self.word_dict)):
            self.word_dict[i] = daf.WordDict.ret_db_compl(daf.WordDict(), daf.ret_db_datafiles_val(self.f_n_keys[i]))
            print(self.word_dict[i])

    def load_db_file_names(self):
        self.db_file_names = daf.ret_db_datafiles()
        self.f_n_keys = list(self.db_file_names.keys())
        for i in range(len(self.db_file_names)):
            daf.WordDict.cr_word_db(daf.WordDict(), self.db_file_names[self.f_n_keys[i]])

    def loop_main(self):
        """ this is the main loop"""
        while True:
            self.mouse_pos = pg.mouse.get_pos()
            if self.app_stat == 0:
                self.loop_start()
            if self.app_stat == 1:
                self.loop_show_a_w()
            if self.app_stat == 2:
                self.loop_countdown()
            if self.app_stat == 3:
                SelectRightWordGame.loop_word_game(SelectRightWordGame(), self.win)
                self.cd_counter = 3
                self.app_stat = 0
            pg.display.update()
            self.clock.tick(con.FPS)
            self.events_main()

    def loop_start(self):
        """show the start-window with buttons for the functions of the app. App_stat: 1"""
        self.w_numb = 0
        self.load_ponits()
        self.win.fill(con.BG_G)
        self.win.blit(con.bg, (0, 0))
        self.win.blit(con.flag_ger, (25, 25))
        self.win.blit(con.flag_gre, (5, 5))
        buf.show_text(self.win, self.json_dict["text"]["tit_main"], con.FO40, 332, 10)
        buf.show_text(self.win, self.json_dict["text"]["start"], con.FO16, 430, 60)
        buf.show_text(self.win, self.json_dict["text"]["man_p_1"], con.FO16, 300, 125)
        buf.show_text(self.win, self.json_dict["user_data"]["u_name"], con.FO23, 89, 150)
        buf.show_text(self.win, self.json_dict["text"]["l_points"], con.FO23, 195, 150)
        buf.show_text(self.win, str(self.u_points), con.FO23, 300, 150)
        buf.cr_g_but(self.win, buf.b_alph, buf.b_al_x + 80, buf.b_al_y + 4, self.mouse_pos,
                     self.json_dict["text"]["l_alpha"])
        buf.cr_g_but(self.win, buf.digit, buf.dig_x + 80, buf.dig_y + 4, self.mouse_pos,
                     self.json_dict["text"]["l_digit"])
        buf.cr_g_but(self.win, buf.b_sel_word_game, buf.sel_w_x + 80, buf.sel_w_y + 8, self.mouse_pos,
                     self.json_dict["text"]["l_r_w"], con.FO16)
        buf.cr_g_but(self.win, buf.n_word, buf.n_w_x + 80, buf.n_w_y + 8, self.mouse_pos,
                     self.json_dict["text"]["l_new_w"], con.FO16)

    def loop_countdown(self):
        buf.show_countdown(self.win, self.cd_counter)
        self.cd_counter -= 1
        if self.cd_counter < 0:
            self.app_stat = 3

    def loop_verbs(self):
        buf.cr_but(self.win, buf.have, buf.have_x + 80, buf.have_y + 4, self.mouse_pos,
                   self.json_dict["text"]["l_have"])
        buf.cr_but(self.win, buf.b_go, buf.go_x + 80, buf.go_y + 4, self.mouse_pos,
                   self.json_dict["text"]["l_go"])

    def loop_show_a_w(self):
        """show the words in diverse fields. App_stat: 1"""
        self.win.fill(con.BG_G)
        fonts = [con.FO40, con.FO100, con.FO23, con.FO40, con.FO23]
        y_pos = [200, 50, 400, 275, 340]
        f_text = self.word_dict[self.dict_number][self.w_numb][4]
        f_t_split = f_text.split(" ")
        print(f_t_split)
        print(len(f_t_split))
        for i in range(5):
            buf.show_text(self.win, self.word_dict[self.dict_number][self.w_numb][i], fonts[i], con.W_MID, y_pos[i])
        buf.cr_but(self.win, buf.b_next, buf.next_x + 90, buf.next_y - 4, self.mouse_pos, "next →", con.FO40)
        buf.cr_but(self.win, buf.b_back, buf.b_ba_x + 80, buf.b_ba_y - 4, self.mouse_pos, "← back", con.FO40)
        buf.cr_but(self.win, buf.b_main, buf.main_x + 80, buf.main_y + 4, self.mouse_pos, "Hauptmenü")
        buf.cr_but_play(self.win, buf.b_play, buf.play_x + 80, buf.play_y + 4, self.mouse_pos, "")
        self.win.blit(con.hf_act, (buf.play_x - 9, buf.play_y - 9))

    def play_audio_word(self, word):
        """play a soundfile from the word."""
        pg.mixer.music.load("Audio/" + word + ".mp3")
        pg.mixer.music.set_volume(0.7)
        pg.draw.ellipse(self.win, con.FG_P, [buf.play_x - 10, buf.play_y - 10, 50, 50])
        pg.display.update()
        pg.mixer.music.play()


class SelectRightWordGame:
    def __init__(self):
        self.w_1, self.w_2, self.w_3, self.w_4, self.s_w = "", "", "", "", ""
        self.zf_z_list = []
        self.word_dict = daf.WordDict.ret_db_compl(daf.WordDict(), daf.ret_db_datafiles_val("zahlen"))
        self.but_pos_x = (120, 400, 120, 400)
        self.but_pos_y = (280, 280, 420, 420)
        self.pos_list = []
        self.set_new_w()

        self.answer = ""
        self.w_stat = True
        self.lives = 3
        self.count_r_a = 0

        self.u_points = daf.ret_u_data_val("points")

        self.b_1_x, self.b_1_y = self.but_pos_x[self.pos_list[0]], self.but_pos_y[self.pos_list[0]]
        self.b_1 = pg.Rect(self.b_1_x, self.b_1_y, 200, 100)
        self.b_2_x, self.b_2_y = self.but_pos_x[self.pos_list[1]], self.but_pos_y[self.pos_list[1]]
        self.b_2 = pg.Rect(self.b_2_x, self.b_2_y, 200, 100)
        self.b_3_x, self.b_3_y = self.but_pos_x[self.pos_list[2]], self.but_pos_y[self.pos_list[2]]
        self.b_3 = pg.Rect(self.b_3_x, self.b_3_y, 200, 100)
        self.b_4_x, self.b_4_y = self.but_pos_x[self.pos_list[3]], self.but_pos_y[self.pos_list[3]]
        self.b_4 = pg.Rect(self.b_4_x, self.b_4_y, 200, 100)

    def check_answer(self, win):
        if self.answer == self.w_1:
            self.set_new_w()
            self.count_r_a += 1
            self.u_points += 1
            daf.add_user_points(self.u_points)
        else:
            self.lives -= 1
            if self.lives == 0:
                self.loop_loose(win)
                time.sleep(3)
                self.w_stat = False

    def set_new_w(self):
        self.zf_z_list = []
        self.pos_list = []
        while len(self.pos_list) < 4:
            p_zahl = random.randint(0, 3)
            if p_zahl not in self.pos_list:
                self.pos_list.append(p_zahl)
        while len(self.zf_z_list) < 4:
            z_zahl = random.randint(0, len(self.word_dict) - 1)
            if z_zahl not in self.zf_z_list:
                self.zf_z_list.append(z_zahl)
        self.s_w = self.word_dict[self.zf_z_list[0]][1]
        self.w_1 = self.word_dict[self.zf_z_list[0]][0]
        self.w_2 = self.word_dict[self.zf_z_list[1]][0]
        self.w_3 = self.word_dict[self.zf_z_list[2]][0]
        self.w_4 = self.word_dict[self.zf_z_list[3]][0]
        self.b_1_x, self.b_1_y = self.but_pos_x[self.pos_list[0]], self.but_pos_y[self.pos_list[0]]
        self.b_2_x, self.b_2_y = self.but_pos_x[self.pos_list[1]], self.but_pos_y[self.pos_list[1]]
        self.b_3_x, self.b_3_y = self.but_pos_x[self.pos_list[2]], self.but_pos_y[self.pos_list[2]]
        self.b_4_x, self.b_4_y = self.but_pos_x[self.pos_list[3]], self.but_pos_y[self.pos_list[3]]
        self.b_1 = pg.Rect(self.b_1_x, self.b_1_y, 200, 100)
        self.b_2 = pg.Rect(self.b_2_x, self.b_2_y, 200, 100)
        self.b_3 = pg.Rect(self.b_3_x, self.b_3_y, 200, 100)
        self.b_4 = pg.Rect(self.b_4_x, self.b_4_y, 200, 100)

    def show_buttons(self, win, mouse_pos):
        buf.cr_g_but(win, self.b_1, self.but_pos_x[self.pos_list[0]] + 100, self.but_pos_y[self.pos_list[0]] + 30,
                     mouse_pos, self.w_1, con.FO40)
        buf.cr_g_but(win, self.b_2, self.but_pos_x[self.pos_list[1]] + 100, self.but_pos_y[self.pos_list[1]] + 30,
                     mouse_pos, self.w_2, con.FO40)
        buf.cr_g_but(win, self.b_3, self.but_pos_x[self.pos_list[2]] + 100, self.but_pos_y[self.pos_list[2]] + 30,
                     mouse_pos, self.w_3, con.FO40)
        buf.cr_g_but(win, self.b_4, self.but_pos_x[self.pos_list[3]] + 100, self.but_pos_y[self.pos_list[3]] + 30,
                     mouse_pos, self.w_4, con.FO40)

    def loop_word_game(self, win):
        while self.w_stat:
            win.fill(con.BG_G)
            mouse_pos = pg.mouse.get_pos()
            for event in pg.event.get():
                if event.type == pg.MOUSEBUTTONDOWN:
                    if buf.b_main.collidepoint(mouse_pos):
                        self.w_stat = False
                    if self.b_1.collidepoint(mouse_pos):
                        self.answer = self.w_1
                    if self.b_2.collidepoint(mouse_pos):
                        self.answer = self.w_2
                    if self.b_3.collidepoint(mouse_pos):
                        self.answer = self.w_3
                    if self.b_4.collidepoint(mouse_pos):
                        self.answer = self.w_4
                    self.check_answer(win)
            buf.cr_but(win, buf.b_main, buf.main_x + 80, buf.main_y + 4, mouse_pos, "Hauptmenü")
            buf.show_text(win, self.s_w, con.FO100, con.W_MID, 50)
            buf.show_text(win, daf.ret_db_text_val("l_r_ans"), con.FO23, 100, 10)
            buf.show_text(win, str(self.count_r_a), con.FO23, 220, 10)
            self.show_buttons(win, mouse_pos)
            buf.show_text(win, daf.ret_db_text_val("l_life"), con.FO23, 550, 10)

            life_pos = 600
            for i in range(self.lives):
                win.blit(con.pic_gre, (life_pos, 13))
                life_pos += 33

            pg.display.update()

    def loop_loose(self, win):
        win.fill(con.BG_G)
        buf.show_text(win, daf.ret_db_text_val("l_lose"), con.FO40, con.W_MID, 50)
        buf.show_text(win, daf.ret_db_text_val("l_g_end"), con.FO40, con.W_MID, 200)
        buf.show_text(win, str(self.count_r_a), con.FO40, 100, 200)

        pg.display.update()


if __name__ == "__main__":
    MainApp()
