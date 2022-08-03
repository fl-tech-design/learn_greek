import pygame as pg
pg.init()
"""this class defines the game fonts"""
FO100 = pg.font.SysFont("Arial", 100)
FO40 = pg.font.SysFont("Arial", 40)
FO23 = pg.font.SysFont("Arial", 23)
FO16 = pg.font.SysFont("Arial", 16)
FG_A, FG_P, BG_G = (0, 0, 200), (180, 180, 180), (20, 20, 20)
RED, GREEN = (255, 0, 0), (0, 255, 0)
WIN_W, WIN_H = 700, 650
W_MID = WIN_W/2
FPS = 10
flag_gre = pg.image.load("Picture/flag_gre.png")
flag_ger = pg.image.load("Picture/flag_ger.png")
hf_act = pg.image.load("Picture/hf.png")
hf_pas = pg.image.load("Picture/hf_d.png")
