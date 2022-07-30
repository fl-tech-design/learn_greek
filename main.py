#!/usr/bin/python3

"""
this module is a first step to a big greek learning app.
"""

import sqlite3
import tkinter as tk


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


class UserInterface:
    """the main class of the app"""
    def __init__(self):
        """start the window and initialize the String-vars"""
        self.win = Window().win_main
        self.w_ger, self.w_gre, self.w_descr = tk.StringVar(), tk.StringVar(), tk.StringVar()
        WordDict.create_table(WordDict())
        self.new_word()
        self.data = WordDict.read_data(WordDict())
        WordDict.delete_data(WordDict(), '')
        self.ger_words = WordDict.read_ger_words(WordDict())
        self.g_w_list = []
        self.load_ger_words()
        self.show_words()
        self.win.mainloop()

    def cr_label(self, t_xt, x_p, y_p):
        """the name is program"""
        tk.Label(self.win, text=t_xt, font=(None, 16)).place(x=x_p, y=y_p)

    def load_ger_words(self):
        """make a list from all german words from the database"""
        for index, word in enumerate(self.ger_words):
            self.g_w_list.append(list(self.ger_words[index]))
            print(f"index {index}: ", word)

    def new_word(self):
        """get the new word and save to the String-vars"""
        self.w_ger.set(input("eingeben"))
        self.w_gre.set(input("eingeben"))
        self.w_descr.set(input("eingeben"))
        self.save_new_word()

    def save_new_word(self):
        """Write the new word in the databse"""
        WordDict.insert_data(WordDict(), self.w_ger.get(), self.w_gre.get(), self.w_descr.get())

    def show_words(self):
        """display all words in labels"""
        y_pos = 100
        for i in range(3):
            self.cr_label(self.data[0][i], 100, y_pos)
            y_pos += 30


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
        sql_anweisung = """
        CREATE TABLE IF NOT EXISTS DICT (
        W_GE VARCHAR(30),
        W_GR VARCHAR(30),
        W_DIS VARCHAR(30)
        );"""
        self.cursor.execute(sql_anweisung)
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
        result = self.cursor.fetchall()
        self.stop_connection()
        print("data readed")
        return result

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


if __name__ == "__main__":
    UserInterface()
