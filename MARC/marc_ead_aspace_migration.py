from vandura.config import marc_dir
from vandura.config import aspace_credentials
from vandura.shared.scripts.convert_ead_to_aspace_json import convert_ead_to_aspace_json
from vandura.shared.scripts.post_json_to_aspace import post_json_to_aspace

import os
from os.path import join


def run_aspace_ead_migration(marc_dir, aspace_ead_dir, aspace_url, username, password):
	convert_ead_to_aspace_json(marc_dir, aspace_ead_dir, aspace_url, username, password)
	migration_stats_dir = join(marc_dir, "migration_stats")
	ead_to_json_errors = join(migration_stats_dir, 'ead_to_json_errors.txt')
	#if os.path.exists(ead_to_json_errors):
		#print "*** ERRORS DETECTED IN EAD TO ASPACE JSON CONVERSION ***"
		#quit()
	if False:
		quit()
	else:
		post_json_to_aspace(marc_dir, aspace_url, username, password)
		json_to_aspace_errors = join(migration_stats_dir, 'json_to_aspace_errors.txt')
		if os.path.exists(json_to_aspace_errors):
			print "*** ERRORS DETECTED IN JSON TO ASPACE POSTING ***"
		else:
			print "*** ALL RESOURCES IMPORTED SUCCESSFULLY ***"

def main():
	print "*************************************************************"
	print "YOU ARE ABOUT TO RUN THE ARCHIVESSPACE EAD MIGRATION SCRIPT"
	print "Before doing so, confirm that the following have been run:"
	print "* characterize_and_convert_marcxml"
	print "* past_marc_agents_and_subjects"
	print "*************************************************************"
	ready_to_go = raw_input("Has everything been run? (y/n): ")
	if ready_to_go.lower() == 'y':
		aspace_ead_dir = join(marc_dir, "converted_eads")
		aspace_url, username, password = aspace_credentials()
		run_aspace_ead_migration(marc_dir, aspace_ead_dir, aspace_url, username, password)
	else:
		print "Please run everything that needs to be run and then run this script again"
		quit()

if __name__ == "__main__":
	main()