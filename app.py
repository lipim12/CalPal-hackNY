import json
import os
import sqlite3
import requests

# Third-party libraries
from flask import Flask, redirect, request, url_for, jsonify
import flask
from flask_login import (
    LoginManager,
    current_user,
    login_required,
    login_user,
    logout_user,
)
from flask_cors import CORS
from cloud_vision import vision_pubsub

# Internal imports
from db_tasks.db_utils import connect_db
from user import User
from db_tasks.db_utils import save_to_db, finding_remaining_calories, get_recommandation

# Configuration
GOOGLE_CLIENT_ID = os.environ.get("GOOGLE_CLIENT_ID", None)
GOOGLE_CLIENT_SECRET = os.environ.get("GOOGLE_CLIENT_SECRET", None)
GOOGLE_DISCOVERY_URL = (
    "https://accounts.google.com/.well-known/openid-configuration"
)


app = Flask(__name__)
CORS(app)
app.secret_key = os.environ.get("SECRET_KEY") or os.urandom(24)

# User session management setup
# https://flask-login.readthedocs.io/en/latest
login_manager = LoginManager()
login_manager.init_app(app)

# # Naive database setup
# try:
db = connect_db()


user = db.users.find_one({"email": "vmehta342@gmail.com"})
# except:
#     # Assume it's already been created
#     print("errrorrrr")
#     pass


# OAuth 2 client setup
# client = WebApplicationClient(GOOGLE_CLIENT_ID)

# Flask-Login helper to retrieve a user from our db
# @login_manager.user_loader
# def load_user(id):
#     return User.get_id_user(id)


@app.route("/")
def index():
    # if current_user.is_authenticated:
    #     return (
    #         "<p>Hello, {}! You're logged in! Email: {}</p>"
    #         "<div><p>Google Profile Picture:</p>"
    #         '<img src="{}" alt="Google profile pic"></img></div>'
    #         '<a class="button" href="/logout">Logout</a>'.format(
    #             current_user.name, current_user.email, current_user.profile_pic
    #         ) + "<br>"
    #
    #     )
    # else:
    return '<a class="button" href="/add_request">test db</a>'


# def get_google_provider_cfg():
#     return requests.get(GOOGLE_DISCOVERY_URL).json()

# @app.route("/login")
# def login():
#     # Find out what URL to hit for Google login
#     google_provider_cfg = get_google_provider_cfg()
#     authorization_endpoint = google_provider_cfg["authorization_endpoint"]
#
#     # Use library to construct the request for Google login and provide
#     # scopes that let you retrieve user's profile from Google
#     request_uri = client.prepare_request_uri(
#         authorization_endpoint,
#         redirect_uri=request.base_url + "/callback",
#         scope=["openid", "email", "profile"],
#     )
#     return redirect(request_uri)

#
# @app.route("/login/callback")
# def callback():
#     # Get authorization code Google sent back to you
#     code = request.args.get("code")
#
#
#     # Find out what URL to hit to get tokens that allow you to ask for
#     # things on behalf of a user
#     google_provider_cfg = get_google_provider_cfg()
#     token_endpoint = google_provider_cfg["token_endpoint"]
#
#
#     # Prepare and send a request to get tokens! Yay tokens!
#     token_url, headers, body = client.prepare_token_request(
#         token_endpoint,
#         authorization_response=request.url,
#         redirect_url=request.base_url,
#         code=code
#     )
#     token_response = requests.post(
#         token_url,
#         headers=headers,
#         data=body,
#         auth=(GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET),
#     )
#
#     # Parse the tokens!
#     client.parse_request_body_response(json.dumps(token_response.json()))
#
#
#     # Now that you have tokens (yay) let's find and hit the URL
#     # from Google that gives you the user's profile information,
#     # including their Google profile image and email
#     userinfo_endpoint = google_provider_cfg["userinfo_endpoint"]
#     uri, headers, body = client.add_token(userinfo_endpoint)
#     userinfo_response = requests.get(uri, headers=headers, data=body)
#
#
#     # You want to make sure their email is verified.
#     # The user authenticated with Google, authorized your
#     # app, and now you've verified their email through Google!
#     if userinfo_response.json().get("email_verified"):
#         unique_id = userinfo_response.json()["sub"]
#         users_email = userinfo_response.json()["email"]
#         picture = userinfo_response.json()["picture"]
#         users_name = userinfo_response.json()["given_name"]
#     else:
#         return "User email not available or not verified by Google.", 400
#
#
#     # Create a user in your db with the information provided
#     # by Google
#
#     print("herererr")
#     user_l = User(
#         id=unique_id,name=users_name, email=users_email, profile_pic=picture,food_consumptions=[]
#     )
#     print("hrererer")
#     # Doesn't exist? Add it to the database.
#     if not User.get(db,users_email):
#         User.create(db,unique_id,users_name, users_email, picture,[])
#
#     # Begin user session by logging the user in
#     login_user(user_l)
#     temp = user_l
#     global user
#     user = temp
#     # Send user back to homepage
#     return redirect(url_for("index"))
#

#
# @app.route("/logout")
# @login_required
# def logout():
#     logout_user()
#     global user
#     user = None
#     return redirect(url_for("index"))


@app.route("/add_request", methods=['GET', 'POST'])
def test_upload():
    """
    This function is only to check the add endpoint of the system.
    """

    URL = "http://192.168.1.163:5000/add"
    with open("output.txt", "r") as image_text_file:
        base64str = image_text_file.read()
    request_data = {
        "image": base64str
    }
    r = requests.post(url=URL, json=request_data)
    return json.dumps(r.json())


@app.route("/add", methods=["GET", "POST"])
def upload():

    if flask.request.method == "POST":
        flask_json = flask.request.get_json()
    else:
        return jsonify(
            label_name=None,
            qty=None,
            weight=None,
            msg="Sorry please make POST request"
        )

    if "image" in flask_json:
        label_name = vision_pubsub(flask_json['image'].encode("utf-8"))
    elif "fruit_name" in flask_json:
        fruit_name = flask_json['fruit_name']
    else:
        return jsonify(
            label_name=None,
            qty=None,
            weight=None,
            msg="Sorry please use fruit name or select photo"
        )

    global user
    if user is not None:
        check = save_to_db(db, user, label_name, None, None)
    else:
        user = db.users.find_one({"email": "vmehta342@gmail.com"})
        check = save_to_db(db, user, label_name, None, None)
    print("Check==>",check)
    remaining_calories = finding_remaining_calories(db, user)
    recommendations = get_recommandation(db, remaining_calories)

    final_list = []

    for i in recommendations:
        final_list.append(i)

    return jsonify(
        user_email=user['email'],
        calories=check['Calories (kcal)']*100,
        label_name=label_name,
        qty=None,
        weight=None,
        msg="Success",
        daily_calories=user["daily_calories"],
        remaining_calories=remaining_calories,
        recommendations=final_list
    )


if __name__ == "__main__":
    app.run("0.0.0.0", port=5000)
