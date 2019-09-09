# encoding:utf8
'''
业务方法模块，需要选手实现

选手也可以另外创造模块，在本模块定义的方法中填入调用逻辑。这由选手决定

所有方法的参数均已经被解析成json，直接使用即可

所有方法的返回值为dict对象。客户端会在dict前面增加字符个数。
'''

import ballclient.service.strategy as strategy
import ballclient.service.constants as constants
import Queue
import os
from random import shuffle

def mapPreprocess(msg):
    # init
    constants.wormhole = {}
    constants.tunnel = {}
    constants.tunnel_map = {}
    constants.meteor = []
    constants.wormhole_inverse = {}
    constants.height = 0
    constants.width = 0
    constants.players_last_pos = {}
    constants.outOfWormholeRecord = {}
    # preprocess
    if msg['msg_data'].has_key('map'):
        if msg['msg_data']['map'].has_key('width'):
            constants.width = msg['msg_data']['map']['width']
        if msg['msg_data']['map'].has_key('height'):
            constants.height = msg['msg_data']['map']['height']
        if msg['msg_data']['map'].has_key('vision'):
            constants.vision = int(msg['msg_data']['map']['vision'])
        if msg['msg_data']['map'].has_key('meteor'):
            for met in msg['msg_data']['map']['meteor']:
                constants.meteor.append(strategy.point2d(int(met['x']),int(met['y'])))
        if msg['msg_data']['map'].has_key('tunnel'):
            for tun in msg['msg_data']['map']['tunnel']:
                constants.tunnel[strategy.point2d(int(tun['x']), int(tun['y']))] = tun['direction']
        if msg['msg_data']['map'].has_key('wormhole'):
            for wh in msg['msg_data']['map']['wormhole']:
                constants.wormhole[strategy.point2d(int(wh['x']),int(wh['y']))] = wh['name']

    constants.wormhole_inverse = {}
    for k,v in constants.wormhole.items():
        constants.wormhole_inverse[v] = k
    # print 'meteor: ', constants.meteor
    # print 'tunnel: ', constants.tunnel
    # print 'wormhole: ', constants.wormhole
    # print 'wormhole_inverse: ', constants.wormhole_inverse

    def travelByTunnelOneStep(pos, dir):
        if dir == 'up':
            return strategy.point2d(pos.getX(), pos.getY()-1)
        if dir == 'down':
            return strategy.point2d(pos.getX(), pos.getY()+1)
        if dir == 'left':
            return strategy.point2d(pos.getX()-1, pos.getY())
        if dir == 'right':
            return strategy.point2d(pos.getX()+1, pos.getY())

    for pos, dir in constants.tunnel.items():
        if constants.tunnel_map.has_key(pos):
            continue
        tun_q = Queue.Queue()
        tun_q.put(pos)
        while True:
            nextPos = travelByTunnelOneStep(pos, dir)
            if nextPos in constants.wormhole.keys():
                wh_name = constants.wormhole[nextPos]
                if wh_name.upper() != wh_name:
                    new_wh_name = wh_name.upper()
                else:
                    new_wh_name = wh_name.lower()
                finalPos = constants.wormhole_inverse[new_wh_name]
                while not tun_q.empty():
                    constants.tunnel_map[tun_q.get()] = finalPos
                break
            elif nextPos in constants.tunnel.keys():
                if nextPos in constants.tunnel_map.keys():
                    while not tun_q.empty():
                        constants.tunnel_map[tun_q.get()] = constants.tunnel_map[nextPos]
                    break
                else:
                    tun_q.put(nextPos)
                    pos  = nextPos
                    dir = constants.tunnel[nextPos]
            else:
                while not tun_q.empty():
                    constants.tunnel_map[tun_q.get()] = nextPos
                break

    # print 'tunnel_map: ', constants.tunnel_map


def leg_start(msg):
    constants.leg_info = msg
    mapPreprocess(msg)
    constants.logger.info('vision: %d' % constants.vision)


