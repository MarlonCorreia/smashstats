import pymongo
import os
import json
from chars import ULT_CHARS
from dotenv import load_dotenv
load_dotenv()



class DataBase():

    def __init__(self):
        self.client = pymongo.MongoClient("mongodb+srv://smash:"
                                         + os.getenv("DB_PASS") + "@cluster0.5tbxl.mongodb.net/"
                                         + os.getenv("DB_NAME") + "?retryWrites=true&w=majority")

        self.my_db = self.client["db"]
        self.my_chars = self.my_db["chars"]
        self.match_ups = self.my_db["match_up"]
    
    def insert_chars(self, obj):
        self.my_chars.insert_one(obj)
    
    def insert_match_ups(self, mu_list):
        self.match_ups.insert_many(mu_list)

    def select_char_by_id(self, char_id):
        char = self.my_chars.find_one({"id": char_id}, {"name": 1})
        return char

    def select_match_up_by_char_name(self, char_name):
        res = self.match_ups.find_one({"char": char_name}, {"_id": 0, "match_up": 1})
        return res
    
    def update_match_up(self, filter, new_info):
        self.match_ups.update_one(filter, new_info)
