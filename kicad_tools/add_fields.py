import glob
import os

# This script will add PartNumber field to all components in schematic
F4_LINE = 'F 4 "" H {} {} 50  0001 C CNN "PartNumber"\n'
F5_LINE = 'F 5 "" H {} {} 50  0001 C CNN "Keys"\n'


def add_fields(sch_path):
    # Find schematic files and rename it as backup
    schematic_files = glob.glob(os.path.join(sch_path, '*.sch'))
    for schematic_file in schematic_files:
        backup_file = schematic_file + ".bak"
        os.rename(schematic_file, backup_file)
        # F4 is the PartNumber field, by default kicad only add up to F3 (datasheet)
        # Find F3 line and the next line should be F4, if not add F4 & F5 with same position as F3
        with open(backup_file, 'r',encoding='utf8') as input_file, open(schematic_file, 'w', newline='',encoding='utf8') as output_file:
            found_F3 = False
            f3x = 0
            f3y = 0
            for line in input_file.readlines():
                if found_F3:
                    # F 4 goes after F 3
                    # check if F 4 is already there, add otherwise
                    found_F3 = False
                    if not line.startswith("F 4"):
                        line = F4_LINE.format(f3x, f3y) + F5_LINE.format(f3x, f3y) + line
                elif line.startswith("F 3"):
                    found_F3 = True
                    # save coordinates of F3 because F4 & F5 will have the same
                    parts= line.split()
                    f3x = parts[4]
                    f3y = parts[5]
                output_file.write(line)                


if __name__ == "__main__":
    add_fields("/")
