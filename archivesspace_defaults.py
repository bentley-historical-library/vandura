from vandura.shared.scripts.archivesspace_authenticate import authenticate
from vandura.config import aspace_credentials

import requests
import time
import json
import getpass
from pprint import pprint

def make_note_multipart(note_type, note_content):
	note_multipart = {
					"type":note_type,
					"jsonmodel_type":"note_multipart",
					"publish":True,
					"subnotes":[{
						"content":note_content,
						"jsonmodel_type":"note_text",
						"publish":True
						}]
					}
	return note_multipart

def make_note_singlepart(note_type, note_content):
	note_singlepart = {
						"type":note_type,
						"jsonmodel_type":"note_singlepart",
						"publish":True,
						"content": [note_content]
						}

	return note_singlepart

def resource_template():
	resource_template = {
					"record_type":"resource", 
					"defaults":{
						"title":"Enter collection title",
						"publish":True,
						"suppressed":False,
						"level":"collection",
						"language":"eng",
						"finding_aid_title":"Finding aid for the [collection title]",
						"finding_aid_author":"Finding aid created by [enter your name and month year of finding aid creation. Ex.: John Smith, April 2015.]",
						"finding_aid_description_rules":"Finding aid prepared using Describing Archives: A Content Standard (DACS)",
						"finding_aid_language":"The finding aid is written in <language langcode=\"eng\" scriptcode=\"Latn\">English</language>",
						"finding_aid_date":"skip",
						"dates": [
							{
								"label":"creation",
								"expression":"TBD",
								"date_type":"inclusive"
							}
						],
						"extents": [
							{
								"portion":"whole",
								"number":"1",
								"extent_type":"Type TBD"
							}
						],
						"notes":[
							make_note_singlepart("abstract", "Enter Abstract text here"),
							make_note_singlepart("langmaterial", "The material is in <language langcode=\"eng\">English</language>"),
							make_note_multipart("accessrestrict","[DELETE ONE]\r\nThis collection is open without restriction.\r\nOR\r\nRestricted access in part. [detail access restrictions]"),
							make_note_multipart("acqinfo", "Donated by [DONOR NAME] (donor no. <num type=\"donor\">[DONOR NUMBER]</num> in [MONTH YEAR]."),
							make_note_multipart("arrangement", "The collection is arranged into [n] series: [list series titles]"),
							make_note_multipart("bioghist", "[Enter personal/family biography or corporate body history here]"),
							make_note_multipart("relatedmaterial", "[DELETE THIS NOTE IF THERE ARE NO RELATED MATERIALS. REPEAT FULL SET OF <TITLE/> TAGS AS NECESSARY FOR ADDITIONAL RELATED COLLECTIONS]\r\nThe Bentley Historical Library houses the following related collections: <title href=\"[LINK]\" show=\"new\" actuate=\"onrequest\">[COLLECTION TITLE]</title>"),
							make_note_multipart("scopecontent", "enter collection-level Scope and Content note here"),
							make_note_multipart("accruals", "[DELETE ONE]\r\nPeriodic additions to the records expected.\r\n[OR]\r\nNo further additions to the records are expected."),
							make_note_multipart("userestrict", "[DELETE ALL BUT ONE. FIRST TWO OPTIONS GENERALLY APPLY TO NON-UNIVERSITY COLLECTIONS; SECOND TWO GENERALLY APPLY TO UNIVERSITY COLLECTIONS. THESE STOCK COPYRIGHT STATEMENTS MAY ALSO NEED SLIGHT MODIFICATIONS DEPENDING ON THE COLLECTION; CONSULT THE PROCESSING MANUAL FOR MORE INFORMATION]\r\nDonor(s) have transferred any applicable copyright to the Regents of the University of Michigan but the collection may contain third-party materials for which copyright was not transferred. Patrons are responsible for determining the appropriate use or reuse of materials.\r\nOR \r\nDonor(s) have not transferred any applicable copyright to the Regents of the University of Michigan. Patrons are responsible for determining the appropriate use or reuse of materials.\r\nOR\r\nCopyright is held by the Regents of the University of Michigan but the collection may contain third-party materials for which copyright is not held.  Patrons are responsible for determining the appropriate use or reuse of materials.\r\nOR\r\nCopyright is not held by the Regents of the University of Michigan.  Patrons are responsible for determining the appropriate use or reuse of materials."),
							make_note_multipart("prefercite","[item], folder, box, TITLE, Bentley Historical Library, University of Michigan. [URL]")]
						}
					}

	return json.dumps(resource_template)

def add_enum_values(session, aspace_url, enum_set_id, new_values_to_add):
		enum_address = aspace_url + '/config/enumerations/{}'.format(enum_set_id)
		existing_enums_json = session.get(enum_address).json()
		unique_values = [value for value in new_values_to_add if value not in existing_enums_json["values"]]
		existing_enums_json["values"].extend(unique_values)
		print(session.post(enum_address, data=json.dumps(existing_enums_json)).json())

