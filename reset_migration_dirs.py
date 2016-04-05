from vandura.config import ead_dir, marc_dir
import os
from os.path import join

migration_dirs = ["json", "resources", "migration_stats"]

for directory in [ead_dir, marc_dir]:
	for migration_dir in migration_dirs:
		dir_to_delete = join(directory, migration_dir)
		print "Removing files from {}".format(dir_to_delete)
		for filename in os.listdir(dir_to_delete):
			os.remove(join(dir_to_delete, filename))