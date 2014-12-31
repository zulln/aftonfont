aftonfont
=========
Install flask: http://markjberger.com/flask-with-virtualenv-uwsgi-nginx/
Put all the files in there, should be kinda self-explained.

Create "database.db" from schema.sql by running; "sqlite3 database.db < schema.sql".
Create a cron-job that runs main.py every 5 minutes or so.

Create secret.py with credentials for mailgun, like this:
`def getData():
  return ("url", "api-key")
`
