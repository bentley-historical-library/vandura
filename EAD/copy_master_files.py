from vandura.config import ead_dir, real_masters_all
from aspace_prep.copy_eads import copy_eads
from os.path import join

aspace_ead_dir = join(ead_dir, "eads")

copy_eads(real_masters_all, aspace_ead_dir)