from vandura.shared.scripts.archivesspace_authenticate import authenticate
from vandura.config import aspace_credentials

import requests
import os
from os.path import join
import json
import time
from datetime import datetime

def post_json_to_aspace(json_dir, resources_dir, migration_stats_dir, aspace_url, username, password):
    if not os.path.exists(resources_dir):
        os.makedirs(resources_dir)
    importer_stats_file = join(migration_stats_dir, 'json_to_aspace_stats.txt')
    json_to_aspace_errors = join(migration_stats_dir, 'json_to_aspace_errors.txt')
    json_to_aspace_successes = join(migration_stats_dir, 'json_to_aspace_successes.txt')

    for txt_document in [importer_stats_file, json_to_aspace_successes, json_to_aspace_errors]:
        if os.path.exists(txt_document):
            os.remove(txt_document)

    start_time = datetime.now()

    errors = []
    successes = []

    s = authenticate(aspace_url, username, password)
    s.headers.update({"Content-type":"application/json"})
    for filename in os.listdir(json_dir):
        if filename not in os.listdir(resources_dir):
            print "Posting {0}".format(filename)
            with open(join(json_dir, filename), 'rb') as data:
                jsontoresource = s.post(aspace_url + '/repositories/2/batch_imports', data=data)
                try:
                    response = jsontoresource.json()
                    for result in response:
                        if 'saved' in result and not 'errors' in result:
                            if filename not in successes:
                                successes.append(filename)
                        elif 'errors' in result:
                            if filename not in errors:
                                errors.append(filename)
                    with open(join(resources_dir,filename),'w') as json_out:
                        json_out.write(json.dumps(response))
                    if filename in errors:
                        print "Error posting {0}".format(filename)
                    elif filename in successes:
                        print "{0} posted successfully".format(filename)
                except:
                    print jsontoresource.content 
                    quit()

    if errors:
        with open(json_to_aspace_errors,'w') as f:
            f.write("\n".join(errors))
    if successes:
        with open(json_to_aspace_successes,'w') as f:
            f.write("\n".join(successes))

    end_time = datetime.now()

    print "Successfully imported:", str(len(successes))
    print "Errors encountered in", str(len(errors)), "files"

    script_start_time = start_time.strftime("%Y-%m-%d %H:%M:%S %p")
    script_end_time = end_time.strftime("%Y-%m-%d %H:%M:%S %p")
    script_running_time = end_time - start_time

    importer_stats = """
Script start time: {0}
Script end time: {1}
Script running time: {2}
Successfully imported: {3} files
Errors encountered in: {4} files""".format(script_start_time, script_end_time, script_running_time, str(len(successes)), str(len(errors)))
    
    with open(importer_stats_file,'w') as f:
        f.write(importer_stats)

    s.post("{}/logout".format(aspace_url))

def main():
    project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    json_dir = join(project_dir, 'json')
    resources_dir = join(project_dir, 'resources')
    migration_stats_dir = join(project_dir, 'migration_stats')
    aspace_url, username, password = aspace_credentials()
    post_json_to_aspace(json_dir, resources_dir, migration_stats_dir, aspace_url, username, password)

if __name__ == "__main__":
    main()

    
