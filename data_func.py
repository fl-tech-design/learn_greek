import json
import sqlite3


def ret_db_datafiles():
    """ READ THE HIGH-SCORE-FILE AND RETURN A DICT WITH THE DATA"""
    with open("BackEnd/AppData/descript.json", "r", encoding='UTF-8') as file:
        data_dict = json.load(file)
    return data_dict["datafiles"]


def ret_db_datafiles_val(key):
    """ READ THE HIGH-SCORE-FILE AND RETURN A DICT WITH THE DATA"""
    with open("BackEnd/AppData/descript.json", "r", encoding='UTF-8') as file:
        data_dict = json.load(file)
    return data_dict["datafiles"][key]


def ret_db_dict():
    """ READ THE HIGH-SCORE-FILE AND RETURN A DICT WITH THE DATA"""
    with open("BackEnd/AppData/descript.json", "r", encoding='UTF-8') as file:
        data_dict = json.load(file)
    return data_dict["dict_var"]


def ret_db_text():
    """ READ THE HIGH-SCORE-FILE AND RETURN A DICT WITH THE DATA"""
    with open("BackEnd/AppData/descript.json", "r", encoding='UTF-8') as file:
        data_dict = json.load(file)
    return data_dict["text"]


def ret_db_text_val(key_2):
    """ READ THE HIGH-SCORE-FILE AND RETURN A DICT WITH THE DATA"""
    with open("BackEnd/AppData/descript.json", "r", encoding='UTF-8') as file:
        data_dict = json.load(file)
    return data_dict["text"][key_2]

def ret_u_data_val(key_2):
    """ READ THE HIGH-SCORE-FILE AND RETURN A DICT WITH THE DATA"""
    with open("BackEnd/AppData/descript.json", "r", encoding='UTF-8') as file:
        data_dict = json.load(file)
    return data_dict["user_data"][key_2]


def ret_json_full():
    """ returns the full json file for writing new data"""
    with open("BackEnd/AppData/descript.json", "r", encoding='UTF-8') as file:
        data_dict = json.load(file)
    return data_dict


def add_new_cat_name(new_cat_key, new_cat_name):
    """ WRITE THE NEW HIGH-SCORE TO THE .JSON FILE """
    data = ret_json_full()
    data["datafiles"][new_cat_key] = new_cat_name
    with open("BackEnd/AppData/descript.json", "w", encoding='UTF-8') as file:
        json.dump(data, file)

def add_user_points(new_score):
    """ WRITE THE NEW HIGH-SCORE TO THE .JSON FILE """
    data = ret_json_full()
    data["user_data"]["points"] = new_score
    with open("BackEnd/AppData/descript.json", "w", encoding='UTF-8') as file:
        json.dump(data, file)

class WordDict:
    """ the sql class.
        str 1 = category
    """

    def __init__(self):
        """ define the vars of the class"""
        self.conn = None
        self.cursor = None

    def cr_word_db(self, db_file):
        """Check if a database is there. if not, it'll be created"""
        self.db_conn_start(db_file)
        sql_instruction = "CREATE TABLE IF NOT EXISTS WORD ( W_GER VARCHAR(30)," \
                          "W_GRE VARCHAR(30)," \
                          "W_DES VARCHAR(40)," \
                          "W_PHO VARCHAR(30)," \
                          "W_EXA VARCHAR(30)," \
                          "W_STAT INT)"
        self.cursor.execute(sql_instruction)
        self.db_conn_stop()

    def ret_db_compl(self, db):
        self.db_conn_start(db)
        self.cursor.execute("SELECT * from WORD")
        full_dict = self.cursor.fetchall()
        self.db_conn_stop()
        return full_dict

    def db_conn_start(self, db):
        """open a connection to the database"""
        self.conn = sqlite3.connect("BackEnd/AppData/" + db)
        self.cursor = self.conn.cursor()

    def db_conn_stop(self):
        """close the opened connection from database"""
        self.conn.commit()
        self.conn.close()

    def ins_w_to_db(self, w_ge, w_gr, w_di, w_ph, w_ex, db):
        """Preparing SQL queries to INSERT a record into the database."""
        self.db_conn_start(db)
        self.cursor.execute(
            "INSERT INTO WORD(W_GER, W_GRE, W_DES, W_PHO, W_EXA, W_STAT ) VALUES(?, ?, ?, ?, ?, ?)",
            (w_ge, w_gr, w_di, w_ph, w_ex, 0))
        self.db_conn_stop()
