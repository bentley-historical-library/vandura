from vandura.config import marc_dir
from scripts.post_agents import get_and_post_agents
from scripts.post_subjects import get_and_post_subjects
from scripts.add_subject_and_agent_uris import add_subject_and_agent_uris

import getpass

aspace_url = "http://localhost:8089"
username = "admin"
password = getpass.getpass("Password:")

get_and_post_agents(marc_dir, aspace_url, username, password)
get_and_post_subjects(marc_dir, aspace_url, username, password)
add_subject_and_agent_uris(marc_dir)