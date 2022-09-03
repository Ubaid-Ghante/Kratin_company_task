from flask import Flask, request, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_manager, login_user, UserMixin, current_user, logout_user
from flask_mail import Mail, Message
from flask_login.utils import login_required, logout_user
import random

app = Flask(__name__)

app.secret_key = "UBAIDAKHTARGHANTE"
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///Kratin.db'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
login_manager = LoginManager(app)

app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_PORT"] = 465
app.config["MAIL_USERNAME"] = "feedbackbymail00@gmail.com"
app.config["MAIL_PASSWORD"] = "8999650554"
app.config["MAIL_USE_TLS"] = False
app.config["MAIL_USE_SSL"] = True
mail = Mail(app)


@login_manager.user_loader
def load_user(user_id):
    return UserData.query.get(int(user_id))

db = SQLAlchemy(app)


class UserData(db.Model, UserMixin):
    __tablename__ = "Users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(25), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)


@app.route("/")
def home_page():
    return render_template("home.html")


@app.route("/main", methods=["GET", "POST"])
def main_page():
    if request.method == "POST":
        medicineData = ["Calpol", "Humira", "Entyvio","Paracetamol","wincold","Diclowin","Disprin","Acilok","Omeprazole","Rabiprazole","Brufen","Ciprobid","Cefaxime","Amoxicillin","Salbutamol","Cetrizine","Ofloxacin"]

        return render_template("main.html", medicineData=random.sample(medicineData, 4))

    return render_template("main.html")


@app.route("/signup", methods=["GET", "POST"])
def signup_user():
    if request.method == "POST":
        user_name = request.form["username"]
        user_password = request.form["password"]

        user_to_register = UserData(username=user_name, password=user_password)
        try:
            db.session.add(user_to_register)
            db.session.commit()
        except:
            return "Username exists!"

        login_user(user_to_register)
        return redirect(url_for("main_page"))


    return render_template("signup.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method=="POST":
        input_user_name = request.form["username"]
        input_user_password = request.form["password"]

        attempt_user = UserData.query.filter_by(username=input_user_name).first()
        if attempt_user.password == input_user_password:
            login_user(attempt_user)
            return redirect(url_for("main_page"))
            
        return "Invalid Login Credentials."
        

    return render_template("login.html")


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("home_page"))


@app.route("/mail")
def send_mail():
    msg = Message(subject=f"Hello Ubaid", recipients=[
                    "2019bcs043@sggs.ac.in", "2019bcs009@sggs.ac.in"], body=f"Amaan Khan", sender="aman@gmail.com")

    mail.send(msg)


if __name__ == "__main__":
    app.run(debug=True, port=80)