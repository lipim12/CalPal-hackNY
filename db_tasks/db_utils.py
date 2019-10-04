import os

from pymongo import MongoClient


def connect_db():
    username = os.environ.get("db_user")
    password = os.environ.get("db_pass")
    print(username)
    client = MongoClient("mongodb+srv://"+username+":" +
                         password+"@cluster0-750e4.gcp.mongodb.net/test")
    db = client.test
    return db


def save_to_db(db, user, label_name, qty=None, weight=None):
    print("Label name=>", label_name.lower())
    check = db.diets.find_one({"name": label_name.lower()}, {
                              "_id": 0, "Calories (kcal)": 1})
    if user:
        if check:
            db.users.update_one(
                {"email": user['email']},
                {"$push": {
                    "food_consumptions": {"date": "2019-09-29",
                                          "food": label_name.lower(),
                                          "quantity": 0,
                                          "grams": 0,
                                          "calories": check["Calories (kcal)"]*100
                                          }
                }
                }
            )
    else:
        if check:
            db.users.update_one(
                {"email": "vmehta342@gmail.com"},
                {"$push": {
                    "food_consumptions": {"date": "2019-09-29",
                                          "food": label_name.lower(),
                                          "quantity": 0,
                                          "grams": 0,
                                          "calories": check["Calories (kcal)"]*100
                                          }
                }
                }
            )

    return check


def finding_remaining_calories(db, user):
    daily = db.users.find_one({"email": user['email']})["daily_calories"]
    today_date = "2019-09-29"
    today_total = db.users.aggregate([
        {
            "$match": {"email": user['email']}
        },
        {
            "$unwind": "$food_consumptions"
        },
        {
            "$match": {"food_consumptions.date": today_date}
        },
        {
            "$group": {
                "_id": "null",
                "total": {"$sum": "$food_consumptions.calories"}
            }
        }
    ])
    for i in today_total:
        today_total = i["total"]
        break
    print(today_date, today_total, daily-today_total)
    return daily-today_total


def get_recommandation(db, remaining_calories):
    recoms = db.diets.find(
        {
            "Calories (kcal)": {
                "$lt": remaining_calories
            }
        },
        {
            "_id": 0, 
            "name": 1, 
            "Calories (kcal)": 1, 
            "emoji": 1
        }
    )
    return recoms
