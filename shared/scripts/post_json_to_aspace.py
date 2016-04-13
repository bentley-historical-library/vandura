from vandura.shared.scripts.archivesspace_authenticate import authenticate
from vandura.config import aspace_credentials
from vandura.config import marc_dir, ead_dir

import getpass
import requests
import os
from os.path import join
import json
import time
from datetime import datetime

def post_json_to_aspace(base_dir, aspace_url, username, password):
    json_dir = join(base_dir, "json")
    json_success_dir = join(json_dir, "successes")
    resources_dir = join(base_dir, "resources")
    resource_error_dir = join(resources_dir, "errors")
    resource_success_dir = join(resources_dir, "successes")
    migration_stats_dir = join(base_dir, "migration_stats")

    for directory in [resources_dir, resource_error_dir, resource_success_dir, migration_stats_dir]:
        if not os.path.exists(directory):
            os.makedirs(directory)

    importer_stats_file = join(migration_stats_dir, 'json_to_aspace_stats.txt')
    json_to_aspace_errors = join(migration_stats_dir, 'json_to_aspace_errors.txt')

    for txt_document in [importer_stats_file, json_to_aspace_errors]:
        if os.path.exists(txt_document):
            os.remove(txt_document)

    start_time = datetime.now()

    errors = []
    successes = []

    s = authenticate(aspace_url, username, password)
    s.headers.update({"Content-type":"application/json"})

    already_posted = os.listdir(resource_success_dir) + os.listdir(resource_error_dir)
    files_to_post = [filename for filename in os.listdir(json_success_dir) if filename not in already_posted]
    
    for filename in files_to_post:
        print "Posting {0}".format(filename)
        resource = open(join(json_success_dir, filename), "rb")
        jsontoresource = s.post("{0}/repositories/2/resources".format(aspace_url), data=resource)
        try:
            response = jsontoresource.json()
            for result in response:
                if 'saved' in result and not 'errors' in result:
                    if filename not in successes:
                        successes.append(filename)
                elif 'errors' in result:
                    if filename not in errors:
                        errors.append(filename)
                        with open(json_to_aspace_errors, 'a') as f:
                            f.write(filename+"\n")
            if filename in successes:
                print "{0} posted successfully".format(filename)
                with open(join(resource_success_dir,filename),'w') as f:
                    f.write(json.dumps(response))
            elif filename in errors:
                print "Error posting {0}".format(filename)
                with open(join(resource_error_dir, filename), 'w') as f:
                    f.write(json.dumps(response))                    
        except:
            print jsontoresource.content 
            quit()
        time.sleep(2)

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

    #s.post("{}/logout".format(aspace_url))

def main():
    options = {"EAD":ead_dir, "MARC":marc_dir}
    for key in options:
        print "* {}".format(key)
    dir_to_migrate = raw_input("Which type? ")
    try:
        base_dir = options[dir_to_migrate]
    except:
        print "Please try again"
        quit()
    aspace_url, username, password = aspace_credentials()
    post_json_to_aspace(base_dir, aspace_url, username, password)

if __name__ == "__main__":
    main()

    
