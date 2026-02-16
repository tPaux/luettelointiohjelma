import sqlite3
from flask import Flask, redirect, render_template, request, session
from werkzeug.security import generate_password_hash, check_password_hash
import db
import config
import lists

app = Flask(__name__)
app.secret_key = config.secret_key


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        sql = "SELECT id, password_hash FROM users WHERE username = ?"
        row = db.query(sql, [username])[0]
        user_id = row[0]
        password_hash = row[1]

        if check_password_hash(password_hash, password):
            session["username"] = username
            session["user_id"] = user_id

            return redirect("/")

        else:
            return "VIRHE: väärä tunnus tai salasana"

@app.route("/logout")
def logout():
    del session["username"]
    return redirect("/")

@app.route("/register")
def register():
    return render_template("register.html")

@app.route("/create", methods=["POST"])
def create():
    username = request.form["username"]
    password1 = request.form["password1"]
    password2 = request.form["password2"]
    if password1 != password2:
        return "VIRHE: salasanat eivät ole samat"
    password_hash = generate_password_hash(password1)

    try:
        sql = "INSERT INTO users (username, password_hash) VALUES (?, ?)"
        db.execute(sql, [username, password_hash])
    except sqlite3.IntegrityError:
        return "VIRHE: tunnus on jo varattu"

    return redirect("/")

@app.route("/")
def index():
    q = request.args.get("q", "")
    items = lists.get_items(q)

    return render_template("index.html", items=items)


@app.route("/new_item", methods=["POST"])
def new_item():
    ttyype = request.form["ttyype"]
    author = request.form["author"]
    title = request.form["title"]
    year = request.form["year"]
    creator = request.form["creator"]
    condition = request.form["condition"]
    content = request.form["content"]
    user_id = session["user_id"]

    item_id = lists.add_item(ttyype, author, title, year, creator, condition, content, user_id)

    return redirect("/item/" + str(item_id))

@app.route("/item/<int:item_id>")
def show_item(item_id):
    item = lists.get_item(item_id)
    return render_template("item.html", item=item)




