# encoding:utf8
'''
    策略模块
'''
import Queue
import random
import constants

class point2d():
    def __init__(self, x, y):
        self._x = x
        self._y = y
    def getX(self):
        return self._x
    def getY(self):
        return self._y
    def getXY(self):
        return (self._x, self._y)
    def setX(self, x):
        self._x = x
    def setY(self, y):
        self._y = y
    def setXY(self, pos):
        self._x = pos[0]
        self._y = pos[1]
    def __eq__(self, another):
        if self._x == another._x and self._y == another._y:
            return True
        else:
            return False
    def __repr__(self):
        return "Point2d({}, {})".format(self._x, self._y)
    def __hash__(self):
        return hash(self._x ^ self._y * 137)

def ManhattanDstc(point1, point2):
    deltaX = abs(point1.getX() - point2.getX())
    deltaY = abs(point1.getY() - point2.getY())
    return deltaX + deltaY

def computeStep(src, dst, maxStep):
    if src.getX() == dst.getX() and src.getY() == dst.getY():
        return 0
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
    bool_reached = False
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
        upPos = point2d(curPos.getX(), curPos.getY()-1)
        if upPos.getX() == dst.getX() and upPos.getY() == dst.getY():
            bool_reached = True
            break
        if upPos.getY() >= 0 and upPos not in constants.meteor:
            constants.logger.debug('up, not reach edge, not in meteor')
            if reachedMap[curPos.getX()][curPos.getY()-1] == 0:
                constants.logger.debug('up, not reached yet')
                if upPos in constants.wormhole.keys():
                    upPos = travelByWormhole(upPos)
                    if upPos.getX() == dst.getX() and upPos.getY() == dst.getY():
                        bool_reached = True
                        break
                    q.put(upPos)
                    thisStepChoices += 1
                elif upPos in constants.tunnel.keys():
                    constants.logger.debug('up, in tunnel')
                    upPos = travelByTunnel(upPos)
                    if upPos.getX() == dst.getX() and upPos.getY() == dst.getY():
                        bool_reached = True
                        break
                    q.put(upPos)
                    thisStepChoices += 1
                    if upPos not in constants.wormhole.keys():
                        reachedMap[upPos.getX()][upPos.getY()] = 1
                else:
                    constants.logger.debug('up, in ordinary position')
                    q.put(upPos)
                    thisStepChoices += 1
                    reachedMap[upPos.getX()][upPos.getY()] = 1
        # down
        downPos = point2d(curPos.getX(), curPos.getY()+1)
        if downPos.getX() == dst.getX() and downPos.getY() == dst.getY():
            bool_reached = True
            break
        if downPos.getY() < height and downPos not in constants.meteor:
            constants.logger.debug('down, not reach edge, not in meteor')
            if reachedMap[curPos.getX()][curPos.getY()+1] == 0:
                constants.logger.debug('down, not reached yet')
                if downPos in constants.wormhole.keys():
                    downPos = travelByWormhole(downPos)
                    if downPos.getX() == dst.getX() and downPos.getY() == dst.getY():
                        bool_reached = True
                        break
                    q.put(downPos)
                    thisStepChoices += 1
                elif downPos in constants.tunnel.keys():
                    constants.logger.debug('down, in tunnel')
                    downPos = travelByTunnel(downPos)
                    if downPos.getX() == dst.getX() and downPos.getY() == dst.getY():
                        bool_reached = True
                        break
                    q.put(downPos)
                    thisStepChoices += 1
                    if downPos not in constants.wormhole.keys():
                        reachedMap[downPos.getX()][downPos.getY()] = 1
                else:
                    constants.logger.debug('down, in ordinary position')
                    q.put(downPos)
                    thisStepChoices += 1
                    reachedMap[downPos.getX()][downPos.getY()] = 1
        # left
        leftPos = point2d(curPos.getX()-1, curPos.getY())
        if leftPos.getX() == dst.getX() and leftPos.getY() == dst.getY():
            bool_reached = True
            break
        if leftPos.getX() >= 0 and leftPos not in constants.meteor:
            constants.logger.debug('left, not reach edge, not in meteor')
            if reachedMap[curPos.getX()-1][curPos.getY()] == 0:
                constants.logger.debug('left, not reached yet')
                if leftPos in constants.wormhole.keys():
                    leftPos = travelByWormhole(leftPos)
                    if leftPos.getX() == dst.getX() and leftPos.getY() == dst.getY():
                        bool_reached = True
                        break
                    q.put(leftPos)
                    thisStepChoices += 1
                elif leftPos in constants.tunnel.keys():
                    constants.logger.debug('left, in tunnel')
                    leftPos = travelByTunnel(leftPos)
                    if leftPos.getX() == dst.getX() and leftPos.getY() == dst.getY():
                        bool_reached = True
                        break
                    q.put(leftPos)
                    thisStepChoices += 1
                    if leftPos not in constants.wormhole.keys():
                        reachedMap[leftPos.getX()][leftPos.getY()] = 1
                else:
                    constants.logger.debug('left, in ordinary position')
                    q.put(leftPos)
                    thisStepChoices += 1
                    reachedMap[leftPos.getX()][leftPos.getY()] = 1
        # right
        rightPos = point2d(curPos.getX()+1, curPos.getY())
        if rightPos.getX() == dst.getX() and rightPos.getY() == dst.getY():
            bool_reached = True
            break
        if rightPos.getX() < width and rightPos not in constants.meteor:
            constants.logger.debug('right, not reach edge, not in meteor')
            if reachedMap[curPos.getX()+1][curPos.getY()] == 0:
                constants.logger.debug('right, not reached yet')
                if rightPos in constants.wormhole.keys():
                    rightPos = travelByWormhole(rightPos)
                    if rightPos.getX() == dst.getX() and rightPos.getY() == dst.getY():
                        bool_reached = True
                        break
                    q.put(rightPos)
                    thisStepChoices += 1
                elif rightPos in constants.tunnel.keys():
                    constants.logger.debug('right, in tunnel')
                    rightPos = travelByTunnel(rightPos)
                    if rightPos.getX() == dst.getX() and rightPos.getY() == dst.getY():
                        bool_reached = True
                        break
                    q.put(rightPos)
                    thisStepChoices += 1
                    if rightPos not in constants.wormhole.keys():
                        reachedMap[rightPos.getX()][rightPos.getY()] = 1
                else:
                    constants.logger.debug('right, in ordinary position')
                    q.put(rightPos)
                    thisStepChoices += 1
                    reachedMap[rightPos.getX()][rightPos.getY()] = 1
        if lastStepChoices == 0:
            lastStepChoices = thisStepChoices
            thisStepChoices = 0
    constants.logger.debug('Final step_count: %d' % step_count)
    if bool_reached:
        return step_count
    else:
        return constants.INF

