import os
from flask import request, redirect, url_for, Flask, render_template, session
from models import Chore, db, Household, User

app = Flask(__name__)
app.secret_key = "supersecretkey"  # replace with env var later
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///chorewheel.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chores", methods=["GET", "POST"])
def chores():
    if "user_id" not in session:
        return redirect(url_for("login"))

    household = Household.query.first()
    if not household:
        household = Household(name="Default Household")
        db.session.add(household)
        db.session.commit()

    if request.method == "POST":
        description = request.form["description"]
        value = int(request.form["value"])
        assigned_user_id = request.form.get("assigned_user_id")
        if assigned_user_id == "none":
            assigned_user_id = None
        new_chore = Chore(
            description=description,
            value=value,
            assigned_user_id=assigned_user_id,
            household_id=household.id
        )
        db.session.add(new_chore)
        db.session.commit()
        return redirect(url_for("chores"))

    all_chores = Chore.query.all()
    all_users = User.query.filter_by(household_id=household.id).all()
    return render_template("chores.html", chores=all_chores, users=all_users)


@app.route("/complete/<int:chore_id>", methods=["POST"])
def complete_chore(chore_id):
    chore = Chore.query.get_or_404(chore_id)
    chore.is_complete = True
    db.session.commit()
    return redirect(url_for("chores"))

@app.route("/add-users")
def add_users():
    household = Household.query.first()
    if not household:
        household = Household(name="Default Household")
        db.session.add(household)
        db.session.commit()

    if not User.query.first():
        users = [
            User(name="Alice", household_id=household.id),
            User(name="Bob", household_id=household.id),
            User(name="Charlie", household_id=household.id),
        ]
        db.session.add_all(users)
        db.session.commit()
    return redirect(url_for("chores"))

@app.route("/login", methods=["GET", "POST"])
def login():
    household = Household.query.first()
    if not household:
        household = Household(name="Default Household")
        db.session.add(household)
        db.session.commit()

    users = User.query.filter_by(household_id=household.id).all()

    if request.method == "POST":
        selected_user = request.form.get("user_id")
        if selected_user:
            session["user_id"] = int(selected_user)
            return redirect(url_for("chores"))

        new_user_name = request.form.get("new_user_name")
        if new_user_name:
            new_user = User(name=new_user_name, household_id=household.id)
            db.session.add(new_user)
            db.session.commit()
            session["user_id"] = new_user.id
            return redirect(url_for("chores"))

    return render_template("login.html", users=users)


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

