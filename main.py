import afton
import time, sqlite3, requests
import secret

con = sqlite3.connect("database.db")
cur = con.cursor()

def send_emails(emails, size):
	subject	= "Aftonfont-alert! %dpx" % size 
	msg 	= "Chock!! Hela %dpx!!!" % size

	url, key = secret.getData()

	r = requests.post(
		url,
		auth=("api", key),
		data={"from": "Aftonfont <aftonfont@zulln.se>",
			"to"		: "a-lot-of-people@zulln.se",
			"bcc"		: emails,
			"subject"	: subject,
			"text"		: msg })

	print r.text
	print emails

def get_emails(size, now):
	last_day = now - 60 * 60 * 24
	
	query = """
		SELECT mail
		FROM users
		WHERE value <= ?
		AND last_sent <= ?
	"""
	cur.execute(query, (size, last_day))
	data = cur.fetchall()

	rows = []
	for x in range(len(data)):
		rows.append(data[x][0])

	query = """
		UPDATE users
		SET last_sent = ?
		WHERE last_sent <= ?
	"""
	cur.execute(query, (now, last_day))
	con.commit()

	return rows

def save_data(size, url, checks, time):
	query = """
		INSERT INTO data(time, size, url, checks)
		VALUES(?, ?, ?, ?)
	"""
	cur.execute(query, (time, size, url, checks))
	con.commit()

if __name__ == "__main__":
	now = time.time()
	size, url, checks	= afton.get_data()
	emails 				= get_emails(size, now)
	save_data(size, url, checks, now)
	con.close()
	if len(emails) > 0:
		send_emails(emails, size)