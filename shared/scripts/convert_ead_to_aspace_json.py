from vandura.config import marc_dir, ead_dir
from vandura.config import aspace_credentials
from vandura.shared.scripts.archivesspace_authenticate import authenticate

import getpass
import requests
import json
import os
from os.path import join
import time
from datetime import datetime

def convert_ead_to_aspace_json(base_dir, aspace_ead_dir, aspace_url, username, password):
    start_time = datetime.now()

    json_dir = join(base_dir, "json")
    json_success_dir = join(json_dir, "successes")
    json_error_dir = join(json_dir, "errors")
    migration_stats_dir = join(base_dir, "migration_stats")

    for directory in [json_dir, json_success_dir, json_error_dir, migration_stats_dir]:
        if not os.path.exists(directory):
            os.makedirs(directory)
        
    converter_stats_file = join(migration_stats_dir, 'ead_to_json_converter_stats.txt')
    ead_to_json_errors = join(migration_stats_dir, 'ead_to_json_errors.txt')
    for txt_document in [converter_stats_file, ead_to_json_errors]:
        if os.path.exists(txt_document):
            os.remove(txt_document)

    successes = []
    errors = []

    s = authenticate(aspace_url, username, password)
    s.headers.update({"Content-type":"text/xml; charset=utf-8"})

    already_converted = os.listdir(json_success_dir) + os.listdir(json_error_dir)
    files_to_convert = [filename for filename in os.listdir(aspace_ead_dir) if filename+".json" not in already_converted]
    
    for filename in files_to_convert:
        print "Converting {0} to ASpace JSON".format(filename)
        ead = open(join(aspace_ead_dir, filename), 'rb')
        eadtojson = s.post("{}/plugins/jsonmodel_from_format/resource/ead".format(aspace_url), data=ead)
        ead.close()
        try:
            response = eadtojson.json()
            for result in response:
                if 'invalid_object' in result and filename not in errors:
                    errors.append(filename)
                    with open(ead_to_json_errors,'a') as f:
                        f.write(filename + '\n')
                    with open(join(json_error_dir,filename+'.json'),'w') as f:
                        f.write(json.dumps(response))
                elif filename not in successes:
                    successes.append(filename)
                    with open(join(json_success_dir, filename+'.json'),'w') as f:
                        f.write(json.dumps(response))
        except:
            print eadtojson.content
            quit()
        time.sleep(2)

    end_time = datetime.now()

    script_start_time = start_time.strftime("%Y-%m-%d %H:%M:%S %p")
    script_end_time =  end_time.strftime("%Y-%m-%d %H:%M:%S %p")
    script_running_time = end_time - start_time

    converter_stats = """
Script start time: {0}
Script end time: {1}
Script running time: {2}
Successfully converted: {3} files
Errors encountered in: {4} files""".format(script_start_time, script_end_time, script_running_time, len(successes), len(errors))
    
    with open(converter_stats_file, 'w') as f:
        f.write(converter_stats)

    #s.post("{}/logout".format(aspace_url))

def main():
    options = {"EAD":ead_dir, "MARC":marc_dir}
    aspace_ead_dirs = {"EAD":"eads", "MARC":"converted_eads"}
    for key in options:
        print "* {}".format(key)
    dir_to_migrate = raw_input("Which type? ")
    try:
        base_dir = options[dir_to_migrate]
        aspace_ead_dir = join(base_dir, aspace_ead_dirs[dir_to_migrate])
    except:
        print "Please try again"
        quit()
    aspace_url, username, password = aspace_credentials()
    convert_ead_to_aspace_json(base_dir, aspace_ead_dir, aspace_url, username, password)

if __name__ == "__main__":
    main()