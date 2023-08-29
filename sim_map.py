import random
from math import inf
from typing import Dict, List, Optional

from .viewer import GraphicViewer
from .base import (
    _BaseRobot,
    Position,
    DebugCell, 
    BaseCell, 
    UserMap
)

class _BaseGridMap(GraphicViewer):
    def __init__(
        self,
        width: Optional[int] = None,
        height: Optional[int] = None,
        max_energy: int = 20,
        num_obstacle: int = 10,
        debug: bool = False,
        seed: int = 100000,
        fix_factor: bool = False,
        fix_pos: List[List] = [None, None],
    ) -> None:
        super().__init__()
        random.seed(seed)
        # Dedug flag variables
        self._debug = debug

        # Map size variables
        self.width = width
        self.height = height

        # Map configuration variables
        self.origin_map: List[List[DebugCell]] = None
        self._max_energy = max_energy
        self._total_enerngy = 0

        # Obstacle variables.
        self._num_obstacle = num_obstacle
        self._fix_factor = fix_factor
        self._fix_pos = Position(fix_pos[0], fix_pos[1])

        # Check/Store robot's last position at every iteration
        self._latest_robot_position = None

    def _check(self):
        raise NotImplementedError

    def _build(self):
        raise NotImplementedError

    def get_info( self ):
        raise NotImplementedError

    def update( self, robot: _BaseRobot ):
        f'''
            Update map state
            ---
                Update map state using the current robot position.
        '''
        position = robot.position
        vision_sight = robot._vision_sight

        if self._latest_robot_position == None:
            self.origin_map[ position.x ][ position.y ].req_energy = 0

        low_w = position.x - vision_sight
        low_h = position.y - vision_sight
        upp_w = position.x + vision_sight + 1
        upp_h = position.y + vision_sight + 1

        if low_w < 0:
            low_w = 0
        if low_h < 0:
            low_h = 0
        if upp_w > self.width:
            upp_w = self.width
        if upp_h > self.height:
            upp_h = self.height

        for h in range(low_h, upp_h):
            for w in range(low_w, upp_w):
                self.origin_map[h][w].detect = True

        self._latest_robot_position = position


class VacuumCleanerMap(_BaseGridMap):
    def __init__(
        self,
        width: Optional[int] = None,
        height: Optional[int] = None,
        max_energy: int = 20,
        num_obstacle: int = 10,
        debug: bool = False,
        seed: int = 100000,
        fix_factor: bool = False,
        fix_pos: List[List] = [None, None],
        charger_chance: Optional[int] = None,
        charger_pos: Optional[List[List]] = None,
    ) -> None:
        super().__init__(
            width=width, 
            height=height,
            max_energy=max_energy, 
            num_obstacle=num_obstacle, 
            debug=debug, 
            seed=seed,
            fix_factor=fix_factor, 
            fix_pos=fix_pos
        )
        self._charger_chance = charger_chance
        self._charger_pos = Position( charger_pos[0], charger_pos[1] )
        self._check()
        self._build()

    def _check(self):
        if self._num_obstacle != len( self._fix_pos.x ) and self._fix_factor:
            raise Exception("[SBSim] Map build error : Please check number of obstacles again")
        if self._charger_chance == None or self._charger_pos == None:
            raise Exception("[SBSim] Map build error : Please check number of chargers again")

    def _build(self):
        build_map: List[List[Dict]] = []
        pos_w = [ i for i in range(self.width) ]
        pos_h = [ i for i in range(self.height) ]
        obstacles = []
        chargers = []

        ## find chargers
        for x, y in zip( self._charger_pos.x, self._charger_pos.y ):
            chargers.append( (x, y) )

        ## find obstacles
        if not self._fix_factor:
            # random
            for _ in range(self._num_obstacle):
                sel_w = random.choice(pos_w)
                sel_h = random.choice(pos_h)
                while ( (sel_w, sel_h) in obstacles ) or ( (sel_w, sel_h) in chargers ):
                    sel_w = random.choice(pos_w)
                    sel_h = random.choice(pos_h)
                obstacles.append( (sel_w, sel_h) )
        else:
            # static
            for x, y in zip( self._fix_pos.x, self._fix_pos.y ):
                obstacles.append( (x, y) )

        for h in range(self.height):
            build_map.append( [] )
            for w in range(self.width):
                if (w, h) in chargers:
                    map_data = DebugCell(
                        request_energy=0,
                        detect=False,
                        charger=True,
                        chance=self._charger_chance
                    )
                elif (w, h) in obstacles:
                    map_data = DebugCell(
                        request_energy=inf,
                        detect=False,
                        charger=False
                    )
                else:
                    value = random.randint( 0, self._max_energy+1 )
                    map_data = DebugCell(
                        request_energy=value,
                        detect=False,
                        charger=False
                    )
                    self._total_enerngy += value
                build_map[h].append( map_data )

        self.origin_map = build_map

    def get_info( self ):
        user_map: List[ List[ BaseCell ] ] = []
        for h in range( self.height ):
            user_map.append( [] )
            for w in range( self.width ):
                if not self.origin_map[h][w].detect:
                    user_map[h].append(None)
                else:
                    map_data = BaseCell(
                        request_energy=self.origin_map[h][w].req_energy,
                        charger=self.origin_map[h][w].charger
                    )
                    user_map[h].append( map_data )
        return UserMap(user_map, True, self.width, self.height)


