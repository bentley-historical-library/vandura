from __future__ import absolute_import

from vandura.config import real_masters_all, marc_dir

from os.path import join

from vandura.EAD.aspaceify_extents.aspaceify_extents import aspaceify_extents
from vandura.EAD.aspaceify_extents.aspaceify_extents.scripts.extent_grab import get_all_extents


# CHANGE THESE TWO PATHS TO MATCH YOUR SYSTEM
# THE OUTPUT DIRECTORY CAN BE ANYWHERE YOU'D LIKE
ead_input_directory = join(marc_dir, "converted_eads")
ead_output_directory = join(marc_dir, "converted_eads")

# get a list of all extents in your eads, with their xml paths
extents = get_all_extents(ead_input_directory)


# now process this list
aspaceify_extents.main(extent_list=extents,
                       input_dir=ead_input_directory,
                       output_dir=ead_output_directory)

