import json
import requests

def authenticate(aspace_url, username, password, expiring="true"):
	s = requests.session()
	auth = s.post("{0}/users/{1}/login?password={2}&expiring={3}".format(aspace_url, username, password, expiring)).json()
	session = auth["session"]
	s.headers.update({"X-ArchivesSpace-Session":session})
	return s