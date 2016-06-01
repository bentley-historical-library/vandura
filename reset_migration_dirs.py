from vandura.config import ead_dir, marc_dir
import os
from os.path import join

migration_dirs = ["json", "resources", "migration_stats"]
has_sub_dirs = ["json", "resources"]
sub_dirs = ["successes","errors"]

for directory in [ead_dir, marc_dir]:
	for migration_dir in migration_dirs:
		if migration_dir in has_sub_dirs:
			for sub_dir in sub_dirs:
				dir_to_delete = join(directory, migration_dir, sub_dir)
				print "Removing files from {}".format(dir_to_delete)
				files_to_delete = os.listdir(dir_to_delete)
				for filename in files_to_delete:
					os.remove(join(dir_to_delete, filename))
		else:
			dir_to_delete = join(directory, migration_dir)
			print "Removing files from {}".format(dir_to_delete)
			files_to_delete = os.listdir(dir_to_delete)
			for filename in files_to_delete:
				os.remove(join(dir_to_delete, filename))