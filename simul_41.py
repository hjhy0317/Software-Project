from typing import List
from math import inf
from SBSim import (
    VacuumCleaner,
    STAY,
    MOVE,
    CLEN,
    CHAR,
)
from SBSim.base import UserMap
'''
    WARNING
    Do not change def name, arguments and return.
    ---
'''

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

class UserRobot(VacuumCleaner):
    def __init__(
        self,
        fuel: int = 100,
        energy_consumption: int = 10,
        move_consumption: int = 10,
        postion: List[int] = ...,
        vision_sight: int = 2
    ) -> None:
        super().__init__(
            fuel=fuel,
            energy_consumption=energy_consumption, 
            move_consumption=move_consumption,
            postion=postion, 
            vision_sight=vision_sight
        )
        '''
            If you want to store some values, define your variables here.
            Using `self`-based variables, you can re-call the value of previous state easily.
        '''
        self.dir_x = 0
        self.dir_y = 0
        self.visit_map = None

    def algorithms( self, grid_map: UserMap ):
        '''
            You can code your algorithm using robot.position and map.information. The following
            introduces accessible data; 1) the position of robot, 2) the information of simulation
            map.

            Here, you should build an algorithm that determines the next action of 
            the robot.

            Robot::
                - position (list-type) : (x, y)
                - mode (int-type) ::
                    You can determine robot state using 'self.mode', and we provide 4-state.
                    (STAY, MOVE, CLEN, CHAR)
                    Example::
                        1) You want to move the robot to target position.
                        >>> self.mode = MOVE
                        2) Clean-up tail.
                        >>> self.mode = CLEN
            
            map::
                - grid_map :
                    grid_map.height : the value of height of map.
                        Example::
                            >>> print( grid_map.height )

                    grid_map.width : the value of width of map.
                        Example::
                            >>> print( grid_map.width )

                    grid_map[ <height/y> ][ <width/x> ] : the data of map, it consists of 2-array.
                        - grid_map[<h>][<w>].req_energy : the minimum energy to complete cleaning.
                            It is assigned randomly, and it is int-type data.
                        - grid_map[<h>][<w>].charger : is there a charger in this tile? boolean-type data.
                        Example::
                            >>> x = self.position.x
                            >>> y = self.position.y
                            >>> print( grid_map[y][x].req_energy )
                            >>> if grid_map[y][x].req_energy > 0:
                            >>>     self.mode = CLEN

            Tip::
                - Try to avoid loop-based codes such as `while` as possible. It will make the problem harder to solve.
        '''


        if not self.visit_map:
            self.visit_map = [[0 for _ in range(grid_map.height)] for _ in range(grid_map.width)]
        robots_pos = [self.position.x, self.position.y]
        self.mode, new_x, new_y = self.get_next_dircetion(grid_map, robots_pos)


        ######################

        ##### DO NOT CHANGE RETURN VARIABLES! #####
        ## The below codes are fixed. The users only determine the mode and/or the next position (coordinate) of the robot.
        ## Therefore, you need to match the variables of return to simulate.
        (new_x, new_y) = self.tunning( [new_x, new_y] )
        return (new_x, new_y)

    def check_out_of_map(self, grid_map, positions):
        pos_x, pos_y = positions
        
        is_out_map = False
        is_obstacle = False

        if pos_x >= grid_map.width or pos_x < 0:
            is_out_map = True
        if pos_y >= grid_map.height or pos_y < 0:
            is_out_map = True

        if not is_out_map:
            if grid_map.map[pos_y][pos_x].req_energy == inf:
                is_obstacle = True

        cant_move = is_out_map or is_obstacle
        return cant_move

    def get_next_dircetion(self, grid_map, robots_pos):
        directions = [[1, 0], [0, -1], [-1, 0], [0, 1]]
        robot_x, robot_y = robots_pos
        mode = MOVE if grid_map.map[robot_y][robot_x].req_energy == 0 else CLEN

        dir_index = -1
        obstacle_cnt = 0
        is_obstacle = True
        can_move = []

        while (dir_index < 3):
            dir_index = dir_index + 1
            dir_x, dir_y = directions[dir_index]
            pos_x = robot_x + dir_x
            pos_y = robot_y + dir_y
            positions = [pos_x, pos_y]
            is_obstacle = self.check_out_of_map(grid_map, positions)

            if (self.dir_x == dir_x * -1 and self.dir_y == dir_y * -1):
                is_obstacle = True

            if is_obstacle:
                obstacle_cnt = obstacle_cnt + 1
            else:
                visit_cnt = self.visit_map[pos_y][pos_x]
                energy = grid_map.map[pos_y][pos_x].req_energy
                can_move.append([visit_cnt, energy*-1, positions, dir_index])
            
            ## print(can_move)

        if obstacle_cnt == 3:
            self.dir_x = self.dir_x * -1
            self.dir_y = self.dir_y * -1
        else:
            best_visit = min(can_move)
            pos_x, pos_y = best_visit[2]
            dir_index = best_visit[3]
            self.visit_map[pos_y][pos_x] = self.visit_map[pos_y][pos_x] + 1
            self.dir_x, self.dir_y = directions[dir_index]

        new_x = robot_x + self.dir_x
        new_y = robot_y + self.dir_y
        return (mode, new_x, new_y)

## while 문 안에 한 번 print
## while 문 나와서 한 번 print