def travelByTunnel(pos):
    return constants.tunnel_map[pos]

def travelByWormhole(pos):
    wh_name = constants.wormhole[pos]
    if wh_name.upper() != wh_name:
        new_wh_name = wh_name.upper()
    else:
        new_wh_name = wh_name.lower()
    return constants.wormhole_inverse[new_wh_name]

def widthFirstSearch(dstPos_origin):
    dstPos = dstPos_origin
    width = constants.width
    height = constants.height
    thiefChoiceCount = 0
    # wormhole
    findNearestWormhole = False
    min_wormhole_disc = constants.INF
    if len(constants.wormhole) == 0:
        findNearestWormhole = True
    if dstPos in constants.wormhole.keys():
        findNearestWormhole = True
        min_wormhole_disc = 0
        dstPos = travelByWormhole(dstPos)
    # tunnel
    if dstPos in constants.tunnel.keys():
        dstPos = travelByTunnel(dstPos)
    # enemy
    enemy = []
    for enm in constants.enemy_cur_round:  # can't use 'enemy = constants.enemy_cur_round', because the remove and extend operation below will change the constants.enemy_cur_round
        enemy.append(enm)
    if constants.bool_isPoliceMode and len(constants.fakeCloseEnemyPolice) > 0 and constants.count > 1:
        # when we are one step away from the nearest_enemy, adjust the enemy list
        enemy.remove(constants.nearest_enemy)
        enemy.extend(constants.fakeCloseEnemyPolice)
    findNearestEnemy = False
    min_enemy_disc = constants.INF
    if len(enemy) == 0:
        findNearestEnemy = True
    if dstPos_origin in enemy or dstPos in enemy:
        findNearestEnemy = True
        min_enemy_disc = 0
    # fake enemy
    findNearestFakeEnemy = False
    min_fake_enemy_disc = constants.INF
    if len(constants.fakeEnemyPolice) == 0:
        findNearestFakeEnemy = True
    if dstPos_origin in constants.fakeEnemyPolice or dstPos in constants.fakeEnemyPolice:
        findNearestFakeEnemy = True
        min_fake_enemy_disc = 0
    # power
    power = constants.power_cur_round
    findNearestPower = False
    min_power_disc = constants.INF
    if len(power) == 0:
        findNearestPower = True
    if dstPos in power:
        findNearestPower = True
        min_power_disc = 0
    # unvisable greatPower
    greatPower = constants.greatPower
    for gp in greatPower:
        if gp in constants.visable_area:
            greatPower.remove(gp)
    findNearestUnvisableGreatPower = False
    min_unvisable_greatPower_disc = constants.INF
    if len(greatPower) == 0:
        findNearestUnvisableGreatPower = True
    
    if constants.bool_isPoliceMode and findNearestEnemy and findNearestPower and findNearestWormhole and findNearestFakeEnemy and findNearestUnvisableGreatPower:
        return min_enemy_disc, min_power_disc, min_wormhole_disc, min_fake_enemy_disc, thiefChoiceCount, min_unvisable_greatPower_disc
    
    reachedMap = [ [0 for i in range(constants.height)] for j in range(constants.width)]
    if dstPos not in constants.wormhole.keys():
        reachedMap[dstPos.getX()][dstPos.getY()] = 1
    step_count = 0
    q = Queue.Queue()
    q.put(dstPos)
    lastStepChoices = 1
    thisStepChoices = 0
    while_loop_count = 0
    
    findChoiceCountStep = constants.findChoiceCountStep # when thief, find how many choices in findChoiceCountStep steps
    
    while True:
        if thisStepChoices == 0:
            step_count += 1
        if step_count > constants.widthFirstSearchMaxStep:
            break
        curPos = q.get()
        lastStepChoices -= 1
        # up
        upPos = point2d(curPos.getX(), curPos.getY()-1)
        if upPos.getY() >= 0 and upPos not in constants.meteor:
            if reachedMap[curPos.getX()][curPos.getY()-1] == 0:
                if upPos in constants.wormhole.keys():
                    if not findNearestWormhole:
                        findNearestWormhole = True
                        min_wormhole_disc = step_count
                    upPos = travelByWormhole(upPos)
                    q.put(upPos)
                    thisStepChoices += 1
                    if step_count <= findChoiceCountStep and upPos not in constants.thief_enemy_region:
                        thiefChoiceCount += 1
                elif upPos in constants.tunnel.keys():
                    upPos = travelByTunnel(upPos)
                    q.put(upPos)
                    thisStepChoices += 1
                    if step_count <= findChoiceCountStep and upPos not in constants.thief_enemy_region:
                        thiefChoiceCount += 1
                    if upPos not in constants.wormhole.keys():
                        reachedMap[upPos.getX()][upPos.getY()] = 1
                    if not findNearestEnemy and upPos in enemy:
                        findNearestEnemy = True
                        min_enemy_disc = step_count
                    if not findNearestPower and upPos in power:
                        findNearestPower = True
                        min_power_disc = step_count
                    if not findNearestFakeEnemy and upPos in constants.fakeEnemyPolice:
                        findNearestFakeEnemy = True
                        min_fake_enemy_disc = step_count
                    if not findNearestUnvisableGreatPower and upPos in greatPower:
                        findNearestUnvisableGreatPower = True
                        min_unvisable_greatPower_disc = step_count
                else:
                    q.put(upPos)
                    thisStepChoices += 1
                    if step_count <= findChoiceCountStep and upPos not in constants.thief_enemy_region:
                        thiefChoiceCount += 1
                    reachedMap[upPos.getX()][upPos.getY()] = 1
                    if not findNearestEnemy and upPos in enemy:
                        findNearestEnemy = True
                        min_enemy_disc = step_count
                    if not findNearestPower and upPos in power:
                        findNearestPower = True
                        min_power_disc = step_count
                    if not findNearestFakeEnemy and upPos in constants.fakeEnemyPolice:
                        findNearestFakeEnemy = True
                        min_fake_enemy_disc = step_count
                    if not findNearestUnvisableGreatPower and upPos in greatPower:
                        findNearestUnvisableGreatPower = True
                        min_unvisable_greatPower_disc = step_count
        # down
        downPos = point2d(curPos.getX(), curPos.getY()+1)
        if downPos.getY() < height and downPos not in constants.meteor:
            if reachedMap[curPos.getX()][curPos.getY()+1] == 0:
                if downPos in constants.wormhole.keys():
                    if not findNearestWormhole:
                        findNearestWormhole = True
                        min_wormhole_disc = step_count
                    downPos = travelByWormhole(downPos)
                    q.put(downPos)
                    thisStepChoices += 1
                    if step_count <= findChoiceCountStep and downPos not in constants.thief_enemy_region:
                        thiefChoiceCount += 1
                elif downPos in constants.tunnel.keys():
                    downPos = travelByTunnel(downPos)
                    q.put(downPos)
                    thisStepChoices += 1
                    if step_count <= findChoiceCountStep and downPos not in constants.thief_enemy_region:
                        thiefChoiceCount += 1
                    if downPos not in constants.wormhole.keys():
                        reachedMap[downPos.getX()][downPos.getY()] = 1
                    if not findNearestEnemy and downPos in enemy:
                        findNearestEnemy = True
                        min_enemy_disc = step_count
                    if not findNearestPower and downPos in power:
                        findNearestPower = True
                        min_power_disc = step_count
                    if not findNearestFakeEnemy and downPos in constants.fakeEnemyPolice:
                        findNearestFakeEnemy = True
                        min_fake_enemy_disc = step_count
                    if not findNearestUnvisableGreatPower and downPos in greatPower:
                        findNearestUnvisableGreatPower = True
                        min_unvisable_greatPower_disc = step_count
                else:
                    q.put(downPos)
                    thisStepChoices += 1
                    if step_count <= findChoiceCountStep and downPos not in constants.thief_enemy_region:
                        thiefChoiceCount += 1
                    reachedMap[downPos.getX()][downPos.getY()] = 1
                    if not findNearestEnemy and downPos in enemy:
                        findNearestEnemy = True
                        min_enemy_disc = step_count
                    if not findNearestPower and downPos in power:
                        findNearestPower = True
                        min_power_disc = step_count
                    if not findNearestFakeEnemy and downPos in constants.fakeEnemyPolice:
                        findNearestFakeEnemy = True
                        min_fake_enemy_disc = step_count
                    if not findNearestUnvisableGreatPower and downPos in greatPower:
                        findNearestUnvisableGreatPower = True
                        min_unvisable_greatPower_disc = step_count
        # left
        leftPos = point2d(curPos.getX()-1, curPos.getY())
        if leftPos.getX() >= 0 and leftPos not in constants.meteor:
            if reachedMap[curPos.getX()-1][curPos.getY()] == 0:
                if leftPos in constants.wormhole.keys():
                    if not findNearestWormhole:
                        findNearestWormhole = True
                        min_wormhole_disc = step_count
                    leftPos = travelByWormhole(leftPos)
                    q.put(leftPos)
                    thisStepChoices += 1
                    if step_count <= findChoiceCountStep and leftPos not in constants.thief_enemy_region:
                        thiefChoiceCount += 1
                elif leftPos in constants.tunnel.keys():
                    leftPos = travelByTunnel(leftPos)
                    q.put(leftPos)
                    thisStepChoices += 1
                    if step_count <= findChoiceCountStep and leftPos not in constants.thief_enemy_region:
                        thiefChoiceCount += 1
                    if leftPos not in constants.wormhole.keys():
                        reachedMap[leftPos.getX()][leftPos.getY()] = 1
                    if not findNearestEnemy and leftPos in enemy:
                        findNearestEnemy = True
                        min_enemy_disc = step_count
                    if not findNearestPower and leftPos in power:
                        findNearestPower = True
                        min_power_disc = step_count
                    if not findNearestFakeEnemy and leftPos in constants.fakeEnemyPolice:
                        findNearestFakeEnemy = True
                        min_fake_enemy_disc = step_count
                    if not findNearestUnvisableGreatPower and leftPos in greatPower:
                        findNearestUnvisableGreatPower = True
                        min_unvisable_greatPower_disc = step_count
                else:
                    q.put(leftPos)
                    thisStepChoices += 1
                    if step_count <= findChoiceCountStep and leftPos not in constants.thief_enemy_region:
                        thiefChoiceCount += 1
                    reachedMap[leftPos.getX()][leftPos.getY()] = 1
                    if not findNearestEnemy and leftPos in enemy:
                        findNearestEnemy = True
                        min_enemy_disc = step_count
                    if not findNearestPower and leftPos in power:
                        findNearestPower = True
                        min_power_disc = step_count
                    if not findNearestFakeEnemy and leftPos in constants.fakeEnemyPolice:
                        findNearestFakeEnemy = True
                        min_fake_enemy_disc = step_count
                    if not findNearestUnvisableGreatPower and leftPos in greatPower:
                        findNearestUnvisableGreatPower = True
                        min_unvisable_greatPower_disc = step_count
        # right
        rightPos = point2d(curPos.getX()+1, curPos.getY())
        if rightPos.getX() < width and rightPos not in constants.meteor:
            if reachedMap[curPos.getX()+1][curPos.getY()] == 0:
                if rightPos in constants.wormhole.keys():
                    if not findNearestWormhole:
                        findNearestWormhole = True
                        min_wormhole_disc = step_count
                    rightPos = travelByWormhole(rightPos)
                    q.put(rightPos)
                    thisStepChoices += 1
                    if step_count <= findChoiceCountStep and rightPos not in constants.thief_enemy_region:
                        thiefChoiceCount += 1
                elif rightPos in constants.tunnel.keys():
                    rightPos = travelByTunnel(rightPos)
                    q.put(rightPos)
                    thisStepChoices += 1
                    if step_count <= findChoiceCountStep and rightPos not in constants.thief_enemy_region:
                        thiefChoiceCount += 1
                    if rightPos not in constants.wormhole.keys():
                        reachedMap[rightPos.getX()][rightPos.getY()] = 1
                    if not findNearestEnemy and rightPos in enemy:
                        findNearestEnemy = True
                        min_enemy_disc = step_count
                    if not findNearestPower and rightPos in power:
                        findNearestPower = True
                        min_power_disc = step_count
                    if not findNearestFakeEnemy and rightPos in constants.fakeEnemyPolice:
                        findNearestFakeEnemy = True
                        min_fake_enemy_disc = step_count
                    if not findNearestUnvisableGreatPower and rightPos in greatPower:
                        findNearestUnvisableGreatPower = True
                        min_unvisable_greatPower_disc = step_count
                else:
                    q.put(rightPos)
                    thisStepChoices += 1
                    if step_count <= findChoiceCountStep and rightPos not in constants.thief_enemy_region:
                        thiefChoiceCount += 1
                    reachedMap[rightPos.getX()][rightPos.getY()] = 1
                    if not findNearestEnemy and rightPos in enemy:
                        findNearestEnemy = True
                        min_enemy_disc = step_count
                    if not findNearestPower and rightPos in power:
                        findNearestPower = True
                        min_power_disc = step_count
                    if not findNearestFakeEnemy and rightPos in constants.fakeEnemyPolice:
                        findNearestFakeEnemy = True
                        min_fake_enemy_disc = step_count
                    if not findNearestUnvisableGreatPower and rightPos in greatPower:
                        findNearestUnvisableGreatPower = True
                        min_unvisable_greatPower_disc = step_count
        if constants.bool_isPoliceMode and findNearestEnemy and findNearestPower and findNearestWormhole and findNearestFakeEnemy and findNearestUnvisableGreatPower:
            break
        if q.empty():
            break
        if lastStepChoices == 0:
            lastStepChoices = thisStepChoices
            thisStepChoices = 0
    if not constants.bool_isPoliceMode:
        if dstPos_origin in constants.tunnel.keys():
            dstPos_origin = travelByTunnel(dstPos_origin)
        findNearestEnemy = False
        min_enemy_disc = constants.INF
        if len(enemy) == 0:
            findNearestEnemy = True
        if dstPos_origin in enemy:
            findNearestEnemy = True
            min_enemy_disc = 0
        if findNearestEnemy and findNearestPower and findNearestWormhole:
            return min_enemy_disc, min_power_disc, min_wormhole_disc, min_fake_enemy_disc, thiefChoiceCount, min_unvisable_greatPower_disc
        enemy_disc_list = []
        for enm in enemy:
            refer_disc = ManhattanDstc(enm, dstPos_origin)
            if refer_disc > constants.findMinDiscFromEnemyWhenThief:
                disc = constants.INF
            else:
                # if isThief, the min_enemy_disc should be the steps FROM the enemy TO us, which can't be computed in widthFirstSearch above.
                disc = computeStep(enm, dstPos_origin, constants.findMinDiscFromEnemyWhenThief)
            enemy_disc_list.append(disc)
        min_enemy_disc = getMinOfList(enemy_disc_list)
    return min_enemy_disc, min_power_disc, min_wormhole_disc, min_fake_enemy_disc, thiefChoiceCount, min_unvisable_greatPower_disc

