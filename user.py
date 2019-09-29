from flask_login import UserMixin


class User(UserMixin):
    def __init__(self,id, name, email, profile_pic):
        self._id = id
        self.name = name
        self.email = email
        self.profile_pic = profile_pic

    def is_authenticated():
        return True

    @staticmethod
    def get(db,email):
        user = db.users.find_one({
            "email": email
        })
        if not user:
            return None
        print("Finded one")
        return user

    @staticmethod
    def create(db, id,name, email, profile_pic):
        db.users.insert_one(
            {
                "_id": id,
                "name":name,
                "email": email,
                "profile_pic": profile_pic,

            }
        )
        print("Inserted")
