from vandura.config import marc_dir
from vandura.shared.scripts.convert_ead_to_aspace_json import convert_ead_to_aspace_json
from vandura.shared.scripts.post_json_to_aspace import post_json_to_aspace

import getpass
from os.path import join


def run_aspace_ead_migration(marc_dir, aspace_ead_dir, aspace_url, username, password):
	convert_ead_to_aspace_json(marc_dir, aspace_ead_dir, aspace_url, username, password)
	migration_stats_dir = join(marc_dir, "migration_stats")
	ead_to_json_errors = join(migration_stats_dir, 'ead_to_json_errors.txt')
	if os.path.exists(ead_to_json_errors):
		print "*** ERRORS DETECTED IN EAD TO ASPACE JSON CONVERSION ***"
		quit()
	else:
		post_json_to_aspace(marc_dir, aspace_url, username, password)
		json_to_aspace_errors = join(migration_stats_dir, 'json_to_aspace_errors.txt')
		if os.path.exists(json_to_aspace_errors):
			print "*** ERRORS DETECTED IN JSON TO ASPACE POSTING ***"
		else:
			print "*** ALL RESOURCES IMPORTED SUCCESSFULLY ***"

def main():
	aspace_ead_dir = join(marc_dir, 'converted_eads')
	aspace_url = 'http://localhost:8089'
	username = 'admin'
	print "*************************************************************"
	print "YOU ARE ABOUT TO RUN THE ARCHIVESSPACE EAD MIGRATION SCRIPT"
	print "Before doing so, confirm that the following have been run:"
	print "* characterize_and_convert_marcxml"
	print "* past_marc_agents_and_subjects"
	print "*************************************************************"
	ready_to_go = raw_input("Has everything been run? (y/n): ")
	if ready_to_go.lower() == 'y':
		print "*** ArchivesSpace Information ***"
		print "URL: {0}".format(aspace_url)
		print "Username: {0}".format(username)
		print "*********************************"
		aspace_info_correct = raw_input("Is the above ASpace information correct? (y/n): ")
		if aspace_info_correct.lower() == 'y':
			password = getpass.getpass("Enter your ASpace password: ")
			run_aspace_ead_migration(marc_dir, aspace_ead_dir, aspace_url, username, password)
		else:
			print "Please fix the incorrect values and run the script again"
			quit()
	else:
		print "Please run everything that needs to be run and then run this script again"
		quit()

if __name__ == "__main__":
	main()