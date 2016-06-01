from vandura.config import aspace_credentials, ead_dir
from vandura.shared.scripts.archivesspace_authenticate import authenticate

from lxml import etree
import os
from os.path import join
from tqdm import tqdm

def verify_agents(ead_dir, aspace_url, username, password):
	s = authenticate(aspace_url, username, password)
	agent_uris = []
	for filename in os.listdir(ead_dir):
		print "Extracting agent uris from {}".format(filename)
		tree = etree.parse(join(ead_dir, filename))
		agents = tree.xpath("//controlaccess/corpname") + tree.xpath("//controlaccess/persname") + tree.xpath("//controlaccess/famname")
		for agent in agents:
			ref = agent.attrib["ref"]
			if ref not in agent_uris:
				agent_uris.append(ref)

	for agent_uri in tqdm(agent_uris, desc="verifying agents..."):
		response = s.head("{}{}".format(aspace_url, agent_uri)).status_code
		if response != 200:
			print "{} NOT FOUND".format(agent_uri)
			quit()

	s.post("{}/logout".format(aspace_url))

if __name__ == "__main__":
	aspace_url, username, password = aspace_credentials()
	aspace_ead_dir = join(ead_dir, "eads")
	verify_agents(aspace_ead_dir, aspace_url, username, password)
