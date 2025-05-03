import os
from flask import request, redirect, url_for, Flask, render_template
from models import Chore, db, Household

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///chorewheel.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chores", methods=["GET", "POST"])
def chores():
    # Ensure a household exists (for testing/demo)
    household = Household.query.first()
    if not household:
        household = Household(name="Default Household")
        db.session.add(household)
        db.session.commit()

    if request.method == "POST":
        description = request.form["description"]
        value = int(request.form["value"])
        new_chore = Chore(description=description, value=value, household_id=household.id)
        db.session.add(new_chore)
        db.session.commit()
        return redirect(url_for("chores"))

    all_chores = Chore.query.all()
    return render_template("chores.html", chores=all_chores)

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

