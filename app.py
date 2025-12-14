import sqlite3
from flask import Flask, abort, redirect, render_template, request, session
import config
import items
import users
import messages
import re
import os
from werkzeug.utils import secure_filename
import datetime
import secrets

app = Flask(__name__)
app.secret_key = config.secret_key

app.config.from_pyfile('config.py')
app.config['PROFILE_PIC_FOLDER'] = os.path.join(app.root_path, app.config['PROFILE_PIC_FOLDER'])

os.makedirs(app.config['PROFILE_PIC_FOLDER'], exist_ok=True)

def check_login():
    if "user_id" not in session:
        abort(403)

def check_csrf():
    token = request.form.get("csrf_token")
    if not token or token != session.get("csrf_token"):
        abort(403)

@app.route("/")
def index():
    all_items = items.get_items()
    return render_template("index.html", items=all_items)

@app.route("/register")
def register():
    return render_template("register.html")

@app.route("/create", methods=["POST"])
def create():
    username = request.form["username"]
    password1 = request.form["password1"]
    password2 = request.form["password2"]
    if password1 != password2:
        return render_template("error.html", 
                            message="salasanat eivät ole samat",
                            background_color="#111",
                            text_color="#fff")

    try:
        users.create_user(username, password1)
    except sqlite3.IntegrityError:
        return render_template("error.html",
                            message="tunnus on jo varattu",
                            background_color="#111",
                            text_color="#fff")
    
    return render_template("message.html",
                        title="tunnus luotu",
                        message="tunnus on nyt luotu onnistuneesti.",
                        background_color="#111",
                        text_color="#fff")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")

    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        user_id = users.check_login(username, password)
        if user_id:
            session["user_id"] = user_id
            session["username"] = username
            session["csrf_token"] = secrets.token_hex(16)
            return redirect("/")
        else:
            return "väärä tunnus tai salasana"

@app.route("/show_item/<int:item_id>")
def show_item(item_id):
    item = items.get_item(item_id)
    if not item:
        abort(404)

    section = items.get_section(item['section_id'])
    condition = items.get_condition(item['condition_id'])

    classes = items.get_classes(item_id)
    return render_template("show_item.html", item=item, section=section, condition=condition, classes=classes)

@app.route("/find_item")
def find_item():
    query = request.args.get("query")
    if query:
        results = items.find_items(query)
    else:
        query = ""
        results = []
    return render_template("find_item.html", query=query, results=results)

@app.route("/new_item")
def new_item():
    check_login()
    sections = items.get_sections()
    conditions = items.get_conditions()

    section_groups = {}
    for s in sections:
        section_groups.setdefault(s["label"], []).append(s)
    return render_template("new_item.html", sections=section_groups, conditions=conditions)

@app.route("/edit_item/<int:item_id>")
def edit_item(item_id):
    check_login()
    item = items.get_item(item_id)
    if not item:
        abort(404)
    if item["user_id"] != session["user_id"]:
        abort(403)
    sections = items.get_sections()
    conditions = items.get_conditions()
    
    section_groups = {}
    for s in sections:
        section_groups.setdefault(s["label"], []).append(s)
    
    return render_template("edit_item.html", item=item, sections=section_groups, conditions=conditions)

@app.route("/remove_item/<int:item_id>", methods=["GET", "POST"])
def remove_item(item_id):
    check_login()
    item = items.get_item(item_id)
    if not item:
        abort(404)
    if item["user_id"] != session["user_id"]:
        abort(403)

    if request.method == "GET":
        return render_template("remove_item.html", item=item)

    if request.method == "POST":
        check_csrf()
        if "remove" in request.form:
            items.remove_item(item_id)
            return redirect("/")
        else:
            return redirect("/show_item/" + str(item_id))

@app.route("/create_item", methods=["POST"])
def create_item():
    check_login()
    check_csrf()
    title = request.form["title"]
    descr = request.form["descr"]
    price = request.form["price"]
    user_id = session["user_id"]
    section_id = request.form["section_id"]
    condition_id = request.form["condition_id"]

    sections = items.get_sections()
    conditions = items.get_conditions()

    if not any(section["id"] == int(section_id) for section in sections):
        return "valittu osio ei ole olemassa"

    if not any(condition["id"] == int(condition_id) for condition in conditions):
        return "valittu tila ei ole olemassa"

    if not title or len(title) > 50 or not descr or len(descr) > 1000:
        abort(403)
    if not re.search("^[1-9][0-9]{0,5}$", price):
        abort(403)

    items.add_item(title, descr, price, user_id, section_id, condition_id)
    return redirect("/")

