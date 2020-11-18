import os
import re
import csv
import logging


logger = logging.getLogger(__name__)


class Corrector:
    def __init__(self, root_path):
        self.global_rules = self._load_global_rules(os.path.join(os.path.dirname(__file__), "cpl_rotations.csv"))
        self.local_rules = self._load_local_rules(root_path)

    def fix_rotation(self, rotation, footprint):
        # first check if in local rules (must match)
        for pattern, correction in self.local_rules.items():
            if footprint.strip() == pattern.strip():
                logger.debug("Footprint {} matched {} (local rules). Applying {} deg correction"
                      .format(footprint, pattern, correction))
                return self._apply_correction(rotation, correction)
        # if not, check global rules (regex)
        for pattern, correction in self.global_rules.items():
            if pattern.match(footprint):
                logger.debug("Footprint {} matched {} (global rules). Applying {} deg correction"
                      .format(footprint, pattern.pattern, correction))
                return self._apply_correction(rotation, correction)
        return rotation

    @staticmethod
    def _load_global_rules(rotations_file):
        """ Return a Dict with all the rotations from global file"""
        rotations = {}
        with open(rotations_file) as csvfile:
            reader = csv.reader(csvfile, delimiter=',')
            for index, row in enumerate(reader):
                if index == 0:  # header
                    continue
                rotations[re.compile(row[0])] = int(row[1])  # regex
        return rotations

    @staticmethod
    def _load_local_rules(root_path):
        """ Return a Dict with all the rotations from local file"""
        rotations = {}
        local_file_path = os.path.join(root_path, "cpl_rotations.csv")
        try:
            with open(local_file_path) as csvfile:
                reader = csv.reader(csvfile, delimiter=',')
                for index, row in enumerate(reader):
                    if index == 0:  # header
                        continue
                    try:
                        rotations[row[0]] = int(row[1])
                    except IndexError:
                        pass  # can be a blank line
        except FileNotFoundError:
            logger.warning("local 'cpl_rotations.csv' file not found. Creating new one...")
            Corrector._create_local_rules(local_file_path)
        return rotations

    @staticmethod
    def _apply_correction(rotation, correction):
        return "{0:.6f}".format((float(rotation) + correction) % 360)

    @staticmethod
    def _create_local_rules(local_rules_path):
        with open(local_rules_path, 'w') as f:
            f.write('"Footprint pattern","Correction"\r\n')


if __name__ == "__main__":
    corrector = Corrector("/home/dani/github/kicad2jlcpcb/tmp")
    original_rotation = 270
    footprint = "SOT-23-5"
    # footprint = "R_0805_2012Metric"
    new_rotation = corrector.fix_rotation(original_rotation, footprint)
    print("Footprint {} Rotation {} -> {}".format(footprint, original_rotation, new_rotation))
