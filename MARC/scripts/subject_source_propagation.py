from vandura.config import marc_dir, ead_dir

import csv
from lxml import etree
import os
from os.path import join

def make_source_lists(subject_csv, ead_dir):
	lcsh_list = []
	aat_list = []

	print "Building sources list from csv"
	with open(subject_csv, 'rb') as csvfile:
		reader = csv.reader(csvfile)
		for row in reader:
			source = row[1].strip()
			subject = row[2].strip()
			if source == "lcsh" and subject not in lcsh_list:
				lcsh_list.append(subject)
			elif source == "aat" and subject not in aat_list:
				aat_list.append(subject)

	for filename in os.listdir(ead_dir):
		print "Building sources list from {}".format(filename)
		tree = etree.parse(join(ead_dir, filename))
		subjects = tree.xpath("//subject")
		for subject in subjects:
			source = subject.get("source", "")
			subject_joined = "--".join([subfield.text.strip() for subfield in subject.xpath("./*")])
			if source == "lcsh" and subject_joined not in lcsh_list:
				lcsh_list.append(subject_joined)
			elif source == "aat" and subject_joined not in aat_list:
				aat_list.append(subject_joined)

	return lcsh_list, aat_list

def propagate_sources(lcsh_list, aat_list, converted_ead_dir):
	for filename in os.listdir(converted_ead_dir):
		print "Propagating sources in {}".format(filename)
		tree = etree.parse(join(converted_ead_dir, filename))
		subjects = tree.xpath("//subject")
		rewrite = False
		for subject in subjects:
			source = subject.get("source", "")
			if source == "local":
				subject_joined = "--".join([subfield.text.strip() for subfield in subject.xpath("./*")])
				if subject_joined in lcsh_list:
					subject.attrib["source"] = "lcsh"
					rewrite = True
				elif subject_joined in aat_list:
					subject.attrib["source"] = "aat"
					rewrite = True

		if rewrite:
			with open(join(converted_ead_dir, filename), 'w') as f:
				f.write(etree.tostring(tree, encoding="utf-8", xml_declaration=True, pretty_print=True))

def subject_source_propagation(ead_dir, marc_dir):
	converted_eads = join(marc_dir, "converted_eads_working")
	ead_subject_csv = join(ead_dir, "subjects_agents", "ead_unique_subjects.csv")
	lcsh_list, aat_list = make_source_lists(ead_subject_csv, converted_eads)
	propagate_sources(lcsh_list, aat_list, converted_eads)

if __name__ == "__main__":
	subject_source_propagation(ead_dir, marc_dir)



