import os
from os.path import join
import shutil

from vandura.config import real_masters_all, ead_dir

def copy_eads(ead_dir, dst_dir):
	if not os.path.exists(dst_dir):
		os.makedirs(dst_dir)

	filenames = [filename for filename in os.listdir(ead_dir) if filename.endswith('.xml')]

	for filename in filenames:
		print "Copying {0} to {1}".format(filename, dst_dir)
		src_file = join(ead_dir,filename)
		shutil.copy(src_file,dst_dir)

def main():
	dst_dir = join(ead_dir, 'eads')
	copy_eads(real_masters_all,dst_dir)

if __name__ == "__main__":
	main()