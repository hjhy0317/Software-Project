from math import inf
from typing import List, Tuple

class Position:
    def __init__(
        self,
        x: int,
        y: int,
    ) -> None:
        r'''
            This data structure is to show the position of robot.
        '''
        self.x = x
        self.y = y

class _BaseRobot:
    def __init__(
        self,
        fuel: int = 100,
        energy_consumption: int = 10,
        postion: List[int] = [ 0, 0 ],
        vision_sight: int = 2,
    ) -> None:
        '''
            Base/Simple Robot
            ---
                In this code file(robot.py), we define the base robot used in SBSim. '_BaseRobot' is
                a base-type robot, which is a baseline to other robots. It only has 'moving' function.

                'Robot' has 4 variables basically. 'fuel' means the energy of robot used in moving/
                performing tasks. 'energy_consumption' means the energy used when the robot moving/
                performing tasks. Therefore, the robot can not move/perform tasks when 'fuel' is 0.
                'position' shows the current position of robot. And, 'vision_sight' means the maximum
                distance the robot can see.
        '''
        # visible to User
        self.position = Position( postion[0], postion[1] )

        # non-visible to User
        ## Fuel and Charge variables
        self._fuel = fuel
        self._energy_consumption = energy_consumption

        ## Relate with robot position and user algorithm
        self._vision_sight = vision_sight

    def action(self, Any):
        raise NotImplementedError

    def algorithms(self, Any):
        # This part is for users.
        raise NotImplementedError

    def _check_out_of_map(self, next_pos: Position, map ):
        is_out_map = False
        is_obstacle = False

        if next_pos.x >= map.width or next_pos.x < 0:
            is_out_map = True
        if next_pos.y >= map.height or next_pos.y < 0:
            is_out_map = True

        if not is_out_map:
            if map.origin_map[next_pos.y][next_pos.x].req_energy == inf:
                is_obstacle = True

        can_move = is_out_map or is_obstacle
        return can_move

    def tunning(self, new_pos: Tuple[int]):
        vec_pos_x = new_pos[0] - self.position.x
        vec_pos_y = new_pos[1] - self.position.y

        if abs(vec_pos_x) > 1:
            if vec_pos_x < 0:
                vec_pos_x = -1
            elif vec_pos_x > 0:
                vec_pos_x = 1
        if abs(vec_pos_y) > 1:
            if vec_pos_y < 0:
                vec_pos_y = -1
            elif vec_pos_y > 0:
                vec_pos_y = 1

        next_pos = [None, None]
        next_pos[0] = self.position.x + vec_pos_x
        next_pos[1] = self.position.y + vec_pos_y

        if vec_pos_x != 0 and vec_pos_y != 0:
            # next_pos[0] = self.position.x
            next_pos[0] = 0
            next_pos[1] = 0

        return ( next_pos[0], next_pos[1] )

