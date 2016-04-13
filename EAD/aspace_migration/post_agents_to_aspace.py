import getpass
import json
import pickle

from os.path import join

from vandura.shared.aspace_agent_mapping.scripts.add_aspace_agent_ids_to_eads import add_aspace_ids_to_all_agents_in_dir
from vandura.shared.aspace_agent_mapping.scripts.get_agents_from_eads import get_all_agents
from vandura.shared.aspace_agent_mapping.scripts.post_agents import post_agents_and_record_ids
from vandura.shared.aspace_agent_mapping.scripts.prepare_agents_for_aspace import prepare_agents

from vandura.shared.scripts.archivesspace_authenticate import authenticate
from vandura.config import ead_dir
from vandura.config import aspace_credentials

# code to extract agents from EADs, post them to an ASpace instance, then write the new ASpace
# references for each agent back to the EAD files

# third-party libraries required: NLTK, tqdm, requests, nameparser

def post_agents_to_aspace(aspace_ead_dir, subjects_agents_dir, aspace_url, username, password):
    session = authenticate(aspace_url, username, password)
    # extract agent data from eads
    agents = get_all_agents(aspace_ead_dir)

    # create json-formatted entries for each agent
    prepped_agents = prepare_agents(agents)

    with open(join(subjects_agents_dir, "agents_aspace.json"), mode="wb") as f:
        string = json.dumps(prepped_agents, ensure_ascii=False, encoding="utf-8", sort_keys=True, indent=4)
        f.write(string.encode("utf-8"))

    # send these formatted entries to aspace and retrieve their new IDs
    local_name_to_aspace_id_map = post_agents_and_record_ids(session, aspace_url, prepped_agents)

    #session.post("{}/logout".format(aspace_url))
    with open(join(subjects_agents_dir, "local_to_aspace_agent_name_map.p"),"wb") as pickle_out:
        pickle.dump(local_name_to_aspace_id_map, pickle_out)
    # add these ids to our EAD files to map properly
    ead_path = ""
    add_aspace_ids_to_all_agents_in_dir(local_name_to_aspace_id_map, path_to_eads=aspace_ead_dir)



if __name__ == "__main__":
    aspace_ead_dir = join(ead_dir, "eads")
    subjects_agents_dir = join(ead_dir, "subjects_agents")
    aspace_url, username, password = aspace_credentials()
    post_agents_to_aspace(aspace_ead_dir, subjects_agents_dir, aspace_url, username, password)
