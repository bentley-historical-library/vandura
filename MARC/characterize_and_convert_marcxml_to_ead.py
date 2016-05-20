from vandura.config import ead_dir, marc_dir, real_masters_all, shared_dir

from scripts.add_classifications import add_classifications
from scripts.add_containers import add_containers
from scripts.add_container_types import add_container_types
from scripts.agent_role_normalization import normalize_agent_roles
from scripts.agent_source_propagation import agent_source_propagation
from scripts.characterize_and_merge_marcxml import characterize_and_merge_marcxml
from scripts.convert_marcxml_to_ead import convert_marcxml_to_ead
from scripts.deduplicate_subjects import deduplicate_subjects
from scripts.note_cleanup import make_acqinfo_from_odd
from scripts.note_cleanup import normalize_extents
from scripts.note_cleanup import split_extents
from scripts.subject_source_propagation import subject_source_propagation

from vandura.shared.utilities.ead_cleanup.prettifydirectory import prettify_xml_in_directory

import os
from os.path import join

def characterize_and_convert_marcxml_to_ead(ead_dir, marc_dir, real_masters_all, shared_dir):
	characterize_and_merge_marcxml(real_masters_all, marc_dir)

	joined_dir = join(marc_dir, "marcxml_no_ead_joined")

	# This one is SUPPRESSED, is not in BEAL, and is for an unspecified department's publications
	os.remove(join(joined_dir, "011000.xml"))

	converted_dir = join(marc_dir, "converted_eads")
	unconverted_dir = join(marc_dir, "unconverted_marcxml")
	convert_marcxml_to_ead(joined_dir, converted_dir, unconverted_dir)

	normalize_extents(marc_dir)
	split_extents(marc_dir)
	make_acqinfo_from_odd(marc_dir)
	add_classifications(marc_dir, shared_dir)
	add_containers(marc_dir, shared_dir)
	add_container_types(marc_dir)
	deduplicate_subjects(marc_dir)
	subject_source_propagation(ead_dir, marc_dir)
	agent_source_propagation(marc_dir)
	normalize_agent_roles(marc_dir)

	prettify_xml_in_directory(converted_dir, converted_dir)




if __name__ == "__main__":
	characterize_and_convert_marcxml_to_ead(ead_dir, marc_dir, real_masters_all, shared_dir)
