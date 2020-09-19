import os
import sys
import argparse
import json
from .export_bom import extract_bom_from_xml, generate_jlcpcb_bom
from .export_pos import convert_pos
import logging


# Log setup for console (file will be added later)
logFormatter = logging.Formatter("[%(levelname)-7.7s] %(message)s")
logger = logging.getLogger()
consoleHandler = logging.StreamHandler()
consoleHandler.setFormatter(logFormatter)
logger.addHandler(consoleHandler)
logger.setLevel('INFO')


def logger_add_filehandler(path):
    global logger
    fileHandler = logging.FileHandler(os.path.join(path, "kicad2jlcpcb.log"), mode='w')  # override previous file
    fileHandler.setFormatter(logFormatter)
    logger.addHandler(fileHandler)


def create_folder_if_not_exist(folder):
    try:
        os.stat(folder)
    except:
        os.mkdir(folder)


def main():
    parser = argparse.ArgumentParser(description='Generates BOM and CPL suitable for JLCPCB Assembly Service')
    parser.add_argument('xml_path', type=os.path.abspath, help="Path of xml file (%%I from kicad)")
    parser.add_argument('-p', '--pos_folder', metavar='folder', type=str, default='.', help='original pos files path (relative to project) (default: project root)')
    parser.add_argument('-f', '--output_folder', metavar='folder', type=str, default='jlcpcb_fab', help='Output path (relative to project) (default: jlcpcb_fab)')
    parser.add_argument('-s', '--skip_rotations', action='store_true', help='Skips rotations correction')
    parser.add_argument('-j', '--json', action='store_true', help='Saves json file (for debug)')

    # Parse arguments
    args = parser.parse_args()

    project_path = os.path.dirname(os.path.abspath(args.xml_path))
    project_name = os.path.split(project_path)[-1]  # not realy but we'll use folder name as project name
    output_path = os.path.join(project_path, args.output_folder)
    create_folder_if_not_exist(output_path)

    logger_add_filehandler(output_path)

    bom = extract_bom_from_xml(args.xml_path)
    if args.json:
        with open(os.path.join(output_path, "import.json"), 'w') as f:
            json.dump(bom, f, indent=4)
    asam_n, dnp_n, exclude_n = generate_jlcpcb_bom(bom, output_path, project_name)
    logger.info("{} Assambley parts, {} DNP parts, {} Excluded parts".format(asam_n, dnp_n, exclude_n))
    status = convert_pos(project_path, args.pos_folder, output_path, skip_rotations_correction=args.skip_rotations)
    if not status:
        logger.error("No pos files found in {}.\nSee README.md to find out how to generate them or look in another path".format(project_path))
    else:
        logger.info("Files generated in {}".format(output_path))


if __name__ == '__main__':
    main()
