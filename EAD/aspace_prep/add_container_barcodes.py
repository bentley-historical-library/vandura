from lxml import etree
import os
from os.path import join
import uuid
import re

def make_barcode(seen_barcodes):
    barcode = re.sub(r'[A-Za-z\-]','',str(uuid.uuid4()))
    if barcode not in seen_barcodes:
        return barcode
    else:
        make_barcode(seen_barcodes)

def add_container_barcodes(ead_dir):
    # EADs for which box numbering restarts with each subgroup
    subgrp_filenames = ['kelseymu.xml']
    # Alumni Association EADs. Several of the same containers show up in both EADs.
    alumni_filenames = ['alumasso.xml','alumphot.xml']
    alumni_barcodes = {}

    existing_barcodes = re.compile(r'\[[0-9]+\]$')

    av_boxes = {}
    dvd_boxes = {}
    cd_boxes = {}
    sr_boxes = {}
    sd_boxes = {}

    seen_barcodes = []

    # The same AV boxes and DVD boxes may appear in multiple collections -- they should all have the same barcode
    for filename in os.listdir(ead_dir):
        print "Checking for AV Boxes in {0}".format(filename)
        tree = etree.parse(join(ead_dir,filename))
        components = tree.xpath("//dsc//*[starts-with(local-name(), 'c0')]")
        for component in components:
            containers = component.xpath('./did/container')
            if containers:
                top_container = containers[0]
                indicator = top_container.text.strip()
                label = top_container.attrib['label']
                c_type = top_container.attrib["type"]
                if c_type == 'avbox' and indicator not in av_boxes:
                    barcode = make_barcode(seen_barcodes)
                    seen_barcodes.append(barcode)
                    av_boxes[indicator] = barcode
                if label == 'DVD Box' and indicator not in dvd_boxes:
                    barcode = make_barcode(seen_barcodes)
                    seen_barcodes.append(barcode)
                    dvd_boxes[indicator] = barcode
                if label == 'CD Box' and indicator not in cd_boxes:
                    barcode = make_barcode(seen_barcodes)
                    seen_barcodes.append(barcode)
                    cd_boxes[indicator] = barcode
                if label == "Sound Recordings Box" or "sr" in indicator.lower():
                    if indicator not in sr_boxes:
                        barcode = make_barcode(seen_barcodes)
                        seen_barcodes.append(barcode)
                        sr_boxes[indicator] = barcode
                if label == "Sound Disc" and indicator not in sd_boxes:
                    barcode = make_barcode(seen_barcodes)
                    seen_barcodes.append(barcode)
                    sd_boxes[indicator] = barcode

    for filename in os.listdir(ead_dir):
        print "Adding container barcodes in {0}".format(filename)
        tree = etree.parse(join(ead_dir,filename))
        if filename not in subgrp_filenames and filename not in alumni_filenames:
            container_ids = {}
            components = tree.xpath("//dsc//*[starts-with(local-name(), 'c0')]")
            for component in components:
                containers = component.xpath('./did/container')
                if containers:
                    top_container = containers[0]
                    indicator = top_container.text.strip()
                    label = top_container.attrib['label']
                    c_type = top_container.attrib["type"]
                    container_type_label_num = "{0}{1}{2}".format(c_type, label, indicator)
                    if container_type_label_num not in container_ids:
                        barcode = make_barcode(seen_barcodes)
                        seen_barcodes.append(barcode)
                        if c_type == 'avbox':
                            container_ids[container_type_label_num] = av_boxes[indicator]
                        elif label == 'DVD Box':
                            container_ids[container_type_label_num] = dvd_boxes[indicator]
                        elif label == 'CD Box':
                            container_ids[container_type_label_num] = cd_boxes[indicator]
                        elif label == "Sound Recordings Box" or "sr" in indicator.lower():
                            container_ids[container_type_label_num] = sr_boxes[indicator]
                        elif label == "Sound Disc":
                            container_ids[container_type_label_num] = sd_boxes[indicator]
                        else:
                            container_ids[container_type_label_num] = barcode

            for component in components:
                containers = component.xpath('./did/container')
                if containers:
                    top_container = containers[0]
                    indicator = top_container.text.strip()
                    label = top_container.attrib["label"]
                    c_type = top_container.attrib["type"]
                    container_type_label_num = "{0}{1}{2}".format(c_type, label, indicator)
                    barcode = container_ids[container_type_label_num]
                    if existing_barcodes.search(label):
                        top_container.attrib['label'] = re.sub(r'\[[0-9]+\]','',label).strip()
                    top_container.attrib['label'] = "{0} [{1}]".format(label, barcode)

        elif filename in subgrp_filenames:
            subgrps = tree.xpath('//c01')
            for subgrp in subgrps:
                container_ids = {}
                sub_components = subgrp.xpath(".//*[starts-with(local-name(), 'c0')]")
                for sub_component in sub_components:
                    c_containers = sub_component.xpath('./did/container')
                    if c_containers:
                        top_container = c_containers[0]
                        indicator = top_container.text.strip()
                        label = top_container.attrib["label"]
                        c_type = top_container.attrib["type"]
                        container_type_label_num = "{0}{1}{2}".format(c_type, label, indicator)
                        if container_type_label_num not in container_ids:
                            barcode = make_barcode(seen_barcodes)
                            seen_barcodes.append(barcode)
                            container_ids[container_type_label_num] = barcode

                for sub_component in sub_components:
                    c_containers = subcomponent.xpath('./did/container')
                    if c_containers:
                        top_container = c_containers[0]
                        indicator = top_container.text.strip()
                        c_type = top_container.attrib["type"]
                        label = top_container.attrib["label"]
                        container_type_label_num = "{0}{1}{2}".format(c_type, label, indicator)
                        if existing_barcodes.search(label):
                            container.attrib['label'] = re.sub(r'\[[0-9]+\]','',label).strip()
                        container.attrib['label'] = "{0} [{1}]".format(label, container_ids[container_type_label_num])

        elif filename in alumni_filenames:
            components = tree.xpath("//dsc//*[starts-with(local-name(), 'c0')]")
            for component in components:
                c_containers = component.xpath('./did/container')
                if c_containers:
                    top_container = c_containers[0]
                    indicator = top_container.text.strip()
                    label = top_container.attrib["label"]
                    c_type = top_container.attrib["type"]
                    container_type_label_num = "{0}{1}{2}".format(c_type, label, indicator)
                    if container_type_label_num not in alumni_barcodes:
                        barcode = make_barcode(seen_barcodes)
                        seen_barcodes.append(barcode)
                        alumni_barcodes[container_type_label_num] = barcode

            for component in components:
                c_containers = component.xpath("./did/container")
                if c_containers:
                    top_container = c_containers[0]
                    indicator = top_container.text.strip()
                    c_type = top_container.attrib["type"]
                    label = top_container.attrib["label"]
                    container_type_label_num = "{0}{1}{2}".format(c_type, label, indicator)
                    if existing_barcodes.search(label):
                        container.attrib['label'] = re.sub(r'\[[0-9]+\]','',label).strip()
                    container.attrib['label'] = "{0} [{1}]".format(label, alumni_barcodes[container_type_label_num])

        with open(join(ead_dir,filename),'w') as eadout:
            eadout.write(etree.tostring(tree,xml_declaration=True,encoding="utf-8",pretty_print=True))

def main():
    project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    aspace_ead_dir = join(project_dir, 'eads')
    add_container_barcodes(aspace_ead_dir)

if __name__ == "__main__":
    main()
