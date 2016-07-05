from vandura.config import real_masters_all
import os
from os.path import join
from lxml import etree

def downcase_certainty(ead_dir):
	for filename in os.listdir(ead_dir):
		print "Downcasing unitdate certainty attributes in {}".format(filename)
		tree = etree.parse(join(ead_dir, filename))
		rewrite = False
		unitdates = tree.xpath("//did//unitdate")
		for unitdate in unitdates:
			if "certainty" in unitdate.attrib and unitdate.attrib["certainty"] != unitdate.attrib["certainty"].lower():
				rewrite = True
				unitdate.attrib["certainty"] = unitdate.attrib["certainty"].lower()

		if rewrite:
			with open(join(ead_dir, filename), 'w') as f:
				f.write(etree.tostring(tree, encoding='utf-8', xml_declaration=True, pretty_print=True))

def main():
	downcase_certainty(real_masters_all)

if __name__ == "__main__":
	main()