def get_groups():
	"""
	transfer_repository
	manage_repository
	update_accession_record
	update_resource_record
	update_digital_object_record
	update_event_record
	delete_event_record
	suppress_archival_record
	transfer_archival_record
	delete_archival_record
	view_suppressed
	view_repository
	update_classification_record
	delete_classification_record
	import_records
	cancel_importer_job
	manage_subject_record
	manage_agent_record
	manage_vocabulary_record
	merge_agents_and_subjects
	merge_archival_record
	manage_rde_templates
	update_container_record
	manage_container_record
	manage_container_profile_record
	manage_location_profile_record
	"""
	groups = {
			"bhl-aspace-managers":
				{"description":"Managers of the BHL Repository",
				"permissions":['transfer_repository', 'manage_repository', 'update_accession_record', 'update_resource_record', 'update_digital_object_record', 
								'update_event_record', 'delete_event_record', 'suppress_archival_record', 'transfer_archival_record', 'delete_archival_record', 
								'view_suppressed', 'view_repository', 'update_classification_record', 'delete_classification_record', 'import_records', 
								'cancel_importer_job', 'manage_subject_record', 'manage_agent_record', 'manage_vocabulary_record', 'merge_agents_and_subjects', 
								'merge_archival_record', 'manage_rde_templates', 'update_container_record', 'manage_container_record', 
								'manage_container_profile_record', 'manage_location_profile_record']
				},
			"bhl-processors":
				{"description":"BHL Processors", 
				"permissions":["update_accession_record", "update_resource_record", "update_digital_object_record", "delete_archival_record",
								"view_repository", "manage_subject_record", "manage_agent_record", "manage_vocabulary_record", "merge_agents_and_subjects",
								"manage_rde_templates", "update_container_record", "manage_container_record", "manage_container_profile_record", "manage_location_profile_record"]
				},
			"bhl-accessioners":
				{"description":"BHL Accessioners",
				"permissions":["update_accession_record", "update_resource_record", "delete_archival_record", "manage_subject_record", "manage_agent_record",
								"view_repository", "manage_vocabulary_record", "update_container_record", "manage_container_record"]
				},
			"bhl-reference":
				{"description":"BHL Reference",
				"permissions":["view_repository"]
				}
			}

	return groups

def make_group(group_name, group_description, group_permissions):
	group = {"group_code":group_name,
			"description":group_description,
			"grants_permissions":group_permissions,
			"jsonmodel_type":"group"}

	return json.dumps(group)

def post_defaults(aspace_url, username, password):
	s = authenticate(aspace_url, username, password)
	s.headers.update({"Content-type":"application/json"})

	bhl_repo = {
			'name':'Bentley Historical Library',
			'org_code':'MiU-H',
			'repo_code':'BHL',
			'parent_institution_name':'University of Michigan'
			}

	# Create the BHL repository
	post_repo = s.post(aspace_url + '/repositories',data=json.dumps(bhl_repo)).json()
	print post_repo

	mhc_classification = {'title':'Michigan Historical Collections','identifier':'MHC'}
	uarp_classification = {'title':'University Archives','identifier':'UA'}
	faculty_classification = {'title':'Faculty Papers', 'identifier':'Faculty'}
	rcs_classification = {'title':'Records Center Storage','identifier':'RCS'}

	# Create classifications
	for classification in [mhc_classification, uarp_classification, faculty_classification, rcs_classification]: 
		classification_post = s.post(aspace_url + '/repositories/2/classifications',data=json.dumps(classification)).json()
		print classification_post
		
	# Update enumeration values
	add_enum_values(s, aspace_url, 23, ['lcnaf', 'lctgm', 'aacr2', 'lcgft', 'ftamc', 'fast'])  # subject sources
	add_enum_values(s, aspace_url, 4, ['lcnaf'])  # name sources
	add_enum_values(s, aspace_url, 55, ["on file", "pending", "sent", "n/a", "other"])  # user defined enum 1 values (gift agreement status)
	add_enum_values(s, aspace_url, 14, ["TB", "Type TBD"]) # extent
	add_enum_values(s, aspace_url, 9, ["backlog", "discarded", "cataloged", "processed?", "missing"]) # Processing status

	# Suppress the default instance types, since our "instance types" are really more like container labels
	instance_types = s.get("{}/config/enumerations/22".format(aspace_url)).json()
	for value in instance_types["enumeration_values"]:
		value_uri = value["uri"]
		s.post("{0}{1}/suppressed?suppressed=true".format(aspace_url, value_uri)).json()

	repo_preferences = {
		'repository':{'ref':'/repositories/2'},
		'defaults':{'publish':True, 'default_values':True}
		}

	# Post preferences
	print s.post(aspace_url + '/repositories/2/preferences',data=json.dumps(repo_preferences)).json()
	# Post resource template
	print s.post("{}/repositories/2/default_values/resource".format(aspace_url), data=resource_template()).json()

	# Delete the default groups
	default_groups = s.get("{}/repositories/2/groups".format(aspace_url)).json()
	for group in default_groups:
		group_uri = group["uri"]
		print s.delete("{}{}".format(aspace_url, group_uri)).json()


	# Create our own groups
	groups = get_groups()
	for group in groups:
		description = groups[group]["description"]
		permissions = groups[group]["permissions"]
		group_data = make_group(group, description, permissions)
		print s.post("{}/repositories/2/groups".format(aspace_url), data=group_data).json()

	s.post("{}/logout".format(aspace_url))


def main():
	aspace_url, username, password = aspace_credentials()
	post_defaults(aspace_url, username, password)

if __name__ == "__main__":
	main()