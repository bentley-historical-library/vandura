from vandura.config import dspace_mets_dir, dspace_xoai_dir, real_masters_all

from lxml import etree
import urlparse
import requests
import os
from os.path import join
import time

def fetch_dspace_xoai(ead_dir, dspace_mets_dir, dspace_xoai_dir):
    print "Fetching DSpace XOAI"
    filenames = [filename for filename in os.listdir(ead_dir) if filename.endswith('.xml')]
    session = requests.session()
    for filename in filenames:
        tree = etree.parse(join(ead_dir,filename))
        daos = tree.xpath('//dao')
        for dao in daos:
            href = dao.attrib['href'].strip()
            if href.startswith('http://hdl.handle.net/2027.42'):
                handlepath = urlparse.urlparse(href).path
                the_id = handlepath.split('/')[-1]
                xml_filename = the_id + '.xml'
                if xml_filename not in os.listdir(dspace_mets_dir) + os.listdir(dspace_xoai_dir):
                    ns = {"oai":"http://www.openarchives.org/OAI/2.0/"}
                    xoai_url = "https://deepblue.lib.umich.edu/dspace-oai/request?verb=GetRecord&metadataPrefix=xoai&identifier=oai:deepblue.lib.umich.edu:2027.42/" + the_id
                    print "Fetching {0}".format(xoai_url)
                    response = session.get(xoai_url)
                    xoai_xml = etree.fromstring(response.content)
                    if not xoai_xml.xpath("//oai:error", namespaces=ns):
                        with open(join(dspace_xoai_dir, xml_filename),'w') as xoai_out:
                            xoai_out.write(etree.tostring(xoai_xml))
                    time.sleep(15)
    session.close()

def main():
    fetch_dspace_xoai(real_masters_all, dspace_mets_dir, dspace_xoai_dir)

if __name__ == "__main__":
    main()
