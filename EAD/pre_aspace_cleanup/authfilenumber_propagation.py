from lxml import etree
import os
from os.path import join

from vandura.config import real_masters_all

special_cases = {'University of Michigan--Dearborn':'http://id.loc.gov/authorities/names/n79069136',
				'University of Michigan--Flint':'http://id.loc.gov/authorities/names/n79128281',
				'University of Michigan--Dearborn. Department of History':'',
				'University of Wisconsin--Milwaukee':'http://id.loc.gov/authorities/names/n79046004',
				'Lutheran Church--Missouri Synod':''}


def build_text_to_authfilenumber_dict(ead_dir):
	print "Building text_to_authfilenumber_dict"
	text_to_authfilenumber_dict = {}
	filenames = [filename for filename in os.listdir(ead_dir) if filename.endswith('.xml')]
	for filename in filenames:
		print "Building text to authfilenumber dict from {}".format(filename)
		tree = etree.parse(join(ead_dir,filename))
		for subject in tree.xpath('//controlaccess/*'):
			if subject.text and 'authfilenumber' in subject.attrib:
				subject_text = subject.text.strip().rstrip('.').encode('utf-8')
				if subject.tag in ['corpname','persname','famname'] and '--' in subject_text:
					subject_texts = subject_text.split('--')
					joined = '--'.join(subject_texts[0:2]).rstrip(".")
					if joined in special_cases.keys():
						subject_text = joined
					else:
						subject_text = subject_texts[0]
				authfilenumber = subject.attrib['authfilenumber']
				if subject_text not in text_to_authfilenumber_dict:
					text_to_authfilenumber_dict[subject_text] = authfilenumber

	for special_case in special_cases:
		if special_case in text_to_authfilenumber_dict.keys():
			text_to_authfilenumber_dict[special_case] = special_cases[special_case]

	return text_to_authfilenumber_dict

def apply_authfilenumbers(text_to_authfilenumber_dict, ead_dir):
	filenames = [filename for filename in os.listdir(ead_dir) if filename.endswith('.xml')]
	for filename in filenames:
		print "Propagating authfilenumbers in {0}".format(filename)
		tree = etree.parse(join(ead_dir,filename))
		rewrite = False
		for subject in tree.xpath('//controlaccess/*'):
			subject_text = subject.text.strip().rstrip('.').encode('utf-8')
			if subject.tag in ['corpname','persname','famname'] and '--' in subject_text:
				subject_texts = subject_text.split('--')
				joined = '--'.join(subject_texts[0:2]).rstrip(".")
				if joined in special_cases.keys():
					subject_text = joined
				else:
					subject_text = subject_texts[0]
			if subject_text in text_to_authfilenumber_dict:
				rewrite = True
				subject.attrib['authfilenumber'] = text_to_authfilenumber_dict[subject_text]
		if rewrite:
			with open(join(ead_dir,filename),'w') as f:
				f.write(etree.tostring(tree,encoding='utf-8',xml_declaration=True,pretty_print=True))

def misassigned_authfilenumber_fixes(ead_dir):
	auth_to_text = {"http://id.loc.gov/authorities/names/n79045539": "Detroit (Mich.)", 
					"http://id.loc.gov/authorities/names/n79022219": "Ann Arbor (Mich.)",
					"http://id.loc.gov/authorities/names/n81129560": "Benton Harbor (Mich.)",
					"http://id.loc.gov/authorities/names/n00086557": "Willow Run (Mich.)"
					}
	filenames = [filename for filename in os.listdir(ead_dir) if filename.endswith(".xml")]
	for filename in filenames:
		print "Resolving misassigned authfilenumber issues in {}".format(filename)
		tree = etree.parse(join(ead_dir, filename))
		rewrite = False
		for geogname in tree.xpath("//controlaccess/geogname"):
			if geogname.get("authfilenumber","") in auth_to_text.keys() and geogname.text.strip() != auth_to_text[geogname.attrib["authfilenumber"]]:
				rewrite = True
				del geogname.attrib["authfilenumber"]
		if rewrite:
			with open(join(ead_dir,filename),'w') as f:
				f.write(etree.tostring(tree,encoding='utf-8',xml_declaration=True,pretty_print=True))

def authfilenumber_propagation(ead_dir):
	text_to_authfilenumber_dict = build_text_to_authfilenumber_dict(ead_dir)
	apply_authfilenumbers(text_to_authfilenumber_dict, ead_dir)
	misassigned_authfilenumber_fixes(ead_dir)

def main():
	authfilenumber_propagation(real_masters_all)

if __name__ == "__main__":
	main()