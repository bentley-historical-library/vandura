from lxml import etree
import os
from os.path import join
import csv

from vandura.config import marc_dir

converted_eads = join(marc_dir, "converted_eads_working")
extent_csv = join(marc_dir, "CSVs", "converted_ead_extents.csv")


fieldnames = ["filename", "xpath", "extent", "physfacet", "dimensions"]
physdescs_info = []
for filename in os.listdir(converted_eads):
	print "Extracting physdescs from {}".format(filename)
	tree = etree.parse(join(converted_eads, filename))
	physdescs = tree.xpath("//physdesc")
	for physdesc in physdescs:
		element_counts = {}
		physdesc_path = tree.getpath(physdesc)
		physdesc_info = {"filename":filename, "xpath":physdesc_path}
		for element in physdesc.xpath("./*"):
			element_text = element.text.strip().encode("utf-8")
			element_name = element.tag
			element_counts[element_name] = element_counts.get(element_name, 0) + 1
			if element_counts[element_name] == 1:
				physdesc_info[element_name] = element_text
			else:
				formatted_element_name = element_name + "{}".format(element_counts[element_name] - 1)
				if formatted_element_name not in fieldnames:
					fieldnames.append(formatted_element_name)
				physdesc_info[formatted_element_name] = element_text
		physdescs_info.append(physdesc_info)

with open(extent_csv, "wb") as f:
	writer = csv.DictWriter(f, fieldnames=fieldnames)
	writer.writeheader()
	writer.writerows(physdescs_info)
