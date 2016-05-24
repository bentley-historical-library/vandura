from vandura.config import marc_dir
from vandura.config import aspace_credentials
from vandura.shared.scripts.archivesspace_authenticate import authenticate

import json
from lxml import etree
import os
from os.path import join
import re
import requests

def get_subjects(ead_dir):
	subjects = {}

	for filename in os.listdir(ead_dir):
		print "Getting subjects from {}".format(filename)
		tree = etree.parse(join(ead_dir, filename))
		for subject in tree.xpath("//subject"):
			if subject.xpath("./term"):
				source = normalize_source(subject.attrib["source"])
				if source not in subjects:
					subjects[source] = []
				subject_string = etree.tostring(subject).strip()
				subject_string = re.sub(r"<\/?subject(.*?)>","", subject_string)
				if subject_string not in subjects[source]:
					subjects[source].append(subject_string)

	return subjects

def make_subjects_json(subjects):
	subjects_json = {}
	print "Making subjects json"
	for source in subjects:
		for subject in subjects[source]:
			parsable_subject = etree.fromstring("<subject>{}</subject>".format(subject))
			terms_list = []
			for term in parsable_subject.xpath("./term"):
				term_dict = {}
				term_dict["term_type"] = term.attrib["type"]
				term_dict["term"] = term.text.strip()
				term_dict["vocabulary"] = "/vocabularies/1"
				terms_list.append(term_dict)

			subject_json = {u"source":source,
							u"vocabulary":"/vocabularies/1",
							u"terms":[term for term in terms_list]}

			subjects_json[subject] = subject_json

	return subjects_json

def normalize_source(source):
	if source in ["ltcgm", "lctrgm", "lcgtm", "1ctgm", "lctm"]:
		source = "lctgm"

	if source in ["1csh"]:
		source = "lcsh"

	return source.strip(".").strip("]")

def post_subjects(subjects_json, aspace_url, username, password):
	subjects_to_aspace_ids = {}

	s = authenticate(aspace_url, username, password)
	s.headers.update({"Content-type":"application/json"})

	for subject in subjects_json:
		subject_json = subjects_json[subject]
		response = s.post("{}/subjects".format(aspace_url), data=json.dumps(subject_json)).json()
		subjects_to_aspace_ids[subject] = extract_id(response)

	s.post("{}/logout".format(aspace_url))
	return subjects_to_aspace_ids

def extract_id(response):
	if u"status" in response:
		aspace_id = response[u"uri"]
	if u"error" in response:
		print response
		aspace_id = response[u"error"][u"conflicting_record"][0]

	return aspace_id

def get_and_post_subjects(marc_dir, aspace_url, username, password):
	ead_dir = join(marc_dir, "converted_eads_working")
	subjects_and_agents_dir = join(marc_dir, "subjects_agents")
	if not os.path.exists(subjects_and_agents_dir):
		os.makedirs(subjects_and_agents_dir)
	subjects_to_aspace_ids_file = join(subjects_and_agents_dir, "subjects_to_aspace_ids.json")
	subjects = get_subjects(ead_dir)
	subjects_json = make_subjects_json(subjects)
	subjects_to_aspace_ids = post_subjects(subjects_json, aspace_url, username, password)

	with open(subjects_to_aspace_ids_file, "wb") as f:
		f.write(json.dumps(subjects_to_aspace_ids))

def main():
	aspace_url, username, password = aspace_credentials()
	get_and_post_subjects(marc_dir, aspace_url, username, password)

if __name__ == "__main__":
	main()






