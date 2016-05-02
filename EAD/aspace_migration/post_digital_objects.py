from vandura.shared.scripts.archivesspace_authenticate import authenticate
from vandura.config import ead_dir, dspace_mets_dir, dspace_xoai_dir
from vandura.config import aspace_credentials

import getpass
import requests
from lxml import etree
import os
from os.path import join
import json
import re
import csv
import urlparse
import urllib2
import uuid
import getpass
import time

def build_digital_object_component(digital_object_uri, component_title, component_label, position):
    digital_object_component = {
                            'digital_object':{'ref':digital_object_uri},
                            'title':component_title,
                            'label':component_label,
                            'position':position,
                            }

    return digital_object_component

def post_digital_object_components(session, digital_object_components):
    errors = []
    for component in digital_object_components:
        digital_object_component_post = session.post(aspace_url+'/repositories/2/digital_object_components',data=json.dumps(component)).json()

        if 'error' in digital_object_component_post:
            errors.append(digital_object_component_post)

    return errors

def post_digital_object():
    pass

def post_digital_objects(ead_dir, digital_objects_dir, dspace_mets_dir, dspace_xoai_dir, aspace_url, username, password,delete_csvs=False):

    if not os.path.exists(digital_objects_dir):
        os.makedirs(digital_objects_dir)

    posted_objects = join(digital_objects_dir, 'posted_digital_objects.csv')
    error_file = join(digital_objects_dir, 'digital_object_errors.txt')
    skipped_items_file = join(digital_objects_dir, 'skipped_items.txt')

    if delete_csvs:
        for csvfile in [posted_objects, error_file, skipped_items_file]:
            if os.path.exists(csvfile):
                os.remove(csvfile)

    already_posted = []

    if os.path.exists(posted_objects):
        with open(posted_objects,'rb') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                href = row[0]
                if href not in already_posted:
                    already_posted.append(href)

    s = authenticate(aspace_url, username, password)
    s.headers.update({"Content-type":"application/json"})

     # Iterate through EADs. If you find a dao href that is a DSpace handle, open the METS from the dspace_mets folder
     # Assemble the digital object and the components as such:
     # Digital object title == EAD component title and dates
     # Digital object identifer and file version uri == dao href
     # Digital object component titles = Titles from METS
     # Digital object component labels == Labels from METS
     # First, post the digital object
     # Then, grab the uri from the posted digital object to set as the parent for each component and post those

    posted_dig_objs = {}
    skipped_items = []
    errors = []

    for filename in os.listdir(ead_dir):
        print "Posting digital objects from {0}".format(filename)
        tree = etree.parse(join(ead_dir,filename))
        daos = tree.xpath('//dao')
        for dao in daos:
            # TO DO -- Account for the same href showing up in different places
            href = dao.attrib['href'].strip()
            if href not in already_posted:
                did = dao.getparent()

                show = dao.get("show", "new")
                actuate = dao.get("actuate", "onRequest")
                xlink_actuate = actuate.replace('request','Request').replace('load','Load')

                daodesc = dao.xpath('./daodesc/p')
                if daodesc:
                    digital_object_note = re.sub(r'^\[|\]$','',daodesc[0].text)
                else:
                    digital_object_note = False

                component_title = etree.tostring(did.xpath('./unittitle')[0])
                digital_object_title = re.sub(r'<(.*?)>','',component_title).strip()

                digital_object = {}
                digital_object['title'] = digital_object_title
                digital_object['digital_object_id'] = str(uuid.uuid4())
                digital_object['publish'] = True
                digital_object['file_versions'] = [{'file_uri':href,'xlink_show_attribute':show,'xlink_actuate_attribute':xlink_actuate}]
                if digital_object_note:
                    digital_object['notes'] = [{'type':'note','publish':True,'content':[digital_object_note.strip()],'jsonmodel_type':'note_digital_object'}]

                digital_object_post = s.post(aspace_url+'/repositories/2/digital_objects',data=json.dumps(digital_object)).json()

                if 'invalid_object' in digital_object_post:
                    errors.append(digital_object_post)

                digital_object_uri = digital_object_post['uri']

                posted_dig_objs[href] = digital_object_uri

                if href.startswith("http://hdl.handle.net/2027.42"):
                    handlepath = urlparse.urlparse(href).path
                    the_id = handlepath.split('/')[-1]
                    xml_filename = the_id + ".xml"
                    digital_object_components = []
                    if xml_filename in os.listdir(dspace_mets_dir):
                        metstree = etree.parse(join(dspace_mets_dir, xml_filename))
                        ns = {'mets':'http://www.loc.gov/METS/','dim': 'http://www.dspace.org/xmlns/dspace/dim','xlink':'http://www.w3.org/TR/xlink/'}
                        XLINK = 'http://www.w3.org/TR/xlink/'

                        fileGrp = metstree.xpath("//mets:fileGrp[@USE='CONTENT']",namespaces=ns)[0]
                        bitstreams = fileGrp.xpath('.//mets:file',namespaces=ns)
                        position = 0
                        for bitstream in bitstreams:
                            #component_size = bitstream.attrib['SIZE']
                            #component_href = 'http://deepblue.lib.umich.edu' + FLocat.attrib['{%s}href' % (XLINK)] 

                            FLocat = bitstream.xpath('./mets:FLocat',namespaces=ns)[0]
                            component_title = FLocat.attrib['{%s}title' % (XLINK)].strip()
                            if '{%s}label' % (XLINK) in FLocat.attrib:
                                component_label = FLocat.attrib['{%s}label' % (XLINK)].strip()[:255]
                            else:
                                component_label = None
                            
                            digital_object_components.append(build_digital_object_component(digital_object_uri, component_title, component_label, position))
                            errors.extend(post_digital_object_components(s, digital_object_components))

                            position += 1
                    elif xml_filename in os.listdir(dspace_xoai_dir):
                        xoaitree = etree.parse(join(dspace_xoai_dir, xml_filename))
                        ns = {'xoai':'http://www.lyncode.com/xoai'}

                        originals = xoaitree.xpath("//xoai:field[text()='ORIGINAL']", namespaces=ns)[0]
                        bitstreams = originals.xpath(".//xoai:element[@name='bitstream']", namespaces=ns)
                        position = 0
                        for bitstream in bitstreams:
                            component_title = bitstream.xpath("./field[@name='name']", namespaces=ns)[0].text.strip()
                            if bitstream.xpath("./field[@name='description']", namespaces=ns):
                                component_label = bitstream.xpath("./field[@name='description']", namespaces=ns)[0].text.strip()[:255]
                            else:
                                component_label = None

                            digital_object_components.append(build_digital_object_component(digital_object_uri, component_title, component_label, position))
                            errors.extend(post_digital_object_components(s, digital_object_components))

                            position += 1
                    else:
                        skipped_items.append(href)

            if errors:
                with open(error_file, "w") as f:
                    f.write("\n".join(errors))

            if skipped_items:
                with open(skipped_items_file, "w") as f:
                    f.write("\n".join(skipped_items))

            posted_data = [[href, uri] for href, uri in posted_dig_objs.iteritems()]
            with open(posted_objects, "ab") as f:
                writer = csv.DictWriter(f)
                writer.writerows(posted_data)

    #s.post("{}/logout".format(aspace_url))

def main():
    aspace_ead_dir = join(ead_dir, 'eads')
    digital_objects_dir = join(ead_dir,'digital_objects')
    aspace_url, username, password = aspace_credentials()
    post_digital_objects(aspace_ead_dir, digital_objects_dir, dspace_mets_dir, dspace_xoai_dir, aspace_url, username, password, delete_csvs=True)

if __name__ == "__main__":
    main()