def getMeanOfList(inputList):
    sum = 0
    for item in inputList:
        sum += item
    if len(inputList) == 0:
        return 0
    return float(sum) / len(inputList)

def getMinOfList(inputList):
    rst = constants.INF
    for item in inputList:
        rst = min(item, rst)
    return rst

def computeGainPolice(player_pos, dstPos, last_pos_disc, player_id):
    constants.logger.info('fakeEnemyPolice: ')
    constants.logger.info(constants.fakeEnemyPolice)
    # choose whether to suicide
    if constants.bool_enough_players:
        w_enemy_police = constants.w_enemy_police[0]
    else:
        w_enemy_police = constants.w_enemy_police[1]
    
    min_enemy_disc, min_power_disc, min_wormhole_disc, min_fake_enemy_disc, thiefChoiceCount, min_unvisable_greatPower_disc= widthFirstSearch(dstPos)
    
    nearest_greatpower_disc = constants.INF
    if min_enemy_disc == constants.INF and min_power_disc == constants.INF:
        for gtpr in constants.greatPower:
            this_gtpr_disc = ManhattanDstc(gtpr, dstPos)
            if this_gtpr_disc < nearest_greatpower_disc:
                nearest_greatpower_disc = this_gtpr_disc
    
    if dstPos in constants.wormhole:
        finalPos = travelByWormhole(dstPos)
    elif dstPos in constants.tunnel:
        finalPos = travelByTunnel(dstPos)
    else:
        finalPos = dstPos
    # players do not overlay
    if finalPos in constants.cur_round_player_next_pos.values():
        bool_overlay = 1
    else:
        bool_overlay = 0
    mean_player_disc = constants.INF
    min_player_disc = constants.INF
    player_disc_list = []
    for player_pos in constants.cur_round_player_next_pos.values():
        player_disc_list.append(ManhattanDstc(finalPos, player_pos))
    if len(player_disc_list) > 0:
        mean_player_disc = getMeanOfList(player_disc_list)
        min_player_disc = getMinOfList(player_disc_list)
    # go for wormhole or go away from it
    if constants.outOfWormholeRecord[player_id] > constants.howManyStepsAfterOutOfWormhole:
        w_wormhole_police = constants.w_wormhole_police[0]
    else:
        w_wormhole_police = constants.w_wormhole_police[1]
    gain = w_enemy_police * 1.0 / (min_enemy_disc + 1) + constants.w_power_police * 1.0 /(min_power_disc + 1) + constants.w_last_pos_police * 1.0 /(last_pos_disc + 1) + w_wormhole_police * 1.0 / (min_wormhole_disc + 1) + constants.w_player_disc_police * 1.0 / (min_player_disc + 1) + constants.w_player_overlay_police * bool_overlay + constants.w_fake_enemy_police * 1.0 / (min_fake_enemy_disc + 1) +  constants.w_nearest_greatpower_disc_police * 1.0 / (nearest_greatpower_disc + 1) + constants.w_unvisable_greatPower * 1.0 / (min_unvisable_greatPower_disc + 1)
    constants.logger.info('bool_overlay: %d'% bool_overlay)
    constants.logger.info('min_enemy_disc: %d'%min_enemy_disc)
    constants.logger.info('min_power_disc: %d'%min_power_disc)
    constants.logger.info('min_wormhole_disc: %d'%min_wormhole_disc)
    constants.logger.info('last_pos_disc: %d'% last_pos_disc)
    constants.logger.info('mean_player_disc: %d' % mean_player_disc)
    constants.logger.info('min_player_disc: %d' % min_player_disc)
    constants.logger.info('min_fake_enemy_disc: %d' % min_fake_enemy_disc)
    constants.logger.info('nearest_greatpower_disc: %d' % nearest_greatpower_disc)
    constants.logger.info('gain: %f'%gain)
    return gain