def leg_end(msg):
    '''

    :param msg:
    {
        "msg_name" : "leg_end",
        "msg_data" : {
            "teams" : [
            {
                "id" : 1001,				#队ID
                "point" : 770             #本leg的各队所得点数
            },
            {
            "id" : 1002,
            "point" : 450
             }
            ]
        }
    }

    :return:
    '''
    print "round over"
    teams = msg["msg_data"]['teams']
    for team in teams:
        print "teams:%s" % team['id']
        print "point:%s" % team['point']
        if constants.points_summary.has_key(team['id']):
            constants.points_summary[team['id']] = constants.points_summary[team['id']] + team['point']
        else:
            constants.points_summary[team['id']] = team['point']
        
        print "\n"
    print constants.points_summary


def game_over(msg):
    print "game over!"

def getNextPosFromDecision(player_pos, decision):
    nextPos = player_pos
    if decision == 1:
        nextPos = strategy.point2d(player_pos.getX(),player_pos.getY()-1)
    elif decision == 2:
        nextPos = strategy.point2d(player_pos.getX(),player_pos.getY()+1)
    elif decision == 3:
        nextPos = strategy.point2d(player_pos.getX()-1,player_pos.getY())
    elif decision == 4:
        nextPos = strategy.point2d(player_pos.getX()+1,player_pos.getY())
    else:
        nextPos = strategy.point2d(player_pos.getX(),player_pos.getY())
    return nextPos

