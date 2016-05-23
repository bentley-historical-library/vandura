from lxml import etree
import os
from os.path import join
import csv

from vandura.config import marc_dir

converted_eads = join(marc_dir, "converted_eads")
extent_csv = join(marc_dir, "CSVs", "converted_ead_extents.csv")

physdescs_info = []
for filename in os.listdir(converted_eads):
	print "Extracting physdescs from {}".format(filename)
	tree = etree.parse(join(converted_eads, filename))
	physdescs = tree.xpath("//physdesc")
	for physdesc in physdescs:
		physdesc_path = tree.getpath(physdesc)
		physdesc_info = {"filename":filename, "xpath":physdesc_path}
		for element in physdesc.xpath("./*"):
			element_text = element.text.strip().encode("utf-8")
			element_name = element.tag
			physdesc_info[element_name] = element_text
		physdescs_info.append(physdesc_info)

fieldnames = ["filename", "xpath", "extent", "physfacet", "dimensions"]
with open(extent_csv, "wb") as f:
	writer = csv.DictWriter(f, fieldnames=fieldnames)
	writer.writeheader()
	writer.writerows(physdescs_info)
