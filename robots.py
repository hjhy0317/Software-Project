import random
from typing import List, Tuple
from math import inf

from .sim_map import VacuumCleanerMap
from .base import (
    _BaseRobot, 
    Position, 
    DebugCell,
    STAY,
    MOVE,
    CLEN,
    CHAR,
)


class VacuumCleaner(_BaseRobot):
    def __init__(
        self,
        fuel: int = 100,
        energy_consumption: int = 10,
        move_consumption: int = 10,
        postion: List[int] = [0, 0],
        vision_sight: int = 2
    ) -> None:
        super().__init__(
            fuel=fuel,
            energy_consumption=energy_consumption,
            postion=postion,
            vision_sight=vision_sight
        )
        r'''
            This robot is for cleaning the room. This vacuum cleaner can select behaviors; MOVE, STAY,
            CLEN(Clean), CHAR(Charge). 'energy_consumtion' is used for cleaning and 'move_energy' is 
            used for moving.
        '''
        self._init_fuel = self._fuel
        self._move_energy: int = move_consumption
        self.mode: int = STAY

    def action(self, new_position: Tuple[int], grid_map_obj: VacuumCleanerMap):
        new_position = self.tunning( new_position )
        pred_position: Position = None
        new_pos: Position = Position(new_position[0], new_position[1])
        grid_map: List[List[DebugCell]] = grid_map_obj.origin_map

        # To avoid the robot being out of map
        out_of_map = self._check_out_of_map( new_pos, grid_map_obj )
        if out_of_map:
            print(
                "Warning!!!",
                "The vacuum cleaner robot cannot move target position,"
            )
            return

        # Check the data of target position.
        if self.mode == MOVE:
            if self._fuel > 0:
                pred_position = new_pos
                self._fuel -= self._move_energy
        elif (
            self.mode == CHAR and \
            grid_map[self.position.y][self.position.x].charger and \
            grid_map[self.position.y][self.position.x].chance > 0
        ):
            self._fuel = self._init_fuel
            grid_map[self.position.y][self.position.x].chance -= 1
            if grid_map[self.position.y][self.position.x].chance == 0:
                grid_map[self.position.y][self.position.x].charger = False
        elif self.mode == CLEN:
            grid_energy = grid_map[ self.position.y ][ self.position.x ].req_energy
            grid_energy = grid_energy - self._energy_consumption
            if self._fuel > 0:
                self._fuel -= self._energy_consumption
                if grid_energy < 0:
                    grid_map_obj.origin_map[self.position.y][self.position.x].req_energy = 0
                else:
                    grid_map_obj.origin_map[self.position.y][self.position.x].req_energy = grid_energy

        if pred_position != None and grid_map[pred_position.y][pred_position.x].req_energy != inf:
                self.position = pred_position



