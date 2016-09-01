from vandura.config import ead_dir

from os.path import join

from unitdates_in_unittitles.unitdates_unittitles_fix import unitdates_unittitles_fix
from unitdates_in_unittitles.capitalize_unittitles import capitalize_unittitles
from unitdates_in_unittitles.deduplicate_dates import remove_duplicate_unitdates
from unitdates_in_unittitles.deduplicate_dates import consolidate_duplicate_data
from unitdates_in_unittitles.add_inclusive_types import add_inclusive_types
from unitdates_in_unittitles.make_odds_from_unittitles import make_odds_from_unittitles

def run_unitdates_in_unittitles(aspace_ead_dir):
	unitdates_unittitles_fix(aspace_ead_dir, aspace_ead_dir)
	add_inclusive_types(aspace_ead_dir)
	capitalize_unittitles(aspace_ead_dir)
	make_odds_from_unittitles(aspace_ead_dir)
	remove_duplicate_unitdates(aspace_ead_dir)
	consolidate_duplicate_data(aspace_ead_dir)

def main():
	aspace_ead_dir = join(ead_dir, 'eads')
	post_migration_eads = join(ead_dir, "post_migration_eads")
	run_unitdates_in_unittitles(post_migration_eads)

if __name__ == "__main__":
	main()