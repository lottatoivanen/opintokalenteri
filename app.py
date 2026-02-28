import sqlite3
from flask import Flask
from flask import redirect, render_template, request, session, abort, flash
import config
import db
import entries
import user
import courses
import comments
from datetime import datetime
import secrets

app = Flask(__name__)
app.secret_key = config.secret_key

def check_csrf():
    token_form = request.form.get("csrf_token")
    token_session = session.get("csrf_token")
    if token_form != token_session or not token_form or not token_session:
        abort(403)

def require_login():
    if "user_id" not in session:
        return redirect("/login")

@app.route("/")
def index():
    if "user_id" not in session:
        return render_template("index.html", all_entries=[], all_courses=[])
    all_entries = user.get_entries_by_user(session["user_id"])
    all_courses = user.get_courses_by_user(session["user_id"])
    all_tags = entries.get_all_tags()
    return render_template("index.html", all_entries=all_entries, all_courses=all_courses, all_tags=all_tags)

### entries ###

@app.route("/user/<username>")
def user_entries(username):
    require_login()
    u = user.get_user_by_username(username)
    if not u:
        return abort(404)
    e = user.get_entries_by_user(u["id"])
    c = user.get_courses_by_user(u["id"])
    all_tags = entries.get_all_tags()
    return render_template("show_user.html", user=u, entries=e, courses=c, all_tags=all_tags)    

@app.route("/find_entry")
def find_entry():
    require_login()
    query = request.args.get("query")
    if query:
        results = entries.find_entry_user(query)
        other_results = entries.find_entry_other_users(query)
    else:
        query = ""
        results = []
        other_results = []
    all_tags = entries.get_all_tags()
    return render_template("find_entry.html", query=query, results=results, other_results=other_results, all_tags=all_tags)

@app.route("/entry/<int:entry_id>")
def show_entry(entry_id):
    require_login()
    entry = entries.get_entry(entry_id)
    if not entry:
        return abort(404)
    tags = entries.get_tags(entry_id)
    all_tags = entries.get_all_tags()
    if "csrf_token" not in session:
        session["csrf_token"] = secrets.token_hex(16)
    entry_comments = comments.get_comments_entry(entry_id)
    return render_template("show_entry.html", entry=entry, owner=(entry["user_id"] == session["user_id"]), tags=tags, all_tags=all_tags, comments=entry_comments)

@app.route("/new_entry")
def new_entry():
    require_login()
    course_id = request.args.get("course_id")
    all_courses = user.get_courses_by_user(session["user_id"])
    all_tags = entries.get_all_tags()
    return render_template("new_entry.html", all_courses=all_courses, selected_course_id=course_id, all_tags=all_tags)

@app.route("/create_entry", methods=["GET", "POST"])
def create_entry():
    require_login()
    check_csrf()
    if request.method == "GET":
        course_id = request.args.get("course_id")
        all_courses = user.get_courses_by_user(session["user_id"])
        all_tags = entries.get_all_tags()
        return render_template("new_entry.html", all_courses=all_courses, selected_course_id=course_id, all_tags=all_tags)
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
    all_courses = user.get_courses_by_user(session["user_id"])
    if course_id and not any(course["id"] == course_id for course in all_courses):
        return abort(403)
    all_tags = entries.get_all_tags()
    tags = []
    for entry in request.form.getlist("tags"):
        if entry:
            parts = entry.split(":")
            if parts[0] not in all_tags or parts[1] not in all_tags[parts[0]]:
                return abort(403)
            tags.append((parts[0], parts[1]))
    tags = list(set(tags))
    entries.add_entry(title, description, date, user_id, course_id, tags)
    return redirect("/")

@app.route("/edit_entry/<int:entry_id>")
def edit_entry(entry_id):
    require_login()
    entry = entries.get_entry(entry_id)
    if not entry:
        return abort(404)
    if entry["user_id"] != session["user_id"]:
        return abort(403)
    all_tags = entries.get_all_tags()
    entry_tags = entries.get_tags(entry_id)
    all_courses = user.get_courses_by_user(session["user_id"])
    return render_template("edit_entry.html", entry=entry, all_courses=all_courses, all_tags=all_tags, entry_tags=entry_tags)

@app.route("/edit_entry/<int:entry_id>", methods=["POST"])
def update_entry(entry_id):
    require_login()
    check_csrf()
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
    all_courses = user.get_courses_by_user(session["user_id"])
    if course_id and not any(course["id"] == course_id for course in all_courses):
        return abort(403)
    all_tags = entries.get_all_tags()
    tags = []
    for entry in request.form.getlist("tags"):
        if entry:
            parts = entry.split(":")
            if parts[0] not in all_tags or parts[1] not in all_tags[parts[0]]:
                return abort(403)
            tags.append((parts[0], parts[1]))
    tags = list(set(tags))
    if "update" in request.form:
        entries.update_entry(entry_id, title, description, date, course_id, tags)
        return redirect("/entry/" + str(entry_id))
    else:
        return redirect("/entry/" + str(entry_id))

