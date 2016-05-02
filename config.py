import getpass
import os

vandura_base_dir = os.path.dirname(os.path.abspath(__file__))

accessions_dir = os.path.join(vandura_base_dir, "ACCESSIONS")
dspace_mets_dir = os.path.join(vandura_base_dir, "dspace_mets")
dspace_xoai_dir = os.path.join(vandura_base_dir, "dspace_xoai")
ead_dir = os.path.join(vandura_base_dir, "EAD")
marc_dir = os.path.join(vandura_base_dir, "MARC")
real_masters_all = os.path.join(vandura_base_dir, "Real_Masters_all")
shared_dir = os.path.join(vandura_base_dir, "shared")

def aspace_credentials():
	aspace_url = "http://localhost:8089"
	aspace_username = "admin"
	print "Connecting to: {}".format(aspace_url)
	print "Username: {}".format(aspace_username)
	is_correct = raw_input("Is this information correct? (y/n) ")
	if is_correct.lower() == "y":
		aspace_password = getpass.getpass("Enter your ArchivesSpace password: ")
		return aspace_url, aspace_username, aspace_password
	elif is_correct.lower() == "n":
		aspace_url = raw_input("Enter the correct ArchivesSpace URL: ")
		aspace_username = raw_input("Enter the correct ArchivesSpace username: ")
		aspace_password = getpass.getpass("Enter your ArchivesSpace password: ")
		return aspace_url, aspace_username, aspace_password
	else:
		print "Quitting"
		quit()