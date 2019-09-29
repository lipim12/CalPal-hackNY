from flask_login import UserMixin
from db_tasks import db_utils

class User(UserMixin):
    def __init__(self,id, name, email, profile_pic,food_consumptions, daily_calories=2000):
        self.id = id
        self.name = name
        self.email = email
        self.profile_pic = profile_pic
        self.food_consumptions = []
        self.daily_calories = daily_calories

    @staticmethod
    def get_id_user(id):
        db = db_utils.connect_db()
        user = db.users.find_one({
            "id": id
        })

        if not user:
            return None
        user_obj = User(id=user['id'],
                        name=user['name'],
                        email=user['email'],
                        profile_pic= user['profile_pic'],
                        food_consumptions=user['food_consumptions'])
        return user_obj

    @staticmethod
    def get(db,email):

        user = db.users.find_one({
            "email": email
        })
        if not user:
            return None
        user_obj = User(id=user['id'],
                        name=user['name'],
                        email=user['email'],
                        profile_pic= user['profile_pic'],
                        food_consumptions=user['food_consumptions'],
                        daily_calories = user['daily_calories'])
        return user_obj


    @staticmethod
    def create(db, id,name, email, profile_pic,food_consumptions,daily_calories=2000):
        db.users.insert_one(
            {
                "id": id,
                "name":name,
                "email": email,
                "profile_pic": profile_pic,
                "food_consumptions":food_consumptions,
                "daily_calories":daily_calories
            }
        )
