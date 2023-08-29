from typing import Dict
from queue import Queue
import toml
import argparse

from .sim_map import VacuumCleanerMap
from .robots import VacuumCleaner
from .base import Position


class DotDict(dict):
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__

    def __getattr__(*args):
        val = dict.get(*args)
        return DotDict(val) if type(val) is dict else val


class ConfigParser:
    def __init__(self, config: Dict) -> None:
        self._config = DotDict(config)

    @classmethod
    def parse(cls, config_path: str) -> Dict:
        config = toml.load(config_path)
        return cls(config=config)

    # setting read-only attributes
    @property
    def data(self):
        return self._config


def args_paser():
    parser = argparse.ArgumentParser(
            description="Simple Robot Simulator (SBSim), provied by WHY"
        )
    parser.add_argument(
        '-m', '--map',
        type=str, default='./maps/example_map.toml',
        help='Select map for simulation'
        )

    return parser.parse_args()


def map_selector( config: ConfigParser ):
    return VacuumCleanerMap(
        width=config.data.map.width,
        height=config.data.map.height,
        max_energy=config.data.map.max_energy,
        num_obstacle=config.data.map.num_obstacle,
        debug=config.data.map.debug,
        seed=config.data.sim.seed,
        fix_factor=config.data.map.fix.enable,
        fix_pos=[ config.data.map.fix.pos_x, config.data.map.fix.pos_y ],
        charger_chance=config.data.map.charger.chance,
        charger_pos=[ config.data.map.charger.pos_x, config.data.map.charger.pos_y ]
    )

