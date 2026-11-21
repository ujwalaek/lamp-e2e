"""Sanity check: can LAMP's core (non-simulator) modules be imported under Python 3?"""
from _lamp_path import setup
setup()

from Config import Config
Config.declare_config("Packing", "MagneticGripper")
import useful_functions  # noqa
from src.utilities.RelativeOccupancyMapping import RelativeOccupancyMap  # noqa
from src.utilities.DataAugmentation import DataAugmenter  # noqa
from src.utilities.TransitionClusters import TransitionClusters  # noqa
from src.data_structures.WorldModel import WorldModel  # noqa

print("imports ok")
print("DATA_MISC_DIR:", Config.DATA_MISC_DIR)
print("gripper-can relational bins:", Config.get_discretizer("gripper", "can").relational_n_bins)
print("can-surface relational bins:", Config.get_discretizer("can", "surface").relational_n_bins)
