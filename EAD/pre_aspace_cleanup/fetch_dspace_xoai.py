from vandura.config import dspace_mets_dir, dspace_xoai_dir, real_masters_all

from lxml import etree
import urlparse
import requests
import os
from os.path import join
from tqdm import tqdm
import time

def fetch_dspace_xoai(ead_dir, dspace_mets_dir, dspace_xoai_dir):
    filenames = [filename for filename in os.listdir(ead_dir) if filename.endswith('.xml')]
    error_dir = join(dspace_xoai_dir, "errors")
    xoai_to_fetch = []
    for filename in filenames:
        print "Extracting DSpace IDs to fetch from {}".format(filename)
        tree = etree.parse(join(ead_dir,filename))
        daos = tree.xpath('//dao')
        for dao in daos:
            href = dao.attrib['href'].strip()
            if href.startswith('http://hdl.handle.net/2027.42'):
                handlepath = urlparse.urlparse(href).path
                the_id = handlepath.split('/')[-1]
                xml_filename = the_id + '.xml'
                if xml_filename not in os.listdir(dspace_mets_dir) + os.listdir(dspace_xoai_dir) + os.listdir(error_dir):
                    if the_id not in xoai_to_fetch:
                        xoai_to_fetch.append(the_id)

    session = requests.session()
    session.headers["User-Agent"] = "BHL"

    count = 1
    for xoai_id in xoai_to_fetch:
        print "{0}/{1} - {2}".format(count, len(xoai_to_fetch), xoai_id)
        xml_filename = "{}.xml".format(xoai_id)
        ns = {"oai":"http://www.openarchives.org/OAI/2.0/"}
        xoai_url = "https://deepblue.lib.umich.edu/dspace-oai/request?verb=GetRecord&metadataPrefix=xoai&identifier=oai:deepblue.lib.umich.edu:2027.42/{}".format(xoai_id)
        response = session.get(xoai_url)
        xoai_xml = etree.fromstring(response.content)
        if not xoai_xml.xpath("//oai:error", namespaces=ns):
            with open(join(dspace_xoai_dir, xml_filename),"w") as xoai_out:
                xoai_out.write(etree.tostring(xoai_xml))
        else:
            with open(join(error_dir, xml_filename), "w") as error_out:
                error_out.write(etree.tostring(xoai_xml))
        time.sleep(5)
        count += 1

    session.close()

def main():
    fetch_dspace_xoai(real_masters_all, dspace_mets_dir, dspace_xoai_dir)

if __name__ == "__main__":
    main()
