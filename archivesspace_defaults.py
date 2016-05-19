from vandura.shared.scripts.archivesspace_authenticate import authenticate
from vandura.config import aspace_credentials

import requests
import time
import json
import getpass
from pprint import pprint

def add_enum_values(session, aspace_url, enum_set_id, new_values_to_add):
		enum_address = aspace_url + '/config/enumerations/{}'.format(enum_set_id)
		existing_enums_json = session.get(enum_address).json()
		unique_values = [value for value in new_values_to_add if value not in existing_enums_json["values"]]
		existing_enums_json["values"].extend(unique_values)
		print(session.post(enum_address, data=json.dumps(existing_enums_json)).json())

def post_defaults(aspace_url, username, password):
	s = authenticate(aspace_url, username, password)
	s.headers.update({"Content-type":"application/json"})

	bhl_repo = {
			'name':'Bentley Historical Library',
			'org_code':'MiU-H',
			'repo_code':'BHL',
			'parent_institution_name':'University of Michigan'
			}

	post_repo = s.post(aspace_url + '/repositories',data=json.dumps(bhl_repo)).json()
	print post_repo

	'''
	base_profile = {
		'name':'',
		'extent_dimension':'height',
		'dimension_units':'inches',
		'height':'0',
		'width':'0',
		'depth':'0'
	}

	profile_names = ['box','folder','volume','reel','map-case','panel','sound-disc','tube','item','object','bundle']

	for profile_name in profile_names:
		container_profile = base_profile
		container_profile['name'] = profile_name
		profile_post = requests.post(aspace_url + '/container_profiles',headers=headers,data=json.dumps(container_profile)).json()
		print profile_post
	'''

	mhc_classification = {'title':'Michigan Historical Collections','identifier':'MHC'}
	uarp_classification = {'title':'University Archives and Records Program','identifier':'UARP'}
	faculty_classification = {'title':'Faculty Papers', 'identifier':'Faculty'}
	rcs_classification = {'title':'Records Center Storage','identifier':'RCS'}

	for classification in [mhc_classification, uarp_classification, faculty_classification, rcs_classification]: 
		classification_post = s.post(aspace_url + '/repositories/2/classifications',data=json.dumps(classification)).json()
		print classification_post
		
	add_enum_values(s, aspace_url, 23, ['lcnaf', 'lctgm', 'aacr2', 'lcgft', 'ftamc', 'fast'])  # subject sources
	add_enum_values(s, aspace_url, 4, ['lcnaf'])  # name sources
	add_enum_values(s, aspace_url, 55, ["on file", "pending", "sent", "n/a", "other"])  # user defined enum 1 values (gift agreement status)
	add_enum_values(s, aspace_url, 14, ["TB"]) # extent

	repo_preferences = {
		'repository':{'ref':'/repositories/2'},
		'defaults':{'publish':True}
		}

	repo_preferences_post = s.post(aspace_url + '/repositories/2/preferences',data=json.dumps(repo_preferences)).json()
	print repo_preferences_post


def main():
	aspace_url, username, password = aspace_credentials()
	post_defaults(aspace_url, username, password)

if __name__ == "__main__":
	main()