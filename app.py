import os
import datetime
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import DateTime

basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
app.config[ "SQLALCHEMY_DATABASE_URI" ] = os.environ.get("DATABASE_URL") or "sqlite:///" + os.path.join(basedir, "data.sqlite" )
app.config[ "SQLALCHEMY_TRACK_MODIFICATIONS" ] = False
db = SQLAlchemy(app)

def remote_addr():
	return request.remote_addr

def get_user_agent():
	return request.headers.get('User-Agent')

class Connection (db.Model):
	__tablename__ = "connections"
	id = db.Column(db.Integer, primary_key= True)
	created_date = db.Column(DateTime, default=datetime.datetime.utcnow)
	regi_ip = db.Column(db.String(24), default=remote_addr)
	user_agent = db.Column(db.String(200), default=get_user_agent)

@app.errorhandler(404)
def page_not_found (e):
	return "<h1>Page not found Error 404</h1>"


@app.errorhandler(500)
def internal_server_error (e):
	return "<h1>Internal Server Error 500</h1>"


@app.route("/")
def index ():
	connection = Connection()
	db.session.add(connection)
	db.session.commit()
	return render_template("index.html")


@app.route("/view")
def view():
	return render_template("view.html", values=Connection.query.all())


if __name__ == '__main__' :
	db.create_all()
	app.run(debug= True, port=5000, host='0.0.0.0')
	db.session.all()