def round(msg):
    '''

    :param msg: dict
    :return:
    return type: dict
    '''
    # put all information could be used into dict gameinfo
    round_id = msg['msg_data']['round_id']
    constants.logger.info("                    round %d" % round_id)
    players = []
    if msg['msg_data'].has_key('players'):
        players = msg['msg_data']['players']
    round_info = msg
    gameinfo = {}
    if constants.leg_info['msg_data']['teams'][0]['id'] == constants.team_id:
        gameinfo['player_US'] = constants.leg_info['msg_data']['teams'][0]['players']
        gameinfo['player_ENEMY'] = constants.leg_info['msg_data']['teams'][1]['players']
        gameinfo['force'] = constants.leg_info['msg_data']['teams'][0]['force']
    else:
        gameinfo['player_US'] = constants.leg_info['msg_data']['teams'][1]['players']
        gameinfo['player_ENEMY'] = constants.leg_info['msg_data']['teams'][0]['players']
        gameinfo['force'] = constants.leg_info['msg_data']['teams'][1]['force']
    gameinfo['mode'] = round_info['msg_data']['mode']
    if round_info['msg_data'].has_key('players'):
        gameinfo['players'] = round_info['msg_data']['players']
    else:
        gameinfo['players'] = []
    gameinfo['player_US_cur_round'] = []
    for player in players:
        if player['team'] == constants.team_id:
            gameinfo['player_US_cur_round'].append(player)
    if round_info['msg_data'].has_key('power'):
        gameinfo['power'] = round_info['msg_data']['power']
    else:
        gameinfo['power'] = []
    gameinfo['teams'] = round_info['msg_data']['teams']
    gameinfo['map'] = constants.leg_info['msg_data']['map']
    
    # analyze some global information
    
    # bool_isPoliceMode
    constants.bool_isPoliceMode = True
    if gameinfo['mode'] == gameinfo['force']:
        constants.bool_isPoliceMode = True
    else:
        constants.bool_isPoliceMode = False
    # bool_enough_players
    player_US_total = len(gameinfo['player_US'])
    constants.bool_enough_players = True
    if len(gameinfo['player_US_cur_round']) > player_US_total / 2:
        constants.bool_enough_players = True
    else:
        constants.bool_enough_players = False
    # enemy_cur_round
    enemy = []
    for p in gameinfo['players']:
        p_id = p['id']
        if p_id in gameinfo['player_ENEMY']:
            enemy.append(strategy.point2d(int(p['x']), int(p['y'])))
    constants.enemy_cur_round = enemy
    constants.logger.debug('enemy: ')
    constants.logger.debug(enemy)
    # power_cur_round
    power = []
    for pr in gameinfo['power']:
        power.append(strategy.point2d(int(pr['x']), int(pr['y'])))
    constants.power_cur_round = power
    constants.logger.debug('power: ')
    constants.logger.debug(power)
    # our players
    us = {}
    for p in gameinfo['players']:
        p_id = p['id']
        if p_id in gameinfo['player_US']:
            us[p_id] = strategy.point2d(int(p['x']), int(p['y']))
    constants.logger.debug('us: ')
    constants.logger.debug(us)
    # initiation of sorted_us
    sorted_u = []
    for id, u in us.items():
        id_disc_tuple = (id, 0)
        sorted_u.append(id_disc_tuple)
    # shuffle it
    shuffle(sorted_u)
    # visable_area
    constants.visable_area = []
    for id, u in us.items():
        for i in range(-constants.vision, constants.vision + 1):
            for j in range(-constants.vision, constants.vision + 1):
                constants.visable_area.append(strategy.point2d(u.getX()+i,u.getY()+j))
    # greatPower
    for pr in gameinfo['power']:
        pnt = pr['point']
        pr_pos = strategy.point2d(int(pr['x']), int(pr['y']))
        if pr_pos not in constants.greatPower and pnt > 3:
            constants.greatPower.append(pr_pos)
    
    # initiation of some global variables
    constants.w_player_disc_thief = constants.w_player_disc_thief_tuple[0]
    constants.w_player_disc_police = constants.w_player_disc_police_tuple[0]
    constants.thief_enemy_region = []
    constants.fakeEnemyPolice = []
    constants.fakeCloseEnemyPolice = []
    constants.w_enemy_thief = constants.w_enemy_thief_tuple[0]
    constants.w_power_thief = constants.w_power_thief_tuple[0]
    # analyze for two modes
    if not constants.bool_isPoliceMode:
        # thief
        # preprocess the enemy region
        # get the thief_enemy_region when thief, which means in one step away from enemy
        for enm in enemy:
            constants.thief_enemy_region.append(enm)
            for i in [-1,0,1]:
               for j in [-1,0,1]:
                   thisPos = strategy.point2d(enm.getX()+i,enm.getY()+j)
                   if thisPos not in constants.thief_enemy_region:
                       constants.thief_enemy_region.append(thisPos)
        constants.logger.debug('thief_enemy_region: ')
        constants.logger.debug(constants.thief_enemy_region)
        # compute min distance from enemy for each our player
        u_nearest_enemy_disc_dict = {}
        for id, u in us.items():
            u_enemy_disc = []
            for e in enemy:
                u_enemy_disc.append(strategy.ManhattanDstc(u,e))
            u_nearest_enemy_disc_dict[id] = strategy.getMinOfList(u_enemy_disc)
        # the more close with enemy, the earlier to makeDecision
        sorted_u = sorted(u_nearest_enemy_disc_dict.items(),key=lambda x:x[1])
        # when there is no enemy or power, start to act as a ranger.
        if len(enemy) == 0 and len(power) == 0:
            constants.w_player_disc_thief = constants.w_player_disc_thief_tuple[1]
        # when we are only one player left, choose whether to suicide.
        if len(us) == 1:
            last_one_id = us.keys()[0]
            last_one_point = 0
            for p in gameinfo['players']:
                if p['id'] == last_one_id:
                    last_one_point = p['score']
                    break
            remain_round = 0
            if round_id < 150:
                remain_round = 150 - round_id
            else:
                remain_round = 300 - round_id
            if float(last_one_point)/float(remain_round) < 0.8:
                constants.w_enemy_thief = constants.w_enemy_thief_tuple[1]
                constants.w_power_thief = constants.w_power_thief_tuple[1]
    else:
        # police
        
        # when there is no enemy or power, start to act as a ranger.
        if len(enemy) == 0 and len(power) == 0:
            constants.w_player_disc_police = constants.w_player_disc_police_tuple[1]
        # find the nearest_enemy and nearest_us
        if len(enemy) > 0 and len(us) > 0:
            enemy_us_disc_sum_dict = {}
            for enm in enemy:
                disc_sum = 0
                for u in us.values():
                    disc_sum = disc_sum + strategy.ManhattanDstc(enm,u)
                enemy_us_disc_sum_dict[enm] = disc_sum
            constants.nearest_enemy = enemy[0]
            nearest_enemy_disc = constants.INF
            for key,item in enemy_us_disc_sum_dict.items():
                if item < nearest_enemy_disc:
                    nearest_enemy_disc = item
                    constants.nearest_enemy = key
            constants.logger.debug('nearest_enemy: ')
            constants.logger.debug(constants.nearest_enemy)
            nearest_us_disc = constants.INF
            u_nearest_enemy_disc_dict = {}
            for id, u in us.items():
                u_disc = strategy.ManhattanDstc(u, constants.nearest_enemy)
                u_nearest_enemy_disc_dict[id] = u_disc
                if u_disc < nearest_us_disc:
                    nearest_us_disc = u_disc
                    nearest_us = u
            constants.logger.debug('nearest_us: ')
            constants.logger.debug(nearest_us)
            # the more close with enemy, the earlier to makeDecision
            sorted_u = sorted(u_nearest_enemy_disc_dict.items(),key=lambda x:x[1])
            # initiation of the max search step for fake enemy.
            maxStep = constants.stepsOfEnemyFromNearestUsWhenPolice[0]
            if nearest_us_disc == 1:
                constants.logger.info('Just One Step Away! Go Cover It!')
                # enemy very close, the nearest_us should eat the enemy next round, so the enemy position this round is ineffective, instead, the position one step away of the enemy can be set as 'real enemy'
                e_upPos = strategy.point2d(constants.nearest_enemy.getX(),constants.nearest_enemy.getY()-1)
                e_downPos = strategy.point2d(constants.nearest_enemy.getX(),constants.nearest_enemy.getY()+1)
                e_leftPos = strategy.point2d(constants.nearest_enemy.getX()-1,constants.nearest_enemy.getY())
                e_rightPos = strategy.point2d(constants.nearest_enemy.getX()+1,constants.nearest_enemy.getY())
                if e_upPos.getY() >= 0 and e_upPos not in constants.meteor and not nearest_us == e_upPos:
                    if e_upPos in constants.wormhole.keys():
                        constants.fakeCloseEnemyPolice.append(strategy.travelByWormhole(e_upPos))
                    elif e_upPos in constants.tunnel.keys():
                        constants.fakeCloseEnemyPolice.append(strategy.travelByTunnel(e_upPos))
                    else:
                        constants.fakeCloseEnemyPolice.append(e_upPos)
                if e_downPos.getY() < constants.height and e_downPos not in constants.meteor and not nearest_us == e_downPos:
                    if e_downPos in constants.wormhole.keys():
                        constants.fakeCloseEnemyPolice.append(strategy.travelByWormhole(e_downPos))
                    elif e_downPos in constants.tunnel.keys():
                        constants.fakeCloseEnemyPolice.append(strategy.travelByTunnel(e_downPos))
                    else:
                        constants.fakeCloseEnemyPolice.append(e_downPos)
                if e_leftPos.getX() >= 0 and e_leftPos not in constants.meteor and not nearest_us == e_leftPos:
                    if e_leftPos in constants.wormhole.keys():
                        constants.fakeCloseEnemyPolice.append(strategy.travelByWormhole(e_leftPos))
                    elif e_leftPos in constants.tunnel.keys():
                        constants.fakeCloseEnemyPolice.append(strategy.travelByTunnel(e_leftPos))
                    else:
                        constants.fakeCloseEnemyPolice.append(e_leftPos)
                if e_rightPos.getX() < constants.width and e_rightPos not in constants.meteor and not nearest_us == e_rightPos:
                    if e_rightPos in constants.wormhole.keys():
                        constants.fakeCloseEnemyPolice.append(strategy.travelByWormhole(e_rightPos))
                    elif e_rightPos in constants.tunnel.keys():
                        constants.fakeCloseEnemyPolice.append(strategy.travelByTunnel(e_rightPos))
                    else:
                        constants.fakeCloseEnemyPolice.append(e_rightPos)
                constants.logger.info('fakeCloseEnemyPolice: ')
                constants.logger.info(constants.fakeCloseEnemyPolice)
                # when we are one step away from the nearest_enemy, the fakeEnemyPolice search step can be set smaller.
                maxStep = constants.stepsOfEnemyFromNearestUsWhenPolice[1]
            # width first search for nearest_enemy
            src = constants.nearest_enemy
            width = constants.width
            height = constants.height
            reachedMap = [ [0 for i in range(constants.height)] for j in range(constants.width)]
            if src not in constants.wormhole.keys():
                reachedMap[src.getX()][src.getY()] = 1
            step_count = 0
            q = Queue.Queue()
            q.put(src)
            lastStepChoices = 1
            thisStepChoices = 0
            while_loop_count = 0
            while True:
                while_loop_count += 1
                constants.logger.debug('I am in loop %d'% while_loop_count)
                if thisStepChoices == 0:
                    step_count += 1
                    constants.logger.debug('step_count: %d' % step_count)
                if step_count > maxStep:
                    break
                if q.empty():
                    break
                curPos = q.get()
                lastStepChoices -= 1
                # up
                upPos = strategy.point2d(curPos.getX(), curPos.getY()-1)
                if upPos.getY() >= 0 and upPos not in constants.meteor:
                    constants.logger.debug('up, not reach edge, not in meteor')
                    if reachedMap[curPos.getX()][curPos.getY()-1] == 0:
                        constants.logger.debug('up, not reached yet')
                        if upPos in constants.wormhole.keys():
                            upPos = strategy.travelByWormhole(upPos)
                            q.put(upPos)
                            if strategy.ManhattanDstc(nearest_us,upPos) >= nearest_us_disc:
                                constants.fakeEnemyPolice.append(upPos)
                            thisStepChoices += 1
                        elif upPos in constants.tunnel.keys():
                            constants.logger.debug('up, in tunnel')
                            upPos = strategy.travelByTunnel(upPos)
                            q.put(upPos)
                            if strategy.ManhattanDstc(nearest_us,upPos) >= nearest_us_disc:
                                constants.fakeEnemyPolice.append(upPos)
                            thisStepChoices += 1
                            if upPos not in constants.wormhole.keys():
                                reachedMap[upPos.getX()][upPos.getY()] = 1
                        else:
                            constants.logger.debug('up, in ordinary position')
                            q.put(upPos)
                            if strategy.ManhattanDstc(nearest_us,upPos) >= nearest_us_disc:
                                constants.fakeEnemyPolice.append(upPos)
                            thisStepChoices += 1
                            reachedMap[upPos.getX()][upPos.getY()] = 1
                # down
                downPos = strategy.point2d(curPos.getX(), curPos.getY()+1)
                if downPos.getY() < height and downPos not in constants.meteor:
                    constants.logger.debug('down, not reach edge, not in meteor')
                    if reachedMap[curPos.getX()][curPos.getY()+1] == 0:
                        constants.logger.debug('down, not reached yet')
                        if downPos in constants.wormhole.keys():
                            downPos = strategy.travelByWormhole(downPos)
                            q.put(downPos)
                            if strategy.ManhattanDstc(nearest_us,downPos) >= nearest_us_disc:
                                constants.fakeEnemyPolice.append(downPos)
                            thisStepChoices += 1
                        elif downPos in constants.tunnel.keys():
                            constants.logger.debug('down, in tunnel')
                            downPos = strategy.travelByTunnel(downPos)
                            q.put(downPos)
                            if strategy.ManhattanDstc(nearest_us,downPos) >= nearest_us_disc:
                                constants.fakeEnemyPolice.append(downPos)
                            thisStepChoices += 1
                            if downPos not in constants.wormhole.keys():
                                reachedMap[downPos.getX()][downPos.getY()] = 1
                        else:
                            constants.logger.debug('down, in ordinary position')
                            q.put(downPos)
                            if strategy.ManhattanDstc(nearest_us,downPos) >= nearest_us_disc:
                                constants.fakeEnemyPolice.append(downPos)
                            thisStepChoices += 1
                            reachedMap[downPos.getX()][downPos.getY()] = 1
                # left
                leftPos = strategy.point2d(curPos.getX()-1, curPos.getY())
                if leftPos.getX() >= 0 and leftPos not in constants.meteor:
                    constants.logger.debug('left, not reach edge, not in meteor')
                    if reachedMap[curPos.getX()-1][curPos.getY()] == 0:
                        constants.logger.debug('left, not reached yet')
                        if leftPos in constants.wormhole.keys():
                            leftPos = strategy.travelByWormhole(leftPos)
                            q.put(leftPos)
                            if strategy.ManhattanDstc(nearest_us,leftPos) >= nearest_us_disc:
                                constants.fakeEnemyPolice.append(leftPos)
                            thisStepChoices += 1
                        elif leftPos in constants.tunnel.keys():
                            constants.logger.debug('left, in tunnel')
                            leftPos = strategy.travelByTunnel(leftPos)
                            q.put(leftPos)
                            if strategy.ManhattanDstc(nearest_us,leftPos) >= nearest_us_disc:
                                constants.fakeEnemyPolice.append(leftPos)
                            thisStepChoices += 1
                            if leftPos not in constants.wormhole.keys():
                                reachedMap[leftPos.getX()][leftPos.getY()] = 1
                        else:
                            constants.logger.debug('left, in ordinary position')
                            q.put(leftPos)
                            if strategy.ManhattanDstc(nearest_us,leftPos) >= nearest_us_disc:
                                constants.fakeEnemyPolice.append(leftPos)
                            thisStepChoices += 1
                            reachedMap[leftPos.getX()][leftPos.getY()] = 1
                # right
                rightPos = strategy.point2d(curPos.getX()+1, curPos.getY())
                if rightPos.getX() < width and rightPos not in constants.meteor:
                    constants.logger.debug('right, not reach edge, not in meteor')
                    if reachedMap[curPos.getX()+1][curPos.getY()] == 0:
                        constants.logger.debug('right, not reached yet')
                        if rightPos in constants.wormhole.keys():
                            rightPos = strategy.travelByWormhole(rightPos)
                            q.put(rightPos)
                            if strategy.ManhattanDstc(nearest_us,rightPos) >= nearest_us_disc:
                                constants.fakeEnemyPolice.append(rightPos)
                            thisStepChoices += 1
                        elif rightPos in constants.tunnel.keys():
                            constants.logger.debug('right, in tunnel')
                            rightPos = strategy.travelByTunnel(rightPos)
                            q.put(rightPos)
                            if strategy.ManhattanDstc(nearest_us,rightPos) >= nearest_us_disc:
                                constants.fakeEnemyPolice.append(rightPos)
                            thisStepChoices += 1
                            if rightPos not in constants.wormhole.keys():
                                reachedMap[rightPos.getX()][rightPos.getY()] = 1
                        else:
                            constants.logger.debug('right, in ordinary position')
                            q.put(rightPos)
                            if strategy.ManhattanDstc(nearest_us,rightPos) >= nearest_us_disc:
                                constants.fakeEnemyPolice.append(rightPos)
                            thisStepChoices += 1
                            reachedMap[rightPos.getX()][rightPos.getY()] = 1
                if lastStepChoices == 0:
                    lastStepChoices = thisStepChoices
                    thisStepChoices = 0
        constants.logger.debug('Final fakeEnemyPolice: ')
        constants.logger.debug(constants.fakeEnemyPolice)
    # if the direction not in ('up', 'down', 'left', 'right'), the KUN will stop
    direction = {1: 'up', 2: 'down', 3: 'left', 4: 'right', 5: 'stop'}
    action = []
    constants.cur_round_player_next_pos = {}
    constants.count = 0
    result = {
        "msg_name": "action",
        "msg_data": {
            "round_id": round_id
        }
    }
    for player_id_disc_tuple in sorted_u:
        constants.count += 1
        player_id = player_id_disc_tuple[0]
        player_pos = us[player_id]
        constants.logger.info('player_id %d' % player_id)
        constants.logger.info('cur_round_player_next_pos: ')
        constants.logger.info(constants.cur_round_player_next_pos)
        constants.logger.info('player_pos: ')
        constants.logger.info(player_pos)
        if player_id not in constants.outOfWormholeRecord.keys():
            constants.outOfWormholeRecord[player_id] = 11
        if player_pos in constants.wormhole.keys():
            constants.outOfWormholeRecord[player_id] = 0
        else:
            constants.outOfWormholeRecord[player_id]  = constants.outOfWormholeRecord[player_id] + 1
        if player_id not in constants.players_last_pos.keys():
            constants.players_last_pos[player_id] = player_pos
        # core step
        decision = strategy.makeDecision(player_pos, player_id)
        # form the action message for returning to the server
        action.append({"team": constants.team_id, "player_id": player_id,
                       "move": [direction[decision]]})
        constants.players_last_pos[player_id] = player_pos
        # players position do not overlay
        nextPos = getNextPosFromDecision(player_pos, decision)
        constants.cur_round_player_next_pos[player_id] = nextPos
            
    result['msg_data']['actions'] = action
    constants.logger.info('action: ')
    constants.logger.info(action)
    return result
