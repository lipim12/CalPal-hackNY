from pymongo import MongoClient
import os

def connect_db():
    username = os.environ.get("db_user")
    password = os.environ.get("db_pass")
    client = MongoClient("mongodb+srv://"+username+":"+password+"@cluster0-750e4.gcp.mongodb.net/test")
    db = client.test
    return db

def save_to_db(db,user,label_name,qty=None,weight=None):
    print("Label name=>",label_name.lower() )
    check = db.diets.find_one({"name":label_name.lower()}, {"_id":0, "Calories (kcal)":1})
    if user:
        if check:
            db.users.update_one(
            {"email":user.email},
            {"$push" : {
            "food_consumptions" : {"date":"2019-09-29",
            "food" : label_name.lower(),
            "quantity":0,
            "grams":0,
            "calories": check["Calories (kcal)"]*100
            }
            }
            }
            )
    else:
        if check:
            db.users.update_one(
            {"email":"vmehta342@gmail.com"},
            {"$push" : {
            "food_consumptions" : {"date":"2019-09-29",
            "food" : label_name.lower(),
            "quantity":0,
            "grams":0,
            "calories": check["Calories (kcal)"]*100
            }
            }
            }
            )
