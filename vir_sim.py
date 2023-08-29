from math import inf
from queue import Queue

from .base import Position
from .sim_map import VacuumCleanerMap
from .robots import VacuumCleaner
from .utils import ConfigParser


class _BaseSimulator:
    def __init__(
        self,
        robot: VacuumCleaner,
        map: VacuumCleanerMap
    ) -> None:
        self.robot = robot
        self.map = map
        self.time_counter = 0


class VacuumCleanerSimulator(_BaseSimulator):
    def __init__(
        self,
        robot: VacuumCleaner,
        map: VacuumCleanerMap,
        config: ConfigParser,
    ) -> None:
        super().__init__(robot, map)
        self.history_queue = Queue()
        self.config = config
        self.time_out = self.config.data.sim.time_out

    def run(self):
        self.stop = False
        for time in range( self.time_out ):
            self.time_counter += 1

            self.history_queue.put( self.robot.position )

            # Give user visiable map to robot
            map_info = self.map.get_info()

            # Compute new position by user algorithm
            new_position = self.robot.algorithms( map_info )

            # Update by new position
            self.robot.action( new_position, self.map )
            self.map.update( self.robot )

            # Check if simuation is finished.
            if self.terminate():
                self.stop = True

            self.log( time )

            if self.stop:
                break

        if self.time_counter == self.time_out:
            print("Terminated by time out!!!!")
        print(f"[Comsumed Time] {self.time_counter}")

    def terminate( self ):
        is_terminate = False

        # Check if robot cannot clean.
        cannot_clean = False
        if self.robot._fuel <= 0:
            cannot_clean = True
        is_terminate = is_terminate or cannot_clean

        # Check if robot can move to another tile.
        if self.robot._move_energy > self.robot._fuel:
            is_terminate = is_terminate or True

        # Check all tile is cleaned.
        percentage_clean = 0
        for y in range( self.map.height ):
            for x in range( self.map.width ):
                cell_remain_energy = self.map.origin_map[y][x].req_energy
                if cell_remain_energy == inf:
                    continue
                percentage_clean += cell_remain_energy

        if percentage_clean == 0:
            is_terminate = is_terminate or True

        return is_terminate

    def evaluate(self):
        remain_energy = 0
        for line in self.map.origin_map:
            for cell in line:
                if cell.req_energy != inf:
                    remain_energy += cell.req_energy
        per_remain_energy = ( 1 - ( remain_energy / self.map._total_enerngy ) ) * 100
        return per_remain_energy

    def log(self, cur_time):
        if not self.config.data.sim.skip:
            self._non_skip_log(cur_time)
        elif self.config.data.sim.skip and ( self.time_counter == self.time_out or self.stop ):
            self._skip_log(cur_time)

    def _non_skip_log(self, cur_time):
        pos: Position = self.history_queue.get()
        if pos != self.robot.position:
            print(f"Time {cur_time + 1}", "-" * 20)
            self.map.show_robot_map()
            print(f"[ Robot Status ]")
            print(f"Robot.fuel = {self.robot._fuel}")
            print(f"Robot.pos = ({self.robot.position.x}, {self.robot.position.y})")
            print(f"Robot.Consumption = {self.robot._energy_consumption}")
            print(f"Robot.MoveConsumption = {self.robot._move_energy}")

            print(f"\n[ Move log ]")
            print(f'({pos.x}, {pos.y})->({self.robot.position.x}, {self.robot.position.y})')

            print(f"\n[ Evaluation ]")
            print("{:.2f} %".format( self.evaluate() ))

    def _skip_log(self, cur_time):
        print(f"Time {cur_time + 1}", "-" * 20)
        self.map.show_robot_map()
        print(f"[ Robot Status ]")
        print(f"Robot.fuel = {self.robot._fuel}")
        print(f"Robot.pos = ({self.robot.position.x}, {self.robot.position.y})")
        print(f"Robot.Consumption = {self.robot._energy_consumption}")
        print(f"Robot.MoveConsumption = {self.robot._move_energy}")

        print(f"\n[ Move log ]")
        pos_history = ''
        pre_position = Position( -1, -1 )
        for i in range( self.history_queue.qsize() ):
            pos: Position = self.history_queue.get()
            if (pos.x != pre_position.x ) or (pos.y != pre_position.y):
                pos_history += f'({pos.x}, {pos.y})->'
                pre_position = pos
        pos_history += f'({self.robot.position.x}, {self.robot.position.y})*'
        print(pos_history)

        print(f"\n[ Evaluation ]")
        print("{: .2f} %".format( self.evaluate() ))


