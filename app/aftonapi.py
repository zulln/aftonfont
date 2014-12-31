from flask import jsonify, g
from db_handler import get_db, connect_db
import sqlite3
import time

def get_db():
	if not hasattr(g, 'sqlite_db'):
		g.sqlite_db = connect_db()
	return g.sqlite_db

def connect_db():
	rv = sqlite3.connect("database.db")
	rv.row_factory = sqlite3.Row
	return rv

def whenparser(when):
	if when == "last_day":
		now = time.time()
		when = {
			"first" : (now - 60 * 60 * 24),
			"last"	: now
		}
	else:
		when = {
			"first" : when.split("-")[0],
			"last"	: when.split("-")[1]
		}

	if when["first"] > when["last"]:
		return error("Last must be grater than first.")

	return when

def parse(mode):
	method = mode.split("/")[0]

	if "/" in mode:
		when = whenparser(mode.split("/")[1])
	else:
		when = {}

	if method == "now":
		return now()
	elif method == "all":
		return all(when)
	elif method == "c3_all":
		return graph_all(when)
	else:
		return error("Invalid method: %s" % method)

def now():
	query = """
		SELECT size, checks, url FROM data ORDER BY id DESC LIMIT 1;
	"""
	db = get_db()
	cur = db.execute(query)
	data = cur.fetchall()[0]
	
	return jsonify(size = data["size"],
		checks = data["checks"],
		url = data["url"])

def all(when, graph = False):
	if not when:
		return error("When does not exist, fucked up query.")

	query = """
		SELECT size, checks, url, time FROM data WHERE time >= ? AND time <= ?
	"""
	db = get_db()
	cur = db.execute(query, (when["first"], when["last"]) )
	db_data = cur.fetchall()

	if len(db_data) <= 0:
		return error("No data")

	data = {
		"size" : [],
		"checks" : [],
		"url"	: [],
		"time" : []
	}

	for x in range(len(db_data)):
		for y in ["size", "checks", "url", "time"]:
			data[y].append(db_data[x-1][y])

	if graph:
		return data

	return jsonify(
		size	= data["size"],
		checks	= data["checks"],
		url		= data["url"],
		time	= data["time"]
	)

def graph(when, method):
	when = whenparser(when)
	if method == "all":
		data = all(when, True)

	bockar 	= ["Bockar"]	+ data["checks"]
	pixlar 	= ["Pixlar"]	+ data["size"]
	
	time = "[\"time\""
	for entry in data["time"]:
		time += ", new Date(%d)" % entry
	time += "]"

	graph_html = """
		<script>
			var chart = c3.generate({
				data: {
					x: "time",
					columns:[
						%s,
						%s,
						%s
					]
				}
			})
		</script>
	""" % (time, pixlar, bockar)

	return graph_html

def error(msg):
	return "Error: %s" % msg