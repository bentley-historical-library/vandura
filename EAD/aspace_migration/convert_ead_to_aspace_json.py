from vandura.shared.scripts.archivesspace_authenticate import authenticate
from vandura.config import aspace_credentials

import requests
import json
import os
from os.path import join
import time
from datetime import datetime

def convert_ead_to_aspace_json(ead_dir, json_dir, migration_stats_dir, aspace_url, username, password):
    if not os.path.exists(json_dir):
        os.makedirs(json_dir)
    if not os.path.exists(migration_stats_dir):
        os.makedirs(migration_stats_dir)
        
    start_time = datetime.now()
    converter_stats_file = join(migration_stats_dir, 'ead_to_json_converter_stats.txt')
    ead_to_json_errors = join(migration_stats_dir, 'ead_to_json_errors.txt')
    for txt_document in [converter_stats_file, ead_to_json_errors]:
        if os.path.exists(txt_document):
            os.remove(txt_document)
    attempts = 0
    errors = 0
    s = authenticate(aspace_url, username, password)
    s.headers.update({"Content-type":"text/html; charset=utf-8"})
    for filename in os.listdir(ead_dir):
        if filename + '.json' not in os.listdir(json_dir):
            print "Converting {0} to ASpace JSON".format(filename)
            attempts += 1
            with open(join(ead_dir, filename),'rb') as data:
                eadtojson = s.post(aspace_url + '/plugins/jsonmodel_from_format/resource/ead', data=data)
                try:
                    response = eadtojson.json()
                    for result in response:
                        if 'invalid_object' in result:
                            with open(ead_to_json_errors,'a') as f:
                                f.write(filename + '\n')
                            errors += 1
                    with open(join(json_dir,filename+'.json'),'w') as json_out:
                        json_out.write(json.dumps(response))
                except:
                    print eadtojson.content 
                    quit()

    end_time = datetime.now()

    script_start_time = start_time.strftime("%Y-%m-%d %H:%M:%S %p")
    script_end_time =  end_time.strftime("%Y-%m-%d %H:%M:%S %p")
    script_running_time = end_time - start_time

    converter_stats = """
Script start time: {0}
Script end time: {1}
Script running time: {2}
Conversion attempted on: {3} files
Errors encountered in: {4} files""".format(script_start_time, script_end_time, script_running_time, attempts, errors)
    
    with open(converter_stats_file, 'w') as f:
        f.write(converter_stats)

    s.post("{}/logout".format(aspace_url))

def main():
    project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    aspace_ead_dir = join(project_dir, 'eads')
    json_dir = join(project_dir, 'json')
    migration_stats_dir = join(project_dir, 'migration_stats')
    aspace_url, username, password = aspace_credentials()
    convert_ead_to_aspace_json(aspace_ead_dir, json_dir, migration_stats_dir, aspace_url, username, password)

if __name__ == "__main__":
    main()