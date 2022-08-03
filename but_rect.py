import pygame as pg
import config as ApC

main_x, main_y = 20, ApC.WIN_H - 40
voca_x, voca_y = 100, 250
n_word_x, n_word_y = 300, 250

alph_x, alph_y = 40, 150
verb_x, verb_y = ApC.WIN_W / 2 - 80, 150
vip_x, vip_y = ApC.WIN_W / 2 + 150, 150

b_next_x, b_next_y = ApC.WIN_W -180, 500
b_back_x, b_back_y = 20, 500
b_play_x, b_play_y = ApC.WIN_W/2, 500

main = pg.Rect(main_x, main_y, 160, 30)
next = pg.Rect(b_next_x, b_next_y, 160, 30)
back = pg.Rect(b_back_x, b_back_y, 160, 30)
voca = pg.Rect(voca_x, voca_y, 200, 30)
play = pg.Rect(b_play_x, b_play_y, 32, 32)
alph = pg.Rect(alph_x, alph_y, 160, 30)
verb = pg.Rect(verb_x, verb_y, 160, 30)
vip = pg.Rect(vip_x, vip_y, 160, 30)
n_word = pg.Rect(n_word_x, n_word_y, 160, 30)
