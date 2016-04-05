import os
from os.path import join
from vandura.config import accessions_dir, ead_dir, marc_dir

marc_dirs = ["json", "resources", "migration_stats", "marcxml_has_ead", "marcxml_no_ead", "marcxml_no_ead_joined", "marcxml_unknown", "converted_eads", "unconverted_marcxml"]
ead_dirs = ["json", "resources", "migration_stats"]
accession_dirs = ["beal_exports", "json"]

for directory in marc_dirs:
	dir_to_create = join(marc_dir, directory)
	if not os.path.exists(dir_to_create):
		os.makedirs(dir_to_create)

for directory in ead_dirs:
	dir_to_create = join(ead_dir, directory)
	if not os.path.exists(dir_to_create):
		os.makedirs(dir_to_create)

for directory in accession_dirs:
	dir_to_create = join(accessions_dir, directory)
	if not os.path.exists(dir_to_create):
		os.makedirs(dir_to_create)