@app.route("/delete_entry/<int:entry_id>", methods=["GET", "POST"])
def delete_entry(entry_id):
    require_login()
    check_csrf()
    entry = entries.get_entry(entry_id)
    entry_tags = entries.get_tags(entry_id)
    if not entry:
        return abort(404)
    if entry["user_id"] != session["user_id"]:
        return abort(403)
    if request.method == "GET":
        return render_template("delete_entry.html", entry=entry, entry_tags=entry_tags)
    if "delete" in request.form:
        entries.delete_entry(entry_id)
        return redirect("/")
    else:
        return redirect("/entry/" + str(entry_id))

### courses ###

@app.route("/new_course")
def new_course():
    require_login()
    return render_template("new_course.html")

@app.route("/create_course", methods=["GET", "POST"])
def create_course():
    require_login()
    check_csrf()
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
    if "csrf_token" not in session:
        session["csrf_token"] = secrets.token_hex(16)
    course_entries = entries.get_entries_by_course(course_id)
    course_comments = comments.get_comments_course(course_id)
    return render_template("show_course.html", course=course, entries=course_entries, owner=(course["user_id"] == session["user_id"]), comments=course_comments)

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
    check_csrf()
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
    if "update" in request.form:
        courses.update_course(course_id, name, description)
        return redirect("/course/" + str(course_id))
    else:
        return redirect("/course/" + str(course_id))

@app.route("/delete_course/<int:course_id>", methods=["GET", "POST"])
def delete_course(course_id):
    require_login()
    check_csrf()
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

@app.route("/all_courses")
def all_courses():
    require_login()
    all_courses = user.get_all_courses_except_user(session["user_id"])
    return render_template("all_courses.html", all_courses=all_courses)

### comments ###

@app.route("/add_comment_entry/<int:entry_id>", methods=["POST"])
def add_comment_entry(entry_id):
    require_login()
    check_csrf()
    entry = entries.get_entry(entry_id)
    if not entry:
        return abort(404)
    comment = request.form["comment"]
    if not comment or len(comment) > 1000:
        return abort(403)
    user_id = session["user_id"]
    comments.add_comment_entry(entry_id, user_id, comment)
    return redirect("/entry/" + str(entry_id))

@app.route("/add_comment_course/<int:course_id>", methods=["POST"])
def add_comment_course(course_id):
    require_login()
    check_csrf()
    course = courses.get_course(course_id)
    if not course:
        return abort(404)
    comment = request.form["comment"]
    if not comment or len(comment) > 1000:
        return abort(403)
    user_id = session["user_id"]
    comments.add_comment_course(course_id, user_id, comment)
    return redirect("/course/" + str(course_id))

@app.route("/delete_comment/<int:comment_id>", methods=["POST"])
def delete_comment(comment_id):
    require_login()
    check_csrf()
    comment = comments.get_comment(comment_id)
    if not comment:
        return abort(404)
    if comment["user_id"] != session["user_id"]:
        return abort(403)
    entry_id = comment["entry_id"]
    comments.delete_comment(comment_id)
    if comment["entry_id"]:
        return redirect("/entry/" + str(entry_id))
    else:
        course_id = comment["course_id"]
        return redirect("/course/" + str(course_id))

### sign up, login, logout ###

@app.route("/register")
def register():
    session["csrf_token"] = secrets.token_hex(16)
    return render_template("register.html")

@app.route("/create", methods=["POST"])
def create():
    check_csrf()
    username = request.form["username"]
    password1 = request.form["password1"]
    password2 = request.form["password2"]
    if password1 != password2:
        flash("VIRHE: salasanat eivät ole samat", "error")
        return redirect("/register")
    elif len(username) < 3 or len(username) > 20:
        flash("VIRHE: käyttäjätunnuksen tulee olla 3-20 merkkiä pitkä", "error")
        return redirect("/register")
    elif len(password1) < 6 or len(password1) > 100:
        flash("VIRHE: salasanan tulee olla 6-100 merkkiä pitkä", "error")
        return redirect("/register")
    try:
        user.create_user(username, password1)
    except sqlite3.IntegrityError:
        flash("VIRHE: tunnus on jo varattu", "error")
        return redirect("/register")
    flash("Rekisteröityminen onnistui! Voit nyt kirjautua sisään.", "success")
    return redirect("/login")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        session["csrf_token"] = secrets.token_hex(16)
        return render_template("login.html")
    if request.method == "POST":
        check_csrf()
        username = request.form["username"]
        password = request.form["password"]

        user_id = user.check_login(username, password)
        if user_id:
            session["user_id"] = user_id
            session["username"] = username
            return redirect("/")
        else:
            flash("VIRHE: virheellinen tunnus tai salasana", "error")
            return redirect("/login")

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")
