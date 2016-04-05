# BHL EAD ArchivesSpace Migration
EAD cleanup, prep, conversion, and posting scripts for the Bentley's ArchivesSpace migration.

##Requirements
* Walker's [bentley_code](https://github.com/walkerdb/bentley_code) repository (in particular, the agent mapping, extent normalization, and unitdates_in_unittitles normalization scripts) and associated requirements
* [lxml](http://lxml.de/)

##Running Order
1. run_pre_aspace_cleanup.py [this can be run at any time on the BHL's EADs]
2. aspaceify_extents/run_aspaceify.py
3. copy_master_files.py
4. run_aspace_prep.py
5. run_aspace_preliminary_postings.py
6. run_unitdate_unittitle_fix.py
7. run_aspace_verification.py
8. run_aspace_ead_migration.py
