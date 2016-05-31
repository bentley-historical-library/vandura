from lxml import etree
import os
from os.path import join
import re

def add_inclusive_types(ead_dir):
	for filename in os.listdir(ead_dir):
		print "Adding type attribute to unitdates in {}".format(filename)
		tree = etree.parse(join(ead_dir, filename))
		rewrite = False
		unitdates = tree.xpath("//did/unitdate")
		for unitdate in unitdates:
			if 'type' not in unitdate.attrib:
				rewrite = True
				unitdate.attrib['type'] = "inclusive"

		if rewrite:
			with open(join(ead_dir, filename), 'w') as f:
				f.write(etree.tostring(tree, encoding='utf-8', xml_declaration=True, pretty_print=True))

def main():
	project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
	aspace_ead_dir = join(project_dir, 'eads')
	add_inclusive_types(aspace_ead_dir)

if __name__ == "__main__":
	main()