from vandura.config import ead_dir
from vandura.config import aspace_credentials
from vandura.shared.scripts.archivesspace_authenticate import authenticate

import getpass
import requests
import json
from os.path import join
import time
from datetime import datetime
import os

migration_stats_dir = join(ead_dir, "migration_stats")
exporter_stats_file = join(migration_stats_dir, "exporter_stats.txt")
exports_dir = join(ead_dir, "exports")
if not os.path.exists(exports_dir):
    os.makedirs(exports_dir)

aspace_url, username, password = aspace_credentials()
s = authenticate(aspace_url, username, password)

start_time = datetime.now()

# Uncomment one of these to export everything or select resources
#ids_to_export = s.get('{}/repositories/2/resources?all_ids=true'.format(aspace_url)).json()
ids_to_export = ['413']
ids_to_export_count = len(ids_to_export)

already_exported = os.listdir(exports_dir)

count = 1
for resource_id in ids_to_export:
    metadata = s.get("{0}/repositories/2/bhl_resource_descriptions/{1}.xml/metadata".format(aspace_url, resource_id)).json()
    filename = metadata["filename"]
    if filename not in already_exported:
        print "{0}/{1} - Writing resource {2} to {3}".format(count, ids_to_export_count, resource_id, filename)
        ead = s.get('{0}/repositories/2/bhl_resource_descriptions/{1}.xml?include_unpublished=false&include_daos=true&numbered_cs=true'.format(aspace_url, resource_id),stream=True)
        with open(join(exports_dir, filename),'wb') as ead_out:
             for chunk in ead.iter_content(10240):
                    ead_out.write(chunk)
    else:
        print "{0}/{1} - Resource {2} has already been written to {3}".format(count, ids_to_export_count, resource_id, filename)
    count += 1

end_time = datetime.now()

script_start_time = start_time.strftime("%Y-%m-%d %H:%M:%S %p")
script_end_time = end_time.strftime("%Y-%m-%d %H:%M:%S %p")
script_running_time = end_time - start_time

print "Script start time:", script_start_time
print "Script end time:", script_end_time
print "Script running time:", script_running_time

exporter_stats = """
Script start time: {0}
Script end time: {1}
Script running time: {2}""".format(script_start_time, script_end_time, script_running_time)

with open(exporter_stats_file, "w") as f:
    f.write(exporter_stats)

s.post("{}/logout".format(aspace_url))
