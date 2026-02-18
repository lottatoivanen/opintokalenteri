import sqlite3
from flask import Flask
from flask import redirect, render_template, request, session, abort
import config
import db
import entries
import user
import courses
from datetime import datetime

app = Flask(__name__)
app.secret_key = config.secret_key

def require_login():
    if "user_id" not in session:
        return redirect("/login")

@app.route("/")
def index():
    if "user_id" not in session:
        return render_template("index.html", all_entries=[], all_courses=[])
    all_entries = user.get_entries_by_user(session["user_id"])
    all_courses = user.get_courses_by_user(session["user_id"])
    return render_template("index.html", all_entries=all_entries, all_courses=all_courses)

### merkinnät ###

@app.route("/user/<username>")
def user_entries(username):
    require_login()
    u = user.get_user_by_username(username)
    if not u:
        return abort(404)
    e = user.get_entries_by_user(u["id"])
    c = user.get_courses_by_user(u["id"])
    return render_template("show_user.html", user=u, entries=e, courses=c)    

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
    course_id = request.args.get("course_id")
    all_courses = user.get_courses_by_user(session["user_id"])
    return render_template("new_entry.html", all_courses=all_courses, selected_course_id=course_id)

@app.route("/create_entry", methods=["GET", "POST"])
def create_entry():
    require_login()
    if request.method == "GET":
        course_id = request.args.get("course_id")
        all_courses = user.get_courses_by_user(session["user_id"])
        return render_template("new_entry.html", all_courses=all_courses, selected_course_id=course_id)
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
    course_id = request.form.get("course_id")
    course_id = int(course_id) if course_id else None
    entries.add_entry(title, description, date, user_id, course_id)
    return redirect("/")

@app.route("/edit_entry/<int:entry_id>")
def edit_entry(entry_id):
    require_login()
    entry = entries.get_entry(entry_id)
    if not entry:
        return abort(404)
    if entry["user_id"] != session["user_id"]:
        return abort(403)
    all_courses = user.get_courses_by_user(session["user_id"])
    return render_template("edit_entry.html", entry=entry, all_courses=all_courses)

@app.route("/edit_entry/<int:entry_id>", methods=["POST"])
def update_entry(entry_id):
    require_login()
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
    course_id = request.form.get("course_id")
    course_id = int(course_id) if course_id else None
    entries.update_entry(entry_id, title, description, date, course_id)
    return redirect("/entry/" + str(entry_id))

@app.route("/delete_entry/<int:entry_id>", methods=["GET", "POST"])
def delete_entry(entry_id):
    require_login()
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

### kurssit ###

@app.route("/new_course")
def new_course():
    require_login()
    return render_template("new_course.html")

@app.route("/create_course", methods=["GET", "POST"])
def create_course():
    require_login()
    if request.method == "GET":
        return render_template("new_course.html")
    name = request.form["name"]
    if not name or len(name) > 50:
        return abort(403)
    description = request.form["description"]
    if len(description) > 1000:
        return abort(403)
    user_id = session["user_id"]
    courses.add_course(name, description, user_id)
    return redirect("/")

@app.route("/course/<int:course_id>")
def show_course(course_id):
    require_login()
    course = courses.get_course(course_id)
    if not course:
        return abort(404)
    if course["user_id"] != session["user_id"]:
        return abort(403)
    course_entries = entries.get_entries_by_course(course_id)
    return render_template("show_course.html", course=course, entries=course_entries)

@app.route("/edit_course/<int:course_id>")
def edit_course(course_id):
    require_login()
    course = courses.get_course(course_id)
    if not course:
        return abort(404)
    return render_template("edit_course.html", course=course)

@app.route("/edit_course/<int:course_id>", methods=["POST"])
def update_course(course_id):
    require_login()
    course_id = request.form["course_id"]
    course = courses.get_course(course_id)
    if not course:
        return abort(404)
    if course["user_id"] != session["user_id"]:
        return abort(403)

    name = request.form["name"]
    if not name or len(name) > 50:
        return abort(403)
    description = request.form["description"]
    if len(description) > 1000:
        return abort(403) 
    courses.update_course(course_id, name, description)
    return redirect("/course/" + str(course_id))

@app.route("/delete_course/<int:course_id>", methods=["GET", "POST"])
def delete_course(course_id):
    require_login()
    course = courses.get_course(course_id)
    if not course:
        return abort(404)
    if course["user_id"] != session["user_id"]:
        return abort(403)
    if request.method == "GET":
        return render_template("delete_course.html", course=course)
    if "delete" in request.form:
        courses.delete_course(course_id)
        return redirect("/")
    else:
        return redirect("/course/" + str(course_id))

### kirjautuminen ja rekisteröityminen ###

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
    try:
        user.create_user(username, password1)
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

        user_id = user.check_login(username, password)
        if user_id:
            session["user_id"] = user_id
            session["username"] = username
            return redirect("/")
        else:
            return "VIRHE: virheellinen tunnus tai salasana"

@app.route("/logout")
def logout():
    if "user_id" in session:
        del session["user_id"]
        del session["username"]
    return redirect("/")
