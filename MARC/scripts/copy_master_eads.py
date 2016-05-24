from vandura.config import marc_dir
import os
from os.path import join
import shutil

def copy_master_eads(marc_dir):
	converted_eads = join(marc_dir, "converted_eads")
	converted_eads_working = join(marc_dir, "converted_eads_working")

	print "Deleting existing working copy"
	for filename in os.listdir(converted_eads_working):
		os.remove(join(converted_eads_working, filename))

	print "Copying master EADs to working directory"
	for filename in os.listdir(converted_eads):
		shutil.copy(join(converted_eads, filename), converted_eads_working)
