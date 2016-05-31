from vandura.shared.scripts.archivesspace_authenticate import authenticate
from vandura.config import ead_dir
from vandura.config import aspace_credentials

import csv
import json
import requests
from os.path import join
from tqdm import tqdm

def post_subjects(ead_dir, subjects_agents_dir, aspace_url, username, password):
    print "Posting subjects..."
    subjects_csv = join(subjects_agents_dir, 'aspace_subjects.csv')
    posted_csv = join(subjects_agents_dir, 'posted_subjects.csv')
    text_to_authfilenumber_csv = join(subjects_agents_dir, 'text_to_authfilenumber.csv')

    text_to_authfilenumber = {}
    with open(text_to_authfilenumber_csv,'rb') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            sub_text = row[0]
            authfilenumber = row[1]
            text_to_authfilenumber[sub_text] = authfilenumber

    s = authenticate(aspace_url, username, password)
    s.headers.update({"Content-type":"application/json"})

    subjects_data = []
    with open(subjects_csv,'rb') as csvfile:
        reader = csv.reader(csvfile)
        rows = [row for row in reader]
        for row in tqdm(rows, desc="Posting subjects..."):
            row_indexes = len(row) - 1
            source = row[1]
            full_text = row[2]
            if full_text in text_to_authfilenumber:
                authfilenumber = text_to_authfilenumber[full_text]
            else:
                authfilenumber = ''
            terms_list = []
            for row_num in range(3,row_indexes + 1, 2):
                term = row[row_num]
                term_type = row[row_num+1]
                terms_dict = {}
                terms_dict["term"] = term
                terms_dict["term_type"] = term_type
                terms_dict["vocabulary"] = "/vocabularies/1"
                terms_list.append(terms_dict)

            data = json.dumps({"authority_id":authfilenumber,"source":source,"vocabulary":"/vocabularies/1","terms":[i for i in terms_list]})
            subjects = s.post(aspace_url+'/subjects', data=data).json()
            if 'status' in subjects:
                if subjects['status'] == 'Created':
                    subject_uri = subjects['uri']
                    row.append(subject_uri)
                    subjects_data.append(row)
            elif "error" in subjects:
                if "conflicting_record" in subjects["error"]:
                    subject_uri = subjects["error"]["conflicting_record"][0]
                    row.append(subject_uri)
                    subjects_data.append(row)
            else:
                print subjects

    with open(posted_csv,'wb') as csv_out:
        writer = csv.writer(csv_out)
        writer.writerows(subjects_data)

    s.post("{}/logout".format(aspace_url))

def main():
    aspace_ead_dir = join(ead_dir, 'eads')
    subjects_agents_dir = join(ead_dir,'subjects_agents')
    aspace_url, username, password = aspace_credentials()
    post_subjects(aspace_ead_dir, subjects_agents_dir, aspace_url, username, password)

if __name__ == "__main__":
    main()
