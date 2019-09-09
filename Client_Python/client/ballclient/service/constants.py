#global variable here
import logging
import datetime
import ballclient.service.strategy as strategy
# log
LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
logger = logging.getLogger('gamelogger')
logger.setLevel(logging.INFO)
timestr = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
f_handler = logging.FileHandler('KUNPENG_gamelog_'+ timestr + '.txt')
f_handler.setLevel(logging.INFO)
f_handler.setFormatter(logging.Formatter(LOG_FORMAT))
logger.addHandler(f_handler)
# constants
team_id = None
team_name = "SingDanceRap" # decided by yourself.
height = 0
width = 0
INF = 10000
EPS = 0.000001
# weights for police mode
w_enemy_police = (4, 0)  # chase or not chase
w_fake_enemy_police = 3
w_power_police = 3
w_wormhole_police = (0.1, -0.1)   # go for wormhole or go away from wormhole
w_player_disc_police_tuple = (-0.1, -2)   # min_player_distance penalty, set to make our players stay away from each other. When there is no enemy or power in visable_area, choose the bigger penalty
w_player_disc_police = -0.1
w_nearest_greatpower_disc_police = 0
w_player_overlay_police = -3
w_last_pos_police = -1   # penalty for going back. True Man Never Turns Back To Watch AN Explosion. HaHa ~~~
# weights for thief mode
w_enemy_thief_tuple = (-8, 8) # when there is only one KUN left and player_point/remain_round < threshold(0.8), chose to suicide.
w_enemy_thief = -8
w_power_thief_tuple = (3, 9) # when there is only one KUN left and player_point/remain_round < threshold(0.8), chose to suicide. The enemy may escape from us instead of chasing us, so heading for power should be a little better because the enemy must be busy eating power.
w_power_thief = 3
w_wormhole_thief = (0.1, -0.1)   # go for wormhole or go away from wormhole
w_bound_X_thief = -0.1
w_bound_Y_thief = -0.1
w_player_disc_thief_tuple = (-1, -2)  # min_player_distance penalty, set to make our players stay away from each other. When there is no enemy or power in visable_area, chose the bigger penalty
w_player_disc_thief = -1
w_exit_tunnel = -0.01
w_thief_future_choice = -16  # because the thiefChoiceCount is usually around 20~70 when searchStep = 5, the penalty should also be bigger
w_mean_enemy_disc_thief = 0
w_min_enemy_Manhaton_disc_thief = -3
w_nearest_greatpower_disc_thief = 0
w_player_overlay_thief = -1.5
w_last_pos_thief = -2   # penalty for going back. True Man Never Turns Back To Watch AN Explosion. HaHa ~~~
w_danger_area = -1.5
# common weights
# when the map is given, the thief_danger_area below can be set manually, otherwise it should be set empty.
# thief_danger_area = [strategy.point2d(0,15),strategy.point2d(0,17),strategy.point2d(0,18),strategy.point2d(0,19),strategy.point2d(1,19),strategy.point2d(1,16),strategy.point2d(2,19),strategy.point2d(0,0),strategy.point2d(0,1),strategy.point2d(0,2),strategy.point2d(0,4),strategy.point2d(1,3),strategy.point2d(1,0),strategy.point2d(2,0),strategy.point2d(17,0),strategy.point2d(18,0),strategy.point2d(19,0),strategy.point2d(19,1),strategy.point2d(19,2),strategy.point2d(19,4),strategy.point2d(18,3),strategy.point2d(19,15),strategy.point2d(19,17),strategy.point2d(19,18),strategy.point2d(19,19),strategy.point2d(18,16),strategy.point2d(18,19),strategy.point2d(17,19)]
thief_danger_area = []
w_unvisable_greatPower = 1.5
# global lists and dicts
leg_info = {}
players_last_pos = {}
tunnel_map = {}
meteor = []
wormhole = {}
tunnel = {}
wormhole_inverse = {}
cur_round_player_next_pos = {}
points_summary = {}
outOfWormholeRecord = {}
fakeEnemyPolice = []
fakeCloseEnemyPolice = []
greatPower = []
thief_enemy_region = []
visable_area = []
enemy_cur_round = []
power_cur_round = []
# global variables
nearest_enemy = 0
count = 0
vision = 3
bool_isPoliceMode = 1
bool_enough_players = 0
# search step settings
widthFirstSearchMaxStep = 6   # this decide the complexity of the algorithm dominantly.
findChoiceCountStep = 4  # when thief, find how many choices in future
findMinDiscFromEnemyWhenThief = 3
stepsOfEnemyFromNearestUsWhenPolice = (4,2)   # when we are ones step away from enemy, chose the small step
howManyStepsAfterOutOfWormhole = 15 # 