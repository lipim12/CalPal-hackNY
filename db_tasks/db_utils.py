from pymongo import MongoClient
import os

def connect_db():
    username = os.environ.get("db_user")
    password = os.environ.get("db_pass")
    client = MongoClient("mongodb+srv://"+username+":"+password+"@cluster0-750e4.gcp.mongodb.net/test?retryWrites=true&w=majority")
    db = client.test
    return db
def save_to_db():
    pass
