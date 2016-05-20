from vandura.config import marc_dir

from lxml import etree
import os
from os.path import join
import re

def make_acqinfo_from_odd(marc_dir):
	converted_eads = join(marc_dir, "converted_eads")

	for filename in os.listdir(converted_eads):
		print "Making acqinfo from odd in {}".format(filename)
		tree = etree.parse(join(converted_eads, filename))
		odds = tree.xpath("//odd")
		rewrite = False
		for odd in odds:
			p = odd.xpath("./p")
			note_text = p[0].text.strip()
			if "donor" in note_text.lower():
				rewrite = True
				acqinfo = etree.Element("acqinfo")
				acqinfo.text = note_text
				odd_parent = odd.getparent()
				odd_parent.insert(odd_parent.index(odd)+1, acqinfo)
				odd_parent.remove(odd)

		if rewrite:
			with open(join(converted_eads, filename), 'w') as f:
				f.write(etree.tostring(tree, encoding="utf-8", xml_declaration=True, pretty_print=True))


def normalize_extents(marc_dir):
	converted_eads = join(marc_dir, 'converted_eads')

	no_extents = []

	extents_to_add = {
					"05113.xml":["3 boxes"],
					"2008014.xml":["14 bundles"],
					"2008059.xml": ["22 volumes"],
					"2012089.xml":["8 oversize boxes","2 bundles"]
	}

	for filename in os.listdir(converted_eads):
		print "Normalizing extents in {}".format(filename)
		tree = etree.parse(join(converted_eads, filename))
		extents = tree.xpath("//extent")
		if extents:
			for extent in extents:
				extent_statement = extent.text.replace(r"&lt;","").replace(r"&gt;","").strip()
				starts_with_digits = re.compile(r"^\d")
				starts_without_digits = re.compile(r"^[^\d]")
				starts_with_digit_letter = re.compile(r"^\d[A-Za-z]")
				if extent_statement.endswith(";"):
					extent_statement = re.sub(r";$","",extent_statement).strip()
				extent_statement = re.sub(r"linear ft\.?","linear feet",extent_statement)
				if extent_statement.startswith("v.") or extent_statement.startswith("v "):
					extent_statement = "1 " + extent_statement
				extent_statement = re.sub(r"\bv\b\.?","volumes",extent_statement)
				if extent_statement.startswith("One"):
					extent_statement.replace("One","1")
				if extent_statement.startswith("."):
					extent_statement = "0" + extent_statement
				if extent_statement.endswith(";"):
					extent_statement = re.sub(r";$","",extent_statement)
				if extent_statement.lower().startswith("ca"):
					approximation = re.findall(r"^[A-Za-z\.]+\s?",extent_statement)
					extent_statement = extent_statement.replace(approximation[0], "")
					extent_statement += " (number approximate)"
				if starts_with_digits.match(extent_statement):
					extent_number = re.findall(r"[\d\,]+", extent_statement)[0]
					if "," in extent_number:
						extent_number_sanitized = extent_number.replace(",", "")
						extent_statement = extent_statement.replace(extent_number, extent_number_sanitized)
				if "[" in extent_statement:
					extent_statement = extent_statement.replace("[", "").replace("]", "")
				if starts_with_digit_letter.match(extent_statement):
					extent_statement = re.sub(r"^(\d+)([A-Za-z])", r"\1 \2", extent_statement)
				if starts_without_digits.match(extent_statement):
					extent_statement = "1 " + extent_statement + " [fake number supplied]"
				extent.text = extent_statement.strip()
			
			with open(join(converted_eads, filename), 'w') as f:
				f.write(etree.tostring(tree, encoding="utf-8", xml_declaration=True, pretty_print=True))
		else:
			if filename in extents_to_add:
				archdesc_did = tree.xpath("//archdesc/did")[0]
				file_extents = extents_to_add[filename]
				for file_extent in file_extents:
					physdesc = etree.Element("physdesc")
					extent = etree.SubElement(physdesc, "extent")
					extent.text = file_extent
					archdesc_did.append(physdesc)

				with open(join(converted_eads, filename), 'w') as f:
					f.write(etree.tostring(tree, encoding="utf-8", xml_declaration=True, pretty_print=True))
			else:
				no_extents.append(filename)

	print "THESE DO NOT HAVE AN EXTENT"
	print "\n".join(no_extents)