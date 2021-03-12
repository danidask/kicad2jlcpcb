from xml.dom import minidom
import csv
import os, sys
import logging


logger = logging.getLogger(__name__)


PARTNUMBER_VALID_FIELD_NAMES = ["partnumber", "part_number", "partn", "part_n", "pn"]  # here alwais lowercase


def extract_bom_from_xml(file_path):
    bom = []
    try:
        xmldoc = minidom.parse(file_path)
    except FileNotFoundError:
        logger.error("Couldn't open {}.".format(file_path))
        sys.exit(1)
    itemlist = xmldoc.getElementsByTagName('comp')
    for item in itemlist:
        ref = item.attributes['ref'].value  # KeyError
        value = item.getElementsByTagName("value")[0].firstChild.data
        try:
            footprint = item.getElementsByTagName("footprint")[0].firstChild.data  # IndexError:
        except IndexError:
            footprint = ""
        try:
            fields = item.getElementsByTagName("fields")[0].getElementsByTagName("field")
        except IndexError:  # doesnt have custom fields
            fields = []
        part_number = ""
        keys = []
        for field in fields:
            field_name = field.attributes['name'].value
            field_value = field.firstChild.data
            if field_name.lower() in PARTNUMBER_VALID_FIELD_NAMES:
                part_number = field_value.strip()
            elif field_name.lower() == "keys":
                keys = field_value.split(',')
        keys = [x.strip().upper() for x in keys if x.strip()]  # lowercase all keys, remove remove blanks and empties
        component = {
            "ref": ref,
            "value": value,
            "footprint": footprint.split(':')[-1],  # remove library name
            "part_number": part_number,
            "keys": keys,
        }
        bom.append(component)
    return bom


def generate_jlcpcb_bom(bom, output_path, project_name):
    # Assembly file
    asam_n = 0
    csv_file = os.path.join(output_path, project_name + "_BOM_Assembly.csv")
    try:
        with open(csv_file, 'w', newline='') as csvfile:
            csvwriter = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
            csvwriter.writerow(['Comment', 'Designator', 'Footprint', 'LCSC Part'])
            for line in bom:
                if 'DNP' not in line['keys'] and 'EXCLUDE' not in line['keys']:
                    csvwriter.writerow([line['value'], line['ref'], line['footprint'], line['part_number']])
                    asam_n += 1
    except PermissionError:
        logger.error("Couldn't open {}. Maybe its already open.".format(csv_file))
        sys.exit(1)
    # Remaining file (do not place components)
    dnp_n = 0
    with open(os.path.join(output_path, project_name + "_BOM_Remaining.csv"), 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
        csvwriter.writerow(['Comment', 'Designator', 'Footprint', 'LCSC Part'])
        for line in bom:
            if 'DNP' in line['keys']:
                csvwriter.writerow([line['value'], line['ref'], line['footprint'], line['part_number']])
                dnp_n += 1
    # exclude components (for debug)
    exclude_n = 0
    """
    with open(os.path.join(output_path, "excluded_parts.txt"), 'w') as file:
        file.write("This is a debug file to check the excluded parts\n")
        for line in bom:
            if 'EXCLUDE' in line['keys']:
                file.write("- {}\t{}\n".format(line['ref'], line['value']))
                exclude_n += 1
    """
    for line in bom:
        if 'EXCLUDE' in line['keys']:
            logger.debug("Component excluded from BOM: {} ({})".format(line['ref'], line['value']))
            exclude_n += 1
    return asam_n, dnp_n, exclude_n
