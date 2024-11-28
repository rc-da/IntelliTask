from flask import Flask, session, render_template
from flask_cors import CORS
from apscheduler.schedulers.background import BackgroundScheduler
from controller.user_controller import user_bp
from controller.reminder_controller import reminder_bp
from controller.location_controller import location_bp
from reminder.reminder import fetch_all_reminders
from reminder.reminder_trigger import check_reminders_trigger

app = Flask(__name__)
CORS(app)

app.secret_key = "\x1f\xeb\x00\xa3!+\xecJqi\xe0\xcf\x81\xbd\xfc\xdd\xc4=>kx\x1cq\xd9"



fetch_all_reminders()

scheduler = BackgroundScheduler()
scheduler.add_job(check_reminders_trigger, 'interval', seconds=60)
scheduler.start()

@app.route("/home")
def homepage():
    user_id = session.get("user_id", None)
    return render_template("index.html", user_id = user_id)

@app.route("/reminder")
def reminder():
    user_id = session.get("user_id", None)
    return render_template("reminder.html", user_id = user_id)

@app.route("/map")
def map():
    user_id = session.get("user_id", None)
    return render_template("map.html",user_id = session.get("user_id", None))

@app.route("/authentication")
def auth():
    return render_template("authentication.html")

app.register_blueprint(user_bp, url_prefix="/user")
app.register_blueprint(reminder_bp, url_prefix="/reminder")
app.register_blueprint(location_bp, url_prefix="/location")

if __name__ == '__main__':
    app.run(debug=True)
