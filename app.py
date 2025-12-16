import sqlite3
from flask import Flask, redirect, render_template, request, session
from werkzeug.security import generate_password_hash, check_password_hash
import db
import config
import lists

app = Flask(__name__)
app.secret_key = config.secret_key

@app.route("/")
def index():
    my_lists = lists.get_lists()
    return render_template("index.html", lists=my_lists)

@app.route("/lists")
def lists_view():  
    my_lists = lists.get_lists()  
    return render_template("lists.html", lists=my_lists)  

@app.route("/list/<int:list_id>")
def show_list(list_id):
    list = lists.get_list(list_id)
    items = lists.get_items(list_id)
    return render_template("list.html", list=list, items=items)

@app.route("/new_list", methods=["POST"])
def new_list():
    type = request.form["type"]
    content = request.form["content"]
    year = request.form["year"]
    title = request.form["title"]
    condition = request.form["condition"]
    creator = request.form["creator"]
    username = session["username"]

    list_id = lists.add_list(type, content, year, title, condition, creator, username)
    return redirect("/list/" + str(list_id))

@app.route("/new_item", methods=["POST"])
def new_item():
    content = request.form["content"]
    year = request.form["year"]
    title = request.form["type"]
    condition = request.form["condition"]
    creator = request.form["creator"]
    username = session["username"]
    list_id = request.form["list_id"]

    lists.add_item(content, username, list_id, year, title, condition)
    return redirect("/list/" + str(list_id))

@app.route("/edit/<int:item_id>", methods=["GET", "POST"])
def edit_item(item_id):
    item = lists.get_item(item_id)

    if request.method == "GET":
        return render_template("edit.html", item=item)

    if request.method == "POST":
        content = request.form["content"]
        year = request.form["year"]
        title = request.form["type"]
        condition = request.form["condition"]
        creator = request.form["creator"]
        lists.update_item(item["id"], content, year, title, condition)
        return redirect("/list/" + str(item["list_id"]))

@app.route("/remove/<int:item_id>", methods=["GET", "POST"])
def remove_item(item_id):
    item = lists.get_item(item_id)

    if request.method == "GET":
        return render_template("remove.html", item=item)

    if request.method == "POST":
        if "continue" in request.form:
            lists.remove_item(item["id"])
        return redirect("/list/" + str(item["list_id"]))

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        sql = "SELECT password_hash FROM users WHERE username = ?"
        password_hash = db.query(sql, [username])[0][0]

        if check_password_hash(password_hash, password):
            session["username"] = username
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

    return "tunnus luotu"
