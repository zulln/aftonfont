from flask import render_template, redirect, request, g
from app import app
import aftonapi
from db_handler import get_db, connect_db
import sqlite3

@app.route("/")
def index():
	query = """
		SELECT size, checks, url FROM data ORDER BY id DESC LIMIT 1;
	"""

	db = get_db()
	cur = db.execute(query)
	data = cur.fetchall()[0]

	data = {
		"size"		: data["size"],
		"checks"	: data["checks"],
		"url"		: data["url"]
	}

	graph = aftonapi.graph("last_day", "all")

	return render_template('index.htm', data=data, graph=graph)

@app.route("/ta-bort", methods=["POST", "GET"])
def ta_bort():
	if request.method == "POST":
		mail = request.form["mail"]
		query = """
			DELETE FROM users WHERE mail = ?
		"""

		return render_template("tagit-bort.htm", mail=mail) #in flask we trust, and there should be no xss
	return render_template("ta-bort.htm")

@app.route("/prenumerera", methods=["POST", "GET"])
def prenumerera():
	if request.method == "POST":
		mail = request.form["mail"]
		size = request.form["size"]

		query = """
			INSERT OR REPLACE INTO users (id, mail, value, last_sent) 
			VALUES (coalesce((SELECT id FROM users WHERE mail=?),
             (SELECT max(id) FROM USERS) + 1), ?, ?, 0);
		"""

		db = get_db()
		db.execute(query, (mail, mail, size))
		db.commit()

		#it kinda goes against my nature but let's trust flasks automagic escape-function
		return render_template("prenumerera.htm", mail=mail, size=size)
	else:
		return redirect("/")

@app.route("/api/<path:mode>")
def api(mode):
	return aftonapi.parse(mode)

@app.route("/api/")
def api_docs():
	return render_template("api.htm")