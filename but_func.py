import sys
import time

import pygame as pg

import config as conf


b_al_x, b_al_y = 40, 200
b_alph = pg.Rect(b_al_x, b_al_y, 160, 30)

dig_x, dig_y = 40, 240
digit = pg.Rect(dig_x, dig_y, 160, 30)

sel_w_x, sel_w_y = 210, 200
b_sel_word_game = pg.Rect(sel_w_x, sel_w_y, 160, 30)

b_ba_x, b_ba_y = 20, 500
b_back = pg.Rect(b_ba_x, b_ba_y, 160, 30)

be_x, be_y = 40, 240
b_be = pg.Rect(be_x, be_y, 160, 30)


go_x, go_y = 40, 450
b_go = pg.Rect(go_x, go_y, 160, 30)

have_x, have_y = 40, 350
have = pg.Rect(have_x, have_y, 160, 30)

main_x, main_y = conf.W_MID - 80, conf.WIN_H - 40
b_main = pg.Rect(main_x, main_y, 160, 30)

next_x, next_y = conf.WIN_W - 180, 500
b_next = pg.Rect(next_x, next_y, 160, 30)

play_x, play_y = conf.WIN_W / 2, 500
b_play = pg.Rect(play_x, play_y, 32, 32)


verb_x, verb_y = 40, 350
verb = pg.Rect(verb_x, verb_y, 160, 30)

n_w_x, n_w_y = 178, 85
n_word = pg.Rect(n_w_x, n_w_y, 160, 30)












def cr_but(w, rect, p_x, p_y, mouse_pos, text, fo=conf.FO23):
    """create a button at the inserted position"""
    pg.draw.rect(w, conf.BG_G, rect)
    if rect.collidepoint(mouse_pos):
        show_text(w, text, fo, p_x, p_y)
    else:
        show_text(w, text, fo, p_x, p_y, 1)


def cr_g_but(win, rect, p_x, p_y, mouse_pos, text, fo=conf.FO23):
    """create a button at the inserted position"""
    if rect.collidepoint(mouse_pos):
        pg.draw.rect(win, conf.FG_A, rect, 1, 5)
        show_text(win, text, fo, p_x, p_y)
    else:
        pg.draw.rect(win, conf.FG_P, rect, 1, 5)
        show_text(win, text, fo, p_x, p_y, 1)


def cr_but_play(win, rect, p_x, p_y, mouse_pos, text, fo=conf.FO23):
    """create a button at the inserted position"""
    pg.draw.ellipse(win, conf.BG_G, rect)
    if rect.collidepoint(mouse_pos):
        pg.draw.ellipse(win, conf.FG_P, rect)
        show_text(win, text, fo, p_x, p_y)
    else:
        pg.draw.ellipse(win, conf.BG_G, rect)
        show_text(win, text, fo, p_x, p_y, 1)


def show_text(win, text, font, p_x, p_y, act=0):
    """create a text-field who changed the color if collided"""
    if act == 0:
        text = font.render(text, True, pg.Color(conf.FG_P))
    else:
        text = font.render(text, True, pg.Color(conf.FG_A))
    text_rect = text.get_rect()
    text_rect.midtop = (p_x, p_y)
    win.blit(text, text_rect)


def show_countdown(win, counter):
    c_x, c_y = conf.W_MID - 100, conf.WIN_H / 2 - 100
    rect_circle = pg.Rect(c_x, c_y, 200, 200)
    pg.draw.ellipse(win, conf.FG_A, rect_circle)
    c_3 = conf.FO100.render(str(counter), True, pg.Color(conf.FG_P))
    c_3_rect = c_3.get_rect()
    c_3_rect.midtop = (c_x + 100, c_y + 55)
    time.sleep(1)
    win.blit(c_3, c_3_rect)


def quit_game():
    """ quit the game and close the window"""
    pg.quit()
    sys.exit(0)
