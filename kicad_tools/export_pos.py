import os
import csv
from .fix_rotations import Corrector


def get_pos_files(original_pos_path):
    # PROJECTNAME-bottom-pos.csv and PROJECTNAME-top-pos.csv
    pos_files = []
    try:
        original_files = os.listdir(original_pos_path)
    except FileNotFoundError:
        return []
    for file in original_files:
        if file.endswith("-pos.csv"):
            pos_files.append(file)
    return pos_files


def convert_pos(root_path, pos_folder, output_path, skip_rotations_correction=False):
    corrector = Corrector(root_path)  # will get the rotation rules for apply later
    pos_files_path = os.path.join(root_path, pos_folder)
    pos_files = get_pos_files(pos_files_path)
    if not pos_files:
        return False
    for original_pos_file in pos_files:
        original_pos_abs_path = os.path.join(pos_files_path, original_pos_file)
        new_pos_file = original_pos_file[:-4] + "-jlcpcb.csv"
        new_pos_abs_path = os.path.join(output_path, new_pos_file)
        index = 0
        with open(original_pos_abs_path, 'r') as input_file, open(new_pos_abs_path, 'w') as output_file:
            csv_reader = csv.reader(input_file, delimiter=',')
            csv_writer = csv.writer(output_file, delimiter=',', quoting=csv.QUOTE_MINIMAL)
            csv_writer.writerow(['Designator', 'Mid X', 'Mid Y', 'Layer', 'Rotation'])
            for row in csv_reader:
                index += 1
                if index == 1:  # header ['Ref', 'Val', 'Package', 'PosX', 'PosY', 'Rot', 'Side']
                    continue
                rotation = row[6]
                footprint = row[2]
                if not skip_rotations_correction:
                    rotation = corrector.fix_rotation(rotation, footprint)
                csv_writer.writerow([row[0], row[3], row[4], rotation, row[5]])
        if index < 2:  # only header, delete
            os.remove(new_pos_abs_path)
    return True


if __name__ == "__main__":
    convert_pos("/home/dani/github/SuperPower/PCB_Raspberry_Pi", "tmp", "")
