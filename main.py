from queue import Queue

from SBSim.utils import (
    ConfigParser,
    args_paser,
    map_selector,
)
from SBSim import VacuumCleanerMap, VacuumCleanerSimulator
from simul import UserRobot


def introduce(config: ConfigParser):
    print(f">>> Simple Robot Sim (SBSim) <<< ")
    print(f'[Simulator]')
    print(f' - mode(skip?): {config.data.sim.skip}')

    print(f'[Robot]')
    print(f' - fuel: {config.data.robot.fuel}')
    print(f' - energy consumption: {config.data.robot.energy_consumption}')
    print(f' - start postion: ({config.data.robot.position_x}, {config.data.robot.position_y})')
    print(f' - vision sight: {config.data.robot.vision_sight}')

    print(f'[Map]')
    print(f' - map name: {config.data.map.name}')
    print(f' - random?: {not config.data.map.fix.enable}')
    print(f' - map size: ({config.data.map.width}, {config.data.map.height})')
    print()


if __name__ == '__main__':
    args = args_paser()
    config: ConfigParser = ConfigParser.parse( args.map )

    # Print introduction
    introduce(config)

    # Create Robot and Map
    robot = UserRobot(
        fuel=config.data.robot.fuel,
        energy_consumption=config.data.robot.energy_consumption,
        move_consumption=config.data.robot.move_consumption,
        postion=[ config.data.robot.position_x, config.data.robot.position_y ],
        vision_sight=config.data.robot.vision_sight,
    )
    grid_map: VacuumCleanerMap = map_selector( config )

    # Print Initial Grid Map
    grid_map.update( robot )
    if config.data.map.debug:
        print("Debug map")
        grid_map.show_real_map()
    print("\nTime : 0 -------")
    grid_map.show_robot_map()

    simulator = VacuumCleanerSimulator(
        robot,
        grid_map,
        config,
    )
    simulator.run()
