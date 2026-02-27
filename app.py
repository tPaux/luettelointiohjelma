import sqlite3
from flask import Flask, redirect, render_template, request, session, abort, make_response
from werkzeug.security import generate_password_hash, check_password_hash
import db
import config
import lists
import sys
import users
import math
import time
import secrets
from flask import g

app = Flask(__name__)
app.secret_key = config.secret_key

@app.route("/")
@app.route("/<int:page>")
def index(page=1):
    page_size = 10
    items_count = lists.items_count()
    page_count = math.ceil(items_count / page_size)
    page_count = max(page_count, 1)

    if page < 1:
        return redirect("/1")
    if page > page_count:
        return redirect("/" + str(page_count))
    items = lists.get_items(page, page_size)

    return render_template("index.html", items=items, page=page, page_count=page_count)


@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "GET":
        return render_template("login.html")
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        items = lists.get_items(1, 10)
        sql = "SELECT id, password_hash FROM users WHERE username = ?"
        rows = db.query(sql, [username])
        if not rows:
            return render_template("index.html", items=items, page=page, page_count=page_count, error="Väärä tunnus tai salasana")
        row = rows[0]
        user_id = row[0]
        password_hash = row[1]

        if check_password_hash(password_hash, password):
            session["username"] = username
            session["user_id"] = user_id
            session["csrf_token"] = secrets.token_hex(16)

            return redirect("/")

        else:
            return render_template("index.html", items=items, page=page, page_count=page_count, error="Väärä tunnus tai salasana")

def check_csrf():
    if request.form["csrf_token"] != session["csrf_token"]:
        abort(403)

@app.route("/logout")
def logout():

    require_login()
    session.clear()
    return redirect("/")

@app.route("/create", methods=["POST"])
def create():

    username = request.form["username"]
    password1 = request.form["password1"]
    password2 = request.form["password2"]
    items = lists.get_items(1, 10)
    if password1 != password2:
        return render_template("index.html", error="Salasanat eivät täsmää", items=items)
    password_hash = generate_password_hash(password1)

    try:
        sql = "INSERT INTO users (username, password_hash) VALUES (?, ?)"
        db.execute(sql, [username, password_hash])
    except (sqlite3.IntegrityError, sqlite3.OperationalError) as err:
        return render_template("index.html", items=items, page=page, page_count=page_count, error="Tunnus on jo varattu")


    return redirect("/")



@app.route("/search")
@app.route("/search/<int:page>")
def search(page=1):
    q = request.args.get("q")
    page_size = 10
    items_count = lists.search_count(q)
    page_count = math.ceil(items_count / page_size)
    items = lists.search(q)

    return render_template("index.html", items=items, page=page, page_count=page_count, q=q)


@app.route("/new_item", methods=["POST"])
def new_item():
    require_login()
    check_csrf()

    ttyype = request.form["ttyype"]
    author = request.form["author"]
    title = request.form["title"]
    year = request.form["year"]
    creator = request.form["creator"]
    condition = request.form["condition"]
    content = request.form["content"]
    user_id = session["user_id"]

    if not ttyype or not author or not title or not condition or len(author) > 50 or len(author) < 2 or len(title) > 50 or len(title) < 2 or len(year) > 8 or len(year) < 1 or len(creator) > 50 or len(content) > 1000 or len(content) < 10 or not condition:
        abort(403)

    try:
        item_id = lists.add_item(ttyype, author, title, year, creator, condition, content, user_id)
    except sqlite3.IntegrityError:
        abort(403)

    return redirect("/item/" + str(item_id))

@app.route("/item/<int:item_id>")
def show_item(item_id):
    item = lists.get_item(item_id)
    if not item:
            abort(404)
    items = lists.get_items(1, 10)
    return render_template("item.html", item=item, items=items)

@app.route("/edit/<int:item_id>", methods=["GET", "POST"])
def edit_item(item_id):
    require_login()
    #check_csrf()
    item = lists.get_item(item_id)

    if item is None:
        abort(404)
    if item["user_id"] != session["user_id"]:
        abort(403)
    if request.method == "GET":
        items = lists.get_items(1, 10)
        return render_template("edit.html", item=item, items=items)
    if request.method == "POST":
        ttyype = request.form["ttyype"]
        author = request.form["author"]
        title = request.form["title"]
        year = request.form["year"]
        creator = request.form["creator"]
        condition = request.form["condition"]
        content = request.form["content"]
        lists.update_item(item_id, ttyype, author, title, year, creator, condition, content)

        return redirect("/")

@app.route("/remove/<int:item_id>", methods=["GET", "POST"])
def remove_item(item_id):
    require_login()
    item = lists.get_item(item_id)

    if request.method == "GET":
        return render_template("remove.html", item=item)
    if request.method == "POST":
        if "continue" in request.form:
            lists.remove_item(item_id)
        return redirect("/")

@app.route("/user/<int:user_id>")
def show_user(user_id):
    user = users.get_user(user_id)
    if not user:
        abort(404)
    items = users.get_items(user_id)
    items = sorted(items, key=lambda x: x["sent_at"])
    return render_template("user.html", user=user, items=items, q=user_id)

def require_login():
    if "user_id" not in session:
        abort(403)

@app.route("/add_image", methods=["GET", "POST"])
def add_image():
    require_login()

    if request.method == "GET":
        return render_template("add_image.html")

    file = request.files["image"]
    if not file.filename.endswith(".jpg"):
        return "VIRHE: väärä tiedostomuoto"

    image = file.read()

    print("Tallennettavan kuvan koko:", len(image))
    if len(image) > 100 * 1024:
        return "VIRHE: liian suuri kuva"

    user_id = session["user_id"]
    users.update_image(user_id, image)
    return redirect("/user/" + str(user_id))


@app.route("/image/<int:user_id>")
def show_image(user_id):
    image = users.get_image(user_id)
    if not image:
        abort(404)

    response = make_response(image)
    response.headers.set("Content-Type", "image/jpeg")
    return response

@app.before_request
def before_request():
    g.start_time = time.time()

@app.after_request
def after_request(response):
    elapsed_time = round(time.time() - g.start_time, 2)
    print("elapsed time:", elapsed_time, "s")
    return response



