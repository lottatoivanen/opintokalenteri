import sqlite3
from flask import Flask
from flask import redirect, render_template, request, session, abort
from werkzeug.security import check_password_hash, generate_password_hash
import config
import os
import db
import entries
import user
from datetime import datetime

app = Flask(__name__)
app.secret_key = config.secret_key

def require_login():
    if "user_id" not in session:
        return redirect("/login")

@app.route("/")
def index():
    if "user_id" not in session:
        return render_template("index.html", all_entries=[])
    all_entries = entries.get_entries_by_user(session["user_id"])
    return render_template("index.html", all_entries=all_entries)

@app.route("/user/<username>")
def user_entries(username):
    require_login()
    u = user.get_user_by_username(username)
    if not u:
        return abort(404)
    e = entries.get_entries_by_user(u["id"])
    return render_template("show_user.html", user=u, entries=e)    

@app.route("/find_entry")
def find_entry():
    require_login()
    query = request.args.get("query")
    if query:
        results = entries.find_entry(query)
    else:
        query = ""
        results = []
    return render_template("find_entry.html", query=query, results=results)

@app.route("/entry/<int:entry_id>")
def show_entry(entry_id):
    require_login()
    entry = entries.get_entry(entry_id)
    if not entry:
        return abort(404)
    if entry["user_id"] != session["user_id"]:
        return abort(403)
    return render_template("show_entry.html", entry=entry)

@app.route("/new_entry")
def new_entry():
    require_login()
    return render_template("new_entry.html")

@app.route("/create_entry", methods=["GET", "POST"])
def create_entry():
    if request.method == "GET":
        return render_template("new_entry.html")
    require_login()
    title = request.form["title"]
    if not title or len(title) > 50:
        return abort(403)
    description = request.form["description"]
    if not description or len(description) > 1000:
        return abort(403)
    date = request.form["date"]
    try:
        datetime.strptime(date, "%Y-%m-%d")
    except (ValueError, TypeError):
        abort(403)
    user_id = session["user_id"]
    
    entries.add_entry(title, description, date, user_id)
    return redirect("/")

@app.route("/edit_entry/<int:entry_id>")
def edit_entry(entry_id):
    entry = entries.get_entry(entry_id)
    if not entry:
        return abort(404)
    if entry["user_id"] != session["user_id"]:
        return abort(403)
    return render_template("edit_entry.html", entry=entry)

@app.route("/edit_entry/<int:entry_id>", methods=["POST"])
def update_entry(entry_id):
    if "user_id" not in session:
        return redirect("/login")
    entry_id = request.form["entry_id"]
    entry = entries.get_entry(entry_id)
    if not entry:
        return abort(404)
    if entry["user_id"] != session["user_id"]:
        return abort(403)

    title = request.form["title"]
    if not title or len(title) > 50:
        return abort(403)
    description = request.form["description"]
    if not description or len(description) > 1000:
        return abort(403)
    date = request.form["date"]
    try:
        datetime.strptime(date, "%Y-%m-%d")
    except (ValueError, TypeError):
        abort(403)
    entries.update_entry(entry_id, title, description, date)
    return redirect("/entry/" + str(entry_id))

@app.route("/delete_entry/<int:entry_id>", methods=["GET", "POST"])
def delete_entry(entry_id):
    if "user_id" not in session:
        return redirect("/login")
    entry = entries.get_entry(entry_id)
    if not entry:
        return abort(404)
    if entry["user_id"] != session["user_id"]:
        return abort(403)
    if request.method == "GET":
        return render_template("delete_entry.html", entry=entry)
    if "delete" in request.form:
        entries.delete_entry(entry_id)
        return redirect("/")
    else:
        return redirect("/entry/" + str(entry_id))



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

    return redirect("/login")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        sql = "SELECT id, password_hash FROM users WHERE username = ?"
        result = db.query(sql, [username])[0]
        user_id = result["id"]
        password_hash = result["password_hash"]

        if check_password_hash(password_hash, password):
            session["user_id"] = user_id
            session["username"] = username
            return redirect("/")
        else:
            return "VIRHE: väärä tunnus tai salasana"

@app.route("/logout")
def logout():
    if "user_id" in session:
        del session["user_id"]
        del session["username"]
    return redirect("/")
