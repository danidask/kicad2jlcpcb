import os
import sys
import argparse
from .export_bom import extract_bom_from_xml, generate_jlcpcb_bom


def create_folder_if_not_exist(folder):
    try:
        os.stat(folder)
    except:
        os.mkdir(folder)


def main():
    parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter, description='Generates BOM and CPL suitable for JLCPCB Assembly Service')
    parser.add_argument('xml_path', type=os.path.abspath, help='Path of xml file (%I from kicad)')
    
    # Check if required aruments exist
    if (len(sys.argv) == 1):
        parser.print_help()
        sys.exit()

	# Parse arguments
    args = parser.parse_args(sys.argv[1:])

    # TODO output file as optional argument to override this
    project_path = os.path.dirname(os.path.abspath(args.xml_path))  
    project_name = os.path.split(project_path)[-1]
    fabrication_folder = "jlcpcb_fab"

    output_path = os.path.join(project_path, fabrication_folder)
    create_folder_if_not_exist(output_path)

    bom = extract_bom_from_xml(args.xml_path)
    # print(json.dumps(bom, indent=4))
    generate_jlcpcb_bom(bom, output_path, project_name)
    print("Files generated in {}".format(fabrication_folder))


if __name__ == '__main__':
    main()
