from math import inf
from typing import Dict, List
from .base import (
    Position, 
    DebugCell
)

expr_design = {
    'robot':        '🚕',
    'not_detect':   '🟪',
    'no_energy':    '..',
    'low_energy':   '🟨',
    'mid_energy':   '🟧',
    'high_energy':  '🟥',
    'obstacle':     '🔵',
    'charger':      '🔋',
    'no_chance':    '🐈',
}

class UnicodeViewer:
    def __init__(self) -> None:
        # Map configuration variables
        self.origin_map: List[List[DebugCell]] = None
        self._max_energy: int = None

        # Check/Store robot's last position at every iteration
        self._latest_robot_position: Position = None

    def show_robot_map(self):
        raise NotImplementedError

    def show_real_map(self):
        raise NotImplementedError


class GraphicViewer(UnicodeViewer):
    def __init__(self) -> None:
        super().__init__()

    def show_robot_map(self):
        robot_x = self._latest_robot_position.x
        robot_y = self._latest_robot_position.y

        for h in range( len(self.origin_map) ):
            for w in range( len(self.origin_map[h]) ):
                grid_egy_expr = None
                grid_detect = self.origin_map[h][w].detect
                grid_energy = self.origin_map[h][w].req_energy
                grid_energy_degree = grid_energy / self._max_energy

                if grid_energy == 0:
                    grid_egy_expr = expr_design['no_energy']
                elif grid_energy == inf:
                    grid_egy_expr = expr_design['obstacle']
                elif grid_energy_degree < 0.33:
                    grid_egy_expr = expr_design['low_energy']
                elif 0.33 < grid_energy_degree < 0.66:
                    grid_egy_expr = expr_design['mid_energy']
                else:
                    grid_egy_expr = expr_design['high_energy']

                if self.origin_map[h][w].charger != None:
                    grid_charger = self.origin_map[h][w].charger
                    grid_egy_expr = expr_design['charger'] if grid_charger else grid_egy_expr
                    grid_egy_expr = expr_design['no_chance'] if self.origin_map[h][w].chance == 0 else grid_egy_expr

                map_state = grid_energy if grid_detect else None
                view_data = ""

                if w + 1 == len(self.origin_map[h]):
                    if map_state == None:
                        view_data += expr_design['robot'] if w == robot_x and h == robot_y else expr_design['not_detect']
                    else:
                        view_data += expr_design['robot'] if w == robot_x and h == robot_y else grid_egy_expr
                    print(view_data)
                else:
                    if map_state == None:
                        view_data += expr_design['robot'] if w == robot_x and h == robot_y else expr_design['not_detect']
                    else:
                        view_data += expr_design['robot'] if w == robot_x and h == robot_y else grid_egy_expr
                    print(view_data, end='')

    def show_real_map(self):
        robot_x = self._latest_robot_position.x
        robot_y = self._latest_robot_position.y

        for h in range( len(self.origin_map) ):
            for w in range( len(self.origin_map[h]) ):
                grid_egy_expr = None
                grid_detect = self.origin_map[h][w].detect
                grid_energy = self.origin_map[h][w].req_energy
                grid_energy_degree = grid_energy / self._max_energy

                if grid_energy == 0:
                    grid_egy_expr = expr_design['no_energy']
                elif grid_energy == inf:
                    grid_egy_expr = expr_design['obstacle']
                elif grid_energy_degree < 0.33:
                    grid_egy_expr = expr_design['low_energy']
                elif 0.33 < grid_energy_degree < 0.66:
                    grid_egy_expr = expr_design['mid_energy']
                else:
                    grid_egy_expr = expr_design['high_energy']

                if self.origin_map[h][w].charger != None:
                    grid_charger = self.origin_map[h][w].charger
                    grid_egy_expr = expr_design['charger'] if grid_charger else grid_egy_expr
                    grid_egy_expr = expr_design['no_chance'] if self.origin_map[h][w].chance == 0 else grid_egy_expr

                view_data = ""

                if w + 1 == len(self.origin_map[h]):
                    view_data += expr_design['robot'] if w == robot_x and h == robot_y else grid_egy_expr
                    print(view_data)
                else:
                    view_data += expr_design['robot'] if w == robot_x and h == robot_y else grid_egy_expr
                    print(view_data, end='')