@app.route("/update_item", methods=["POST"])
def update_item():
    check_login()
    check_csrf()
    item_id = request.form["item_id"]
    title = request.form["title"]
    descr = request.form["descr"]
    price = request.form["price"]
    section_id = request.form["section_id"]
    condition_id = request.form["condition_id"]

    item = items.get_item(item_id)
    if not item:
        abort(404)
    if item["user_id"] != session["user_id"]:
        abort(403)
    if not title or len(title) > 50 or not descr or len(descr) > 1000:
        abort(403)
    if not re.search("^[1-9][0-9]{0,5}$", price):
        abort(403)

    sections = items.get_sections()
    conditions = items.get_conditions()

    if not any(section["id"] == int(section_id) for section in sections):
        return "valittu osio ei ole olemassa"

    if not any(condition["id"] == int(condition_id) for condition in conditions):
        return "valittu tila ei ole olemassa"

    items.update_item(item_id, title, descr, price, section_id, condition_id)
    return redirect("/show_item/" + str(item_id))

@app.route("/messages")
def view_messages():
    check_login()
    user_id = session["user_id"]
    conversations = messages.get_conversations(user_id)
    return render_template("messages.html", conversations=conversations)

@app.route("/conversation/<int:receiver_id>")
def conversation(receiver_id):
    check_login()
    user_id = session["user_id"]
    item_id = request.args.get("item_id", type=int)
    
    if not item_id:
        item_id = messages.get_latest_item_id_for_conversation(user_id, receiver_id)
        if not item_id:
            abort(404, "Keskustelua ei löytynyt")
    
    conv = messages.get_conversation(user_id, receiver_id, item_id)
    if not conv:
        abort(404)
    
    return render_template("conversation.html",
                         messages=conv["messages"],
                         other_user=conv["other_user"],
                         item=conv["item"],
                         current_user_id=user_id)

@app.route("/send_message", methods=["POST"])
def send_message():
    check_login()
    check_csrf()

    sender_id = session["user_id"]
    receiver_id = request.form["receiver_id"]
    item_id = request.form.get("item_id")
    content = request.form["content"]
    
    if not content or len(content) > 1000:
        abort(403)
    messages.send_message(sender_id, receiver_id, item_id, content)
    return redirect(f"/conversation/{receiver_id}" + (f"?item_id={item_id}" if item_id else ""))

@app.route("/user/<int:user_id>")
def user_profile(user_id):
    user = users.get_user_profile(user_id)
    if not user:
        abort(404)
    items = users.get_user_items(user_id)

    user_dict = dict(user)
    user_dict['follower_count'] = users.get_follower_count(user_id)
    user_dict['following_count'] = users.get_following_count(user_id)

    return render_template("user.html", user=user_dict, user_items=items)

@app.route("/follow/<int:user_id>", methods=["POST"])
def follow(user_id):
    check_login()
    check_csrf()
    current_user = session["user_id"]
    if users.get_user_profile(user_id)['is_following']:
        users.unfollow_user(current_user, user_id)
    else:
        users.follow_user(current_user, user_id)

    user_profile_data = users.get_user_profile(user_id)

    return render_template("user.html", user=user_profile_data, user_items=users.get_user_items(user_id))

@app.route("/edit_profile")
def edit_profile():
    check_login()
    user_id = session["user_id"]
    user = users.get_user_profile(user_id)
    return render_template("edit_profile.html", current_user=user)

@app.route("/update_profile", methods=["POST"])
def update_profile():
    check_login()
    check_csrf()
    user_id = session["user_id"]
    
    # Käsittele profiilikuvan lataus
    if 'profile_pic' in request.files:
        file = request.files['profile_pic']
        if file.filename != '':
            if allowed_file(file.filename):
                filename = secure_filename(f"user_{user_id}_{file.filename}")
                file.save(os.path.join(app.config['PROFILE_PIC_FOLDER'], filename))
                users.update_profile_pic(user_id, filename)
    
    # Päivitä muut tiedot
    username = request.form["username"]
    bio = request.form.get("bio", "")
    location = request.form.get("location", "")
    
    # Päivitä salasana jos annettu
    current_password = request.form.get("current_password")
    new_password = request.form.get("new_password")
    confirm_password = request.form.get("confirm_password")
    
    if current_password and new_password and confirm_password:
        if new_password != confirm_password:
            return render_template("edit_profile.html", 
                                current_user=users.get_user_profile(user_id),
                                error="Uudet salasanat eivät täsmää")
        
        if not users.verify_password(user_id, current_password):
            return render_template("edit_profile.html", 
                                current_user=users.get_user_profile(user_id),
                                error="Nykyinen salasana on väärä")
        
        users.update_password(user_id, new_password)
    
    users.update_profile(user_id, username, bio, location)
    
    return redirect(f"/user/{user_id}")

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")