import json
import os
import sqlite3
import requests
# Third-party libraries
from flask import Flask, redirect, request, url_for,jsonify
import flask
from flask_login import (
    LoginManager,
    current_user,
    login_required,
    login_user,
    logout_user,
)
from oauthlib.oauth2 import WebApplicationClient
import requests
from flask_cors import CORS
# Internal imports
from db_tasks.db_utils import connect_db
from user import User
from cloud_vision import vision_pubsub
from db_tasks.db_utils import save_to_db
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


# except:
#     # Assume it's already been created
#     print("errrorrrr")
#     pass


# OAuth 2 client setup
client = WebApplicationClient(GOOGLE_CLIENT_ID)

# Flask-Login helper to retrieve a user from our db
@login_manager.user_loader
def load_user(id):
    return User.get_id_user(id)


@app.route("/")
def index():
    print(current_user.is_authenticated)
    if current_user.is_authenticated:
        return (
            "<p>Hello, {}! You're logged in! Email: {}</p>"
            "<div><p>Google Profile Picture:</p>"
            '<img src="{}" alt="Google profile pic"></img></div>'
            '<a class="button" href="/logout">Logout</a>'.format(
                current_user.name, current_user.email, current_user.profile_pic
            ) + "<br>"
            '<a class="button" href="/add_request">test db</a>'
        )
    else:
        return '<a class="button" href="/login">Google Login</a>'



def get_google_provider_cfg():
    return requests.get(GOOGLE_DISCOVERY_URL).json()

user = None
@app.route("/login")
def login():
    # Find out what URL to hit for Google login
    google_provider_cfg = get_google_provider_cfg()
    authorization_endpoint = google_provider_cfg["authorization_endpoint"]

    # Use library to construct the request for Google login and provide
    # scopes that let you retrieve user's profile from Google
    request_uri = client.prepare_request_uri(
        authorization_endpoint,
        redirect_uri=request.base_url + "/callback",
        scope=["openid", "email", "profile"],
    )
    return redirect(request_uri)


@app.route("/login/callback")
def callback():
    # Get authorization code Google sent back to you
    code = request.args.get("code")


    # Find out what URL to hit to get tokens that allow you to ask for
    # things on behalf of a user
    google_provider_cfg = get_google_provider_cfg()
    token_endpoint = google_provider_cfg["token_endpoint"]


    # Prepare and send a request to get tokens! Yay tokens!
    token_url, headers, body = client.prepare_token_request(
        token_endpoint,
        authorization_response=request.url,
        redirect_url=request.base_url,
        code=code
    )
    token_response = requests.post(
        token_url,
        headers=headers,
        data=body,
        auth=(GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET),
    )

    # Parse the tokens!
    client.parse_request_body_response(json.dumps(token_response.json()))


    # Now that you have tokens (yay) let's find and hit the URL
    # from Google that gives you the user's profile information,
    # including their Google profile image and email
    userinfo_endpoint = google_provider_cfg["userinfo_endpoint"]
    uri, headers, body = client.add_token(userinfo_endpoint)
    userinfo_response = requests.get(uri, headers=headers, data=body)


    # You want to make sure their email is verified.
    # The user authenticated with Google, authorized your
    # app, and now you've verified their email through Google!
    if userinfo_response.json().get("email_verified"):
        unique_id = userinfo_response.json()["sub"]
        users_email = userinfo_response.json()["email"]
        picture = userinfo_response.json()["picture"]
        users_name = userinfo_response.json()["given_name"]
    else:
        return "User email not available or not verified by Google.", 400


    # Create a user in your db with the information provided
    # by Google

    print("herererr")
    user_l = User(
        id=unique_id,name=users_name, email=users_email, profile_pic=picture,food_consumptions=[]
    )
    print("hrererer")
    # Doesn't exist? Add it to the database.
    if not User.get(db,users_email):
        User.create(db,unique_id,users_name, users_email, picture,[])

    # Begin user session by logging the user in
    login_user(user_l)
    temp = user_l
    global user
    user = temp
    # Send user back to homepage
    return redirect(url_for("index"))



@app.route("/logout")
@login_required
def logout():
    logout_user()
    global user
    user = None
    return redirect(url_for("index"))


@app.route("/add_request",methods=['GET','POST'])
def test_upload():
    URL = "https://127.0.0.1:5000/add"
    request_data = {
    "image":
    "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"
    }
    r = requests.post(url = URL, json = request_data,verify=False)
    return "success"

print("here---at upload")
@app.route("/add", methods=["GET","POST"])
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
            msg="Sorry please use fruit name or select photo"\
        )
    
    print("current_user=>",current_user.is_authenticated)
    print("lable_name ====>", label_name)
    global user
    if user is not None:
        save_to_db(db,user,label_name,None,None)
    else:
        save_to_db(db,user,label_name,None,None)
    return jsonify(
        label_name=label_name,
        qty=None,
        weight=None,
        msg = "Success"
    )

if __name__ == "__main__":
    app.run(ssl_context=('cert.pem', 'key.pem'))
