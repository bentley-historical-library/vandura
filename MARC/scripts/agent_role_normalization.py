from vandura.config import marc_dir

from lxml import etree
import os
from os.path import join

def normalize_agent_roles(marc_dir):
	ead_dir = join(marc_dir, "converted_eads")

	# From the ArchivesSpace linked_agent_archival_record_relators enum
	role_normalization_dict = {"collector":"col",
								"interviewee":"ive", 
								"author":"aut", 
								"performer":"prf", 
								"host":"hst", 
								"photographer":"pht",
								"defendant":"dfd",
								"Defendant":"dfd",
								"PRO":"pro",
								"compiler":"com",
								"supposed printers":"prt",
								"tr":"trl"}

	agent_tags = ["persname", "corpname", "famname"]

	for filename in os.listdir(ead_dir):
		print "Normalizing agent roles in {}".format(filename)
		tree = etree.parse(join(ead_dir, filename))
		rewrite = False
		for tag in agent_tags:
			for agent in tree.xpath("//{}".format(tag)):
				role = agent.get("role", "")
				if role == "Mrs":
					title = etree.Element("title")
					title.text = role+"."
					agent.append(title)
					del agent.attrib["role"]
					rewrite = True
				if role in role_normalization_dict:
					agent.attrib["role"] = role_normalization_dict[role]
					rewrite = True

		if rewrite:
			with open(join(ead_dir, filename), "w") as f:
				f.write(etree.tostring(tree, encoding="utf-8", xml_declaration=True, pretty_print=True))

if __name__ == "__main__":
	normalize_agent_roles(marc_dir)
