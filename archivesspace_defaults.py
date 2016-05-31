from vandura.shared.scripts.archivesspace_authenticate import authenticate
from vandura.config import aspace_credentials

import requests
import time
import json
import getpass
from pprint import pprint

def make_note_multipart(note_type, note_content):
	note_multipart = {"type":note_type,
					"jsonmodel_type":"note_multipart",
					"publish":True,
					"subnotes":[{
						"content":note_content,
						"jsonmodel_type":"note_text",
						"publish":True
					}]}
	return note_multipart

def resource_template():
	resource_template = {
					"record_type":"resource", 
					"defaults":{
						"title":"[Enter a title]",
						"publish":True,
						"suppressed":False,
						"level":"collection",
						"language":"eng",
						"finding_aid_title":"Finding aid for the [collection title]",
						"notes":[
							make_note_multipart("accessrestrict","This collection is open for research"),
							make_note_multipart("bioghist", "Enter a biographical note"),
							make_note_multipart("accruals", "REMOVE ONE:\r\nNo accruals expected\r\nAccruals expected"),
							make_note_multipart("prefercite","[item],[box],[folder],[collection], etc.")]
						}
					}

	return json.dumps(resource_template)

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

	mhc_classification = {'title':'Michigan Historical Collections','identifier':'MHC'}
	uarp_classification = {'title':'University Archives','identifier':'UA'}
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
		'defaults':{'publish':True, 'default_values':True}
		}

	repo_preferences_post = s.post(aspace_url + '/repositories/2/preferences',data=json.dumps(repo_preferences)).json()
	print repo_preferences_post

	resource_template_post = s.post("{}/repositories/2/default_values/resource".format(aspace_url), data=resource_template()).json()
	print resource_template_post

	s.post("{}/logout".format(aspace_url))


def main():
	aspace_url, username, password = aspace_credentials()
	post_defaults(aspace_url, username, password)

if __name__ == "__main__":
	main()