from pymongo import MongoClient
import os

def connect_db():
    username = os.get_env("db_user")
    password = os.get_env("db_pass")
    client = MongoClient("mongodb+srv://"+username+":"+password+"@cluster0-750e4.gcp.mongodb.net/test?retryWrites=true&w=majority&ssl=true&ssl_cert_reqs=CERT_NONE")
    db = client.test
    return db
def save_to_db():
    pass
