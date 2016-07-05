import simpy
import random, string
import operator
import copy

# collect_amount_list = [1, 2, 3, 4, 6, 9, 13, 19, 28, 41]
# for i in range(10,36):
#     collect_amount_list.append(collect_amount_list[i-3]+collect_amount_list[i-1])
collect_amount_list = [1, 2, 3, 4, 6, 9, 13, 19, 28, 41, 60, 88, 129, 189, 277, 406, 595, 872, 1278, 1873, 2745, 4023, 5896, 8641, 12664, 18560, 27201, 39865, 58425, 85626, 125491, 183916, 269542, 395033, 578949, 848491]

class Doolgi(object):
    collect_amount = 1
    recollect_duration = 1.0
    # recollect_duration = random.uniform(0, 10)
    id = 1
    level = 0

    def __init__(self, env, id, level):
        self.env = env
        self.action = env.process(self.collect())
        self.id = id
        self.level = level
        global collect_amount_list
        self.collect_amount = collect_amount_list[level]


        ### Move these features from generateDoolgi
        dictManage[self] = int(level)
        numDoolgi = len(dictManage)
        # print('--- Doolgi %s is generated at time %d ---' % (self.id, env.now))
        # print('--- Total number of doolgi is %d ---' % numDoolgi)

    def collect(self):
        while True:
            if dictManage.has_key(self):
                # print('Doolgi %s collects %d won at time %.1f' % (self.id, self.collect_amount, self.env.now))
                global gamescore
                gamescore += self.collect_amount
                # print('gamescore: %d' % gamescore)
            yield self.env.timeout(self.recollect_duration)



def generateDoolgi_flowline(env, tick, maxLevel):
    while True:
        numDoolgi = len(dictManage)
        if numDoolgi < 38:
            level = random.randrange(maxLevel)+1
            id = randomword(10)
            new_doolgi = Doolgi(env, id, level)
        yield env.timeout(tick)


def mergeDoolgi_flowline(env, tick, rate):
    yield env.timeout(tick / 2)
    while True:
        mergeDoolgi(env, rate)
        yield env.timeout(tick)


def killDoolgi(env, thisdoolgi):
    del thisdoolgi


def initialize_doolgi(env, level, numDoolgi):
    for i in range(numDoolgi):
        new_doolgi = Doolgi(env, randomword(10), level)


def mergeDoolgi(env, rate):
    global dickManage
    dictforMerge = copy.copy(dictManage)
    try:
        while True:
            temp_cand1 = min(dictforMerge.items(), key=lambda x: x[1])
            dictforMerge.pop(temp_cand1[0])
            temp_cand2 = min(dictforMerge.items(), key=lambda x: x[1])
            if temp_cand1[1] == temp_cand2[1]:
                dictforMerge.pop(temp_cand2[0])
                # print "Merging soon...", temp_cand1[0].id, temp_cand1[0].level
                # print "Merging soon...", temp_cand2[0].id, temp_cand2[0].level
                killDoolgi(env, temp_cand1[0])
                killDoolgi(env, temp_cand2[0])
                dictManage.pop(temp_cand1[0])
                dictManage.pop(temp_cand2[0])
                rv = random.random()
                if rv >= rate:
                    # print rv, rate
                    new_doolgi = Doolgi(env, randomword(10), temp_cand1[1]+1)
                    # print "Outcome doolgi...", new_doolgi.id, new_doolgi.level
                else:
                    # print rv, rate
                    new_doolgi = Doolgi(env, randomword(10), temp_cand1[1]+2)
                    # print "Outcome doolgi...", new_doolgi.id, new_doolgi.level
                break
    except ValueError:
        pass
        # print("Oops! Not enough Doolgi to proceed merging process.")

def randomword(length):
   return ''.join(random.choice(string.lowercase) for i in range(length))


dictManage = dict()
gamescore = 0

# parameter1 = [10, 0.12, 30, 200]  ### maxLevel, doubleUpgradeRate, intervalMerge, intervalBeaver
#
# def playDoolgiGame(paramList):
#     repeatedResults = dict()
#     for i in range(10):
#         env = simpy.Environment()
#         gamescore = 0
#
#         maxLevel = paramList[0]
#         doubleUpgradeRate = paramList[1]   # probability
#         intervalMerge = paramList[2]      # second
#         intervalBeaver = paramList[3]
#
#         for i in range(10):
#             env.process(generateDoolgi_flowline(env, intervalMerge, maxLevel))
#             env.process(mergeDoolgi_flowline(env, intervalMerge, doubleUpgradeRate))
#             runtime = 400
#             env.run(until=(i+1)*runtime)
#             if i == 9:
#                 thisStatus = sorted(dictManage.values())
#                 print 'Doolgi status: ', thisStatus
#         print('Final gamescore after time %d is %d' % (runtime, gamescore))
#         repeatedResults[gamescore] = thisStatus
#     return repeatedResults
#
# print playDoolgiGame()

