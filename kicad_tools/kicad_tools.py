import os
import sys
import argparse
import json
from .export_bom import extract_bom_from_xml, generate_jlcpcb_bom
from .export_pos import convert_pos


def create_folder_if_not_exist(folder):
    try:
        os.stat(folder)
    except:
        os.mkdir(folder)


def main():
    parser = argparse.ArgumentParser(description='Generates BOM and CPL suitable for JLCPCB Assembly Service')
    parser.add_argument('xml_path', type=os.path.abspath, help="Path of xml file (%%I from kicad)")
    parser.add_argument('-j', '--json', action='store_true', help='Saves json file (for debug)')
    parser.add_argument('-p', '--pos_folder', metavar='folder', type=str, default='.', help='Relative path of pos files (default: project root)')

    # Parse arguments
    args = parser.parse_args()

    # TODO output file as optional argument to override this
    project_path = os.path.dirname(os.path.abspath(args.xml_path))
    project_name = os.path.split(project_path)[-1]  # not realy but we'll use folder name as project name
    fabrication_folder = "jlcpcb_fab"

    output_path = os.path.join(project_path, fabrication_folder)
    create_folder_if_not_exist(output_path)

    bom = extract_bom_from_xml(args.xml_path)
    if args.json:
        with open(os.path.join(output_path, "import.json"), 'w') as f:
            json.dump(bom, f, indent=4)
    asam_n, dnp_n, exclude_n = generate_jlcpcb_bom(bom, output_path, project_name)
    print("{} Assambley parts, {} DNP parts, {} Excluded parts".format(asam_n, dnp_n, exclude_n))
    status = convert_pos(project_path, args.pos_folder, output_path)
    if not status:
        print("ERROR no pos files found in {}".format(project_path))
        print("See README.md to find out how to generate them or look in another path")
    else:
        print("Files generated in {}".format(fabrication_folder))


if __name__ == '__main__':
    main()
