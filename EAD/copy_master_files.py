import os

from vandura.config import ead_dir, real_masters_all

from aspace_prep.copy_eads import copy_eads

aspace_ead_dir = join(ead_dir, "eads")
muschenheim_dir = join(ead_dir, "muschenheim")

copy_eads(muschenheim_dir, aspace_ead_dir)
copy_eads(real_masters_all, aspace_ead_dir)