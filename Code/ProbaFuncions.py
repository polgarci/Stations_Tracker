from utils import *
from SearchAlgorithm import *
from SubwayMap import *


ROOT_FOLDER = 'Code/'
map = Map()
map = read_station_information(os.path.join(ROOT_FOLDER, 'Stations.txt'))
connections = read_cost_table(os.path.join(ROOT_FOLDER, 'Time.txt'))
map.add_connection(connections)

infoVelocity_clean = read_information(os.path.join(ROOT_FOLDER, 'InfoVelocity.txt'))
map.add_velocity(infoVelocity_clean)



print(map.stations)












