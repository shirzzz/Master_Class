import flask.logging
from flask import Flask, render_template, session, redirect, request, jsonify

from db.insert_tables import insert_student_preference
from db.query_tables import login_lookup_students, get_students, get_connection
from students_to_classes_with_DB import run_algorithm

app = Flask(__name__)
app.secret_key = 'skibidi'


@app.route('/')
def welcome():
    return render_template("welcome.html")


@app.route('/login/student', methods=["GET"])
def login_student_get():
    return render_template("student_login.html", login_failed=False)


@app.route('/login/student', methods=["POST"])
def login_student_post():
    if session.get("logged_in", False):
        return redirect(f"/home/{session['user_type']}")

    session.clear()
    user_id = request.form.get("user-id")
    password = request.form.get("password")
    if is_valid_student_login(user_id, password):
        session["logged_in"] = True
        session["user_type"] = "student"
        session["id"] = user_id
        return redirect(f"/home/student")
    else:
        return render_template("student_login.html", login_failed=True)


def is_valid_student_login(user_id, password):
    result = login_lookup_students(user_id)
    if result is None:
        return False
    return result["password"] == password


@app.route("/home/student")
def home_student():
    return render_template("student_friends.html")


@app.route("/api/search_students_by_name", methods=["GET"])
def search_students_by_name_api():
    return jsonify({
        "success": True,
        "results": search_students(request.args.get("query_string") or "")
    })


def search_students(query):
    return [
        {
            "id": res["student_id"],
            "name": res["student_name"]
        } for res in get_students(query, session["id"])
    ]

@app.route("/api/add_friend", methods=["POST"])
def add_friend():
    if not session.get("logged_in", False):
        return {
            "success": False
        }
    if not session["user_type"] == "student":
        return {
            "success": False
        }
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    insert_student_preference(cursor, session["id"], request.form["friend_id"])
    return {
        "success": True
    }


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


@app.route("/match", methods=["POST"])
def match_page():
    results = run_algorithm(int(request.form["class_count"]))
    classes = list()
    for i, (class_list, score) in enumerate(zip(*results)):
        class_with_names = list()
        for student_id in class_list:
            student_name = get_student_name(student_id)
            class_with_names.append({"id": student_id, "name": student_name})
        classes.append((i+1, class_with_names, int(score * 100)))
    return render_template("results.html", results=classes)


def get_student_name(student_id):
    return login_lookup_students(student_id)["student_name"]


@app.route('/login/teacher', methods=["GET"])
def login_teacher_get():
    return render_template("teacher_login.html")


@app.route('/login/teacher', methods=["POST"])
def login_teacher_post():
    session["logged_in"] = True
    session["user_type"] = "teacher"
    return redirect("/home/teacher")


@app.route('/home/teacher')
def home_teacher():
    return render_template("teacher_preferences.html")


if __name__ == "__main__":
    app.run(debug=True)
