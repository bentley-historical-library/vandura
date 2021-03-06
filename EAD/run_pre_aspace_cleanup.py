from vandura.config import dspace_mets_dir, dspace_xoai_dir, ead_dir, real_masters_all 

from os.path import join
import os

from pre_aspace_cleanup.normalize_dates import normalize_dates
from pre_aspace_cleanup.authfilenumber_urls_to_uris import authfilenumber_urls_to_uris
from pre_aspace_cleanup.authfilenumber_propagation import authfilenumber_propagation
from pre_aspace_cleanup.downcase_certainty import downcase_certainty
from pre_aspace_cleanup.fetch_dspace_mets import fetch_dspace_mets
from pre_aspace_cleanup.fetch_dspace_xoai import fetch_dspace_xoai
from pre_aspace_cleanup.fix_collection_level_unittitle_commas import fix_collection_level_unittitle_commas
from pre_aspace_cleanup.note_to_odd import note_to_odd
from pre_aspace_cleanup.move_odds import move_odds
from pre_aspace_cleanup.move_daos import move_daos
from pre_aspace_cleanup.remove_and_between_dates import remove_and_between_dates
from pre_aspace_cleanup.remove_extent_parens import remove_extent_parens
from pre_aspace_cleanup.remove_expired_restrictions import remove_expired_restrictions
from pre_aspace_cleanup.remove_nested_genreforms import remove_nested_genreforms
from pre_aspace_cleanup.remove_unitdates_from_ps import remove_unitdates_from_ps
from pre_aspace_cleanup.wrap_unwrapped_unitdates import wrap_unwrapped_unitdates

from vandura.shared.utilities.ead_cleanup.prettifydirectory import prettify_xml_in_directory

def run_pre_aspace_cleanup(ead_dir, dspace_mets_dir, dspace_xoai_dir):
	fix_collection_level_unittitle_commas(ead_dir)
	wrap_unwrapped_unitdates(ead_dir)
	normalize_dates(ead_dir)
	downcase_certainty(ead_dir)
	authfilenumber_urls_to_uris(ead_dir)
	authfilenumber_propagation(ead_dir)
	fetch_dspace_xoai(ead_dir, dspace_mets_dir, dspace_xoai_dir)
	note_to_odd(ead_dir)
	move_odds(ead_dir)
	remove_unitdates_from_ps(ead_dir)
	move_daos(ead_dir)
	remove_and_between_dates(ead_dir)
	remove_extent_parens(ead_dir)
	remove_expired_restrictions(ead_dir)
	remove_nested_genreforms(ead_dir)
	prettify_xml_in_directory(ead_dir, ead_dir)
	print "*** RUN WALKER'S EXTENT NORMALIZATION SCRIPT ***"
	print "*** COPY THE MASTER FILES TO THE LOCAL EAD DIR ***"

def main():
	aspace_ead_dir = join(ead_dir, 'eads')
	post_migration_eads = join(ead_dir, "post_migration_eads")
	run_pre_aspace_cleanup(post_migration_eads, dspace_mets_dir, dspace_xoai_dir)

if __name__ == "__main__":
	main()