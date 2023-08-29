from typing import List, Optional


class BaseCell:
    def __init__(
        self,
        request_energy: int,
        charger: Optional[bool] = None
    ) -> None:
        r'''
            This data structure is for user's robot. In real world, the robot collects the data
            using its sensor such as inner GPU or encoder. Therefore, this data structure provides
            the data to robot as if the robot collected.
        '''
        self.req_energy = request_energy
        self.charger = charger


class DebugCell(BaseCell):
    def __init__(
        self,
        request_energy: int,
        detect: Optional[bool] = None,
        charger: Optional[bool] = None,
        chance: Optional[int] = None
    ) -> None:
        r'''
            This data structure is an extension of the base cell data structure and is for debugging.
            Also, it is used in simulation to update map information during simulation. It is not used
            for the user's robot.
        '''
        super().__init__(
            request_energy,
            charger=charger
        )
        self.chance = chance
        self.detect = detect


class UserMap:
    def __init__(
        self,
        visible_map: List[List[BaseCell]],
        static: bool,
        width: Optional[int] = None,
        height: Optional[int] = None,
    ) -> None:
        r'''
            This data structure includes the map size and the map data. The robot receives and uses
            this data structure to process. In real world, however, the robot does not know the shape
            of map. Therefore, the user can change to the mode of hiding the shape of map using `static`
            parameter. If `static` mode is off, the user does not need to give map size.

            Example::
                >>> gridMap = UserMap( mapData, True, 33, 33 )
                >>> print( gridMap.width )
                >>> print( gridMap.height )
                >>> x = 1
                >>> y = 6
                >>> cell = gridMap.map[y][x]
                >>> print( cell.req_energy )
                >>> print( cell.charger )
                >>> print( cell.chance )
        '''
        if static:
            self.width = width
            self.height = height
        self.map = visible_map
