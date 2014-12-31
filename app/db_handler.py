from flask import g
import sqlite3

def get_db():
	if not hasattr(g, 'sqlite_db'):
		g.sqlite_db = connect_db()
	return g.sqlite_db

def connect_db():
	rv = sqlite3.connect("/home/zulln/Desktop/aftonfont/www/database.db")
	rv.row_factory = sqlite3.Row
	return rv