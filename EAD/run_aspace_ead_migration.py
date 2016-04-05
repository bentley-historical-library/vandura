from vandura.config import ead_dir
from vandura.config import aspace_credentials
from vandura.shared.scripts.convert_ead_to_aspace_json import convert_ead_to_aspace_json
from vandura.shared.scripts.post_json_to_aspace import post_json_to_aspace

import getpass
import os
from os.path import join

def run_aspace_ead_migration(ead_dir, aspace_ead_dir, aspace_url, username, password):
	convert_ead_to_aspace_json(ead_dir, aspace_ead_dir, aspace_url, username, password)
	migration_stats_dir = join(ead_dir, "migration_stats")
	ead_to_json_errors = join(migration_stats_dir, 'ead_to_json_errors.txt')
	if os.path.exists(ead_to_json_errors):
		print "*** ERRORS DETECTED IN EAD TO ASPACE JSON CONVERSION ***"
		quit()
	else:
		post_json_to_aspace(ead_dir, aspace_url, username, password)
		json_to_aspace_errors = join(migration_stats_dir, 'json_to_aspace_errors.txt')
		if os.path.exists(json_to_aspace_errors):
			print "*** ERRORS DETECTED IN JSON TO ASPACE POSTING ***"
		else:
			print "*** ALL RESOURCES IMPORTED SUCCESSFULLY ***"

def main():
	print "*************************************************************"
	print "YOU ARE ABOUT TO RUN THE ARCHIVESSPACE EAD MIGRATION SCRIPT"
	print "Before doing so, confirm that the following have been run:"
	print "* run_pre_aspace_cleanup"
	print "* Walker's extent normalization script"
	print "* run_aspace_prep"
	print "* run_aspace_preliminary_postings"
	print "* run_unittitle_unitdate_fix"
	print "*************************************************************"
	ready_to_go = raw_input("Has everything been run? (y/n): ")
	if ready_to_go.lower() == 'y':
		aspace_url, username, password = aspace_credentials()
		run_aspace_ead_migration(aspace_ead_dir, json_dir, resources_dir, migration_stats_dir, aspace_url, username, password)
	else:
		print "Please run everything that needs to be run and then run this script again"
		quit()

if __name__ == "__main__":
	main()