import requests, re

def get_data():
	r = requests.get("http://aftonbladet.se")
	if r.status_code != 200:
		exit("aftonbladet doesn't like me")

	data 	= r.text.encode("utf-8")
	check	= data.count("<span class=\"abSymbBo\"></span>")

	#### .... ###
	
	r = requests.get("http://www.aftonfonten.se")
	if r.status_code != 200:
		exit("mr. font fucked up.")

	data 	= r.text.encode("utf-8")
	size 	= int(re.search(r"\"\>(.+?) \<span\>px", data).group(1))
	url  	= re.search(r"<h1><a href=\"(.+?)\"", data).group(1)

	return (size, url, check)