def computeGainThief(player_pos, dstPos, last_pos_disc, player_id):
    enemy = constants.enemy_cur_round
    enemy_disc = [ ManhattanDstc(dstPos,i) for i in enemy ]
    mean_enemy_disc = getMeanOfList(enemy_disc)
    min_enemy_Manhaton_disc_thief = getMinOfList(enemy_disc)
    if len(enemy) == 0:
        mean_enemy_disc = constants.INF
        min_enemy_Manhaton_disc_thief = constants.INF
    
    min_enemy_disc, min_power_disc, min_wormhole_disc, min_fake_enemy_disc, thiefChoiceCount, min_unvisable_greatPower_disc = widthFirstSearch(dstPos)
    
    nearest_greatpower_disc = constants.INF
    if min_enemy_disc == constants.INF and min_power_disc == constants.INF:
        for gtpr in constants.greatPower:
            if gtpr in constants.visable_area:
                continue
            this_gtpr_disc = ManhattanDstc(gtpr, dstPos)
            if this_gtpr_disc < nearest_greatpower_disc:
                nearest_greatpower_disc = this_gtpr_disc
    
    if dstPos in constants.wormhole:
        finalPos = travelByWormhole(dstPos)
    elif dstPos in constants.tunnel:
        finalPos = travelByTunnel(dstPos)
    else:
        finalPos = dstPos
    # players do not overlay
    if finalPos in constants.cur_round_player_next_pos.values():
        bool_overlay = 1
    else:
        bool_overlay = 0
    mean_player_disc = constants.INF
    min_player_disc = constants.INF
    player_disc_list = []
    for player_pos in constants.cur_round_player_next_pos.values():
        player_disc_list.append(ManhattanDstc(finalPos, player_pos))
    if len(player_disc_list) > 0:
        mean_player_disc = getMeanOfList(player_disc_list)
        min_player_disc = getMinOfList(player_disc_list)
    min_bound_X_disc = min(finalPos.getX(), constants.width - 1 - finalPos.getX())
    min_bound_Y_disc = min(finalPos.getY(), constants.height - 1 - finalPos.getY())
    # try not to go through tunnels, because some enemy could also go through the tunnel and finally get out to same position, then our player is eaten.
    bool_exit_tunnel = 0
    if finalPos in constants.tunnel_map.values():
        bool_exit_tunnel = 1
    # try not to go to somewhere which is not in our visable_area
    exit_out_of_vison_penalty = 0
    if finalPos not in constants.visable_area:
        exit_out_of_vison_penalty = -1
    # try not to go to dangerous area
    bool_danger_area = 0
    if finalPos in constants.thief_danger_area:
        bool_danger_area = 1
    # go for wormhole or go away from it
    if constants.outOfWormholeRecord[player_id] > constants.howManyStepsAfterOutOfWormhole:
        w_wormhole_thief = constants.w_wormhole_thief[0]
    else:
        w_wormhole_thief = constants.w_wormhole_thief[1]
    gain = constants.w_enemy_thief * 1.0 / (min_enemy_disc + 1) + constants.w_power_thief * 1.0 /(min_power_disc + 1) + constants.w_last_pos_thief * 1.0 /(last_pos_disc + 1) + w_wormhole_thief * 1.0 /(min_wormhole_disc + 1) + constants.w_player_disc_thief * 1.0 / (min_player_disc + 1) + constants.w_bound_X_thief * 1.0 /(min_bound_X_disc + 1) + constants.w_bound_Y_thief * 1.0 /(min_bound_Y_disc + 1) + (constants.w_exit_tunnel)* 1.0 *bool_exit_tunnel + exit_out_of_vison_penalty + constants.w_player_overlay_thief * bool_overlay + constants.w_mean_enemy_disc_thief * 1.0 / (mean_enemy_disc + 1) + constants.w_thief_future_choice * 1.0 / (thiefChoiceCount + 1) + constants.w_nearest_greatpower_disc_thief * 1.0 /(nearest_greatpower_disc + 1) + constants.w_min_enemy_Manhaton_disc_thief * 1.0 / (min_enemy_Manhaton_disc_thief + 1) + constants.w_danger_area *1.0* bool_danger_area + constants.w_unvisable_greatPower * 1.0 / (min_unvisable_greatPower_disc + 1)
    constants.logger.info('bool_overlay: %d'% bool_overlay)
    constants.logger.info('bool_exit_tunnel: %d'% bool_exit_tunnel)
    constants.logger.info('min_enemy_disc: %d'%min_enemy_disc)
    constants.logger.info('min_power_disc: %d'%min_power_disc)
    constants.logger.info('min_wormhole_disc: %d'%min_wormhole_disc)
    constants.logger.info('last_pos_disc: %d'% last_pos_disc)
    constants.logger.info('mean_player_disc: %d' % mean_player_disc)
    constants.logger.info('min_player_disc: %d' % min_player_disc)
    constants.logger.info('min_bound_X_disc: %d' % min_bound_X_disc)
    constants.logger.info('min_bound_Y_disc: %d' % min_bound_Y_disc)
    constants.logger.info('mean_enemy_disc: %d' % mean_enemy_disc)
    constants.logger.info('nearest_greatpower_disc: %d' % nearest_greatpower_disc)
    constants.logger.info('thiefChoiceCount: %d' % thiefChoiceCount)
    constants.logger.info('min_enemy_Manhaton_disc_thief: %d' % min_enemy_Manhaton_disc_thief)
    constants.logger.info('gain: %f'%gain)
    return gain


def makeDecision(player_pos, player_id):
    player_last_pos = constants.players_last_pos[player_id]
    if constants.bool_isPoliceMode:
        # police
        cur_x = player_pos.getX()
        cur_y = player_pos.getY()
        choices_gains = {}
        # up
        if cur_y > 0:
            dstPos = point2d(cur_x, cur_y - 1)
            collision = False
            for met in constants.meteor:
                if dstPos == met:
                    collision = True
                    break
            if not collision:
                constants.logger.info('police  up')
                if dstPos in constants.tunnel.keys():
                    finalPos = constants.tunnel_map[dstPos]
                    if finalPos.getX() != player_pos.getX() or finalPos.getY() != player_pos.getY():
                        last_pos_disc = 2
                    else:
                        last_pos_disc = 0
                elif dstPos.getX() != player_last_pos.getX() or dstPos.getY() != player_last_pos.getY():
                    last_pos_disc = 2
                else:
                    last_pos_disc = 0
                choices_gains[1] = computeGainPolice(player_pos, dstPos, last_pos_disc, player_id)
        # down
        if cur_y < constants.height-1:
            dstPos = point2d(cur_x, cur_y + 1)
            collision = False
            for met in constants.meteor:
                if dstPos == met:
                    collision = True
                    break
            if not collision:
                constants.logger.info('police  down')
                if dstPos in constants.tunnel.keys():
                    finalPos = constants.tunnel_map[dstPos]
                    if finalPos.getX() != player_pos.getX() or finalPos.getY() != player_pos.getY():
                        last_pos_disc = 2
                    else:
                        last_pos_disc = 0
                elif dstPos.getX() != player_last_pos.getX() or dstPos.getY() != player_last_pos.getY():
                    last_pos_disc = 2
                else:
                    last_pos_disc = 0
                choices_gains[2] = computeGainPolice(player_pos, dstPos, last_pos_disc, player_id)
        # left
        if cur_x > 0:
            dstPos = point2d(cur_x - 1, cur_y)
            collision = False
            for met in constants.meteor:
                if dstPos == met:
                    collision = True
                    break
            if not collision:
                constants.logger.info('police  left')
                if dstPos in constants.tunnel.keys():
                    finalPos = constants.tunnel_map[dstPos]
                    if finalPos.getX() != player_pos.getX() or finalPos.getY() != player_pos.getY():
                        last_pos_disc = 2
                    else:
                        last_pos_disc = 0
                elif dstPos.getX() != player_last_pos.getX() or dstPos.getY() != player_last_pos.getY():
                    last_pos_disc = 2
                else:
                    last_pos_disc = 0
                choices_gains[3] = computeGainPolice(player_pos, dstPos, last_pos_disc, player_id)
        # right
        if cur_x < constants.width-1:
            dstPos = point2d(cur_x + 1, cur_y,)
            collision = False
            for met in constants.meteor:
                if dstPos == met:
                    collision = True
                    break
            if not collision:
                constants.logger.info('police  right')
                if dstPos in constants.tunnel.keys():
                    finalPos = constants.tunnel_map[dstPos]
                    if finalPos.getX() != player_pos.getX() or finalPos.getY() != player_pos.getY():
                        last_pos_disc = 2
                    else:
                        last_pos_disc = 0
                elif dstPos.getX() != player_last_pos.getX() or dstPos.getY() != player_last_pos.getY():
                    last_pos_disc = 2
                else:
                    last_pos_disc = 0
                choices_gains[4] = computeGainPolice(player_pos, dstPos, last_pos_disc, player_id)
        # stop
        dstPos = player_pos
        constants.logger.info('police  stop')
        last_pos_disc = 0
        choices_gains[5] = computeGainPolice(player_pos, dstPos, last_pos_disc, player_id)
        
        constants.logger.info('police. choices_gains: ')
        constants.logger.info(choices_gains)
        maxGain = max(choices_gains.values())
        bestChoices = []
        for (k,v) in choices_gains.items():
            if abs(maxGain - v) < constants.EPS:
                bestChoices.append(k)
        choice = random.choice(bestChoices)
    else:
        # thief
        cur_x = player_pos.getX()
        cur_y = player_pos.getY()
        choices_gains = {}
        # up
        if cur_y > 0:
            dstPos = point2d(cur_x, cur_y - 1)
            collision = False
            for met in constants.meteor:
                if dstPos == met:
                    collision = True
                    break
            if not collision:
                constants.logger.info('thief  up')
                if dstPos in constants.tunnel.keys():
                    finalPos = constants.tunnel_map[dstPos]
                    if finalPos.getX() != player_pos.getX() or finalPos.getY() != player_pos.getY():
                        last_pos_disc = 2
                    else:
                        last_pos_disc = 0
                elif dstPos.getX() != player_last_pos.getX() or dstPos.getY() != player_last_pos.getY():
                    last_pos_disc = 2
                else:
                    last_pos_disc = 0
                choices_gains[1] = computeGainThief(player_pos, dstPos, last_pos_disc, player_id)
        # down
        if cur_y < constants.height-1:
            dstPos = point2d(cur_x, cur_y + 1)
            collision = False
            for met in constants.meteor:
                if dstPos == met:
                    collision = True
                    break
            if not collision:
                constants.logger.info('thief  down')
                if dstPos in constants.tunnel.keys():
                    finalPos = constants.tunnel_map[dstPos]
                    if finalPos.getX() != player_pos.getX() or finalPos.getY() != player_pos.getY():
                        last_pos_disc = 2
                    else:
                        last_pos_disc = 0
                elif dstPos.getX() != player_last_pos.getX() or dstPos.getY() != player_last_pos.getY():
                    last_pos_disc = 2
                else:
                    last_pos_disc = 0
                choices_gains[2] = computeGainThief(player_pos, dstPos, last_pos_disc, player_id)
        # left
        if cur_x > 0:
            dstPos = point2d(cur_x - 1, cur_y)
            collision = False
            for met in constants.meteor:
                if dstPos == met:
                    collision = True
                    break
            if not collision:
                constants.logger.info('thief  left')
                if dstPos in constants.tunnel.keys():
                    finalPos = constants.tunnel_map[dstPos]
                    if finalPos.getX() != player_pos.getX() or finalPos.getY() != player_pos.getY():
                        last_pos_disc = 2
                    else:
                        last_pos_disc = 0
                elif dstPos.getX() != player_last_pos.getX() or dstPos.getY() != player_last_pos.getY():
                    last_pos_disc = 2
                else:
                    last_pos_disc = 0
                choices_gains[3] = computeGainThief(player_pos, dstPos, last_pos_disc, player_id)
        # right
        if cur_x < constants.width-1:
            dstPos = point2d(cur_x + 1, cur_y)
            collision = False
            for met in constants.meteor:
                if dstPos == met:
                    collision = True
                    break
            if not collision:
                constants.logger.info('thief  right')
                if dstPos in constants.tunnel.keys():
                    finalPos = constants.tunnel_map[dstPos]
                    if finalPos.getX() != player_pos.getX() or finalPos.getY() != player_pos.getY():
                        last_pos_disc = 2
                    else:
                        last_pos_disc = 0
                elif dstPos.getX() != player_last_pos.getX() or dstPos.getY() != player_last_pos.getY():
                    last_pos_disc = 2
                else:
                    last_pos_disc = 0
                choices_gains[4] = computeGainThief(player_pos, dstPos, last_pos_disc, player_id)
        # stop
        dstPos = player_pos
        constants.logger.info('thief  stop')
        last_pos_disc = 0
        choices_gains[5] = computeGainThief(player_pos, dstPos, last_pos_disc, player_id)
        constants.logger.info('thief. choices_gains: ')
        constants.logger.info(choices_gains)
        maxGain = max(choices_gains.values())
        bestChoices = []
        for (k,v) in choices_gains.items():
            # the constants.EPS can be adjust to be bigger to allow more randomness.
            if abs(maxGain - v) < constants.EPS:
                bestChoices.append(k)
        choice = random.choice(bestChoices)
    return choice