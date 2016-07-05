import trial_doolgi as td
import simpy
import numpy
import csv



def playDoolgiGame(paramList):
    repeatedResults = dict()
    numExp = paramList[5]
    for i in range(numExp):
        # dictManage = td.dictManage
        # gamescore = td.gamescore
        env = simpy.Environment()
        maxLevel = paramList[0]
        doubleUpgradeRate = paramList[1]   # probability
        intervalMerge = paramList[2]      # second
        intervalBeaver = paramList[3]
        runtime = paramList[4]
        itr = 1


        td.initialize_doolgi(env, 14, 2)
        td.initialize_doolgi(env, 13, 8)
        td.initialize_doolgi(env, 13, 6)
        td.initialize_doolgi(env, 12, 3)
        td.initialize_doolgi(env, 11, 2)
        td.initialize_doolgi(env, 10, 2)
        td.initialize_doolgi(env, 9, 3)
        td.initialize_doolgi(env, 7, 2)
        td.initialize_doolgi(env, 6, 1)
        td.initialize_doolgi(env, 5, 2)
        td.initialize_doolgi(env, 4, 2)
        td.initialize_doolgi(env, 3, 1)
        td.initialize_doolgi(env, 1, 2)



        for i in range(itr):
            env.process(td.generateDoolgi_flowline(env, intervalMerge, maxLevel))
            env.process(td.mergeDoolgi_flowline(env, intervalMerge, doubleUpgradeRate))
            env.run(until=(i+1)*runtime)
            if i == (itr-1):
                thisStatus = sorted(td.dictManage.values())
        #         print 'Doolgi status: ', thisStatus
        # print('Final gamescore after time %d is %d' % (runtime, td.gamescore))
        repeatedResults[td.gamescore] = thisStatus
        td.dictManage = dict()
        td.gamescore = 0
    return repeatedResults


# ### Toy experiment
# # Parameter: maxLevel, doubleUpgradeRate, intervalMerge, intervalBeaver, runtime, numExp
# parameter1 = [10, 0.12, 30, 200, 4000, 3]   # Control group
# parameter2 = [10, 0.14, 30, 200, 4000, 3]   # Doubly Upgrade rate + 2%
# parameter3 = [10, 0.12, 29, 200, 4000, 3]   # Merge interval - 1 second
# parameter4 = [11, 0.12, 30, 200, 4000, 3]   # maxLevel(feed) + 1
#
# print numpy.mean(playDoolgiGame(parameter1).keys())
# print numpy.mean(playDoolgiGame(parameter2).keys())
# print numpy.mean(playDoolgiGame(parameter3).keys())
# print numpy.mean(playDoolgiGame(parameter4).keys())


maxLevel = [10, 11, 12, 13]
upgradeRate = [0.10, 0.12, 0.14, 0.16, 0.18, 0.20]
mergeInterval = [30, 29, 28, 27, 26, 25]
intervalBeaver, runtime, numExp = 200, 30000, 30

# maxLevel = [10]
# upgradeRate = [0.10, 0.12]
# mergeInterval = [30, 29]
# intervalBeaver, runtime, numExp = 200, 40000, 20

with open('doolgi_experiment_result.csv', 'wb') as csvfile:
    resultWriter = csv.writer(csvfile, delimiter=',', quoting=csv.QUOTE_MINIMAL)
    title_trial_list = []
    for i in range(1,numExp+1):
        title_trial_list.append('score_trial_'+str(i))
    resultWriter.writerow(['maxLevel', 'upgradeRate', 'mergeInterval', 'beaverInterval', 'runtime', 'numExperiment', 'avgScore'] + title_trial_list)
    for level in maxLevel:
        for rate in upgradeRate:
            for interval in mergeInterval:
                parameter = [level, rate, interval, intervalBeaver, runtime, numExp]
                eachScore = playDoolgiGame(parameter).keys()
                avgScore = numpy.mean(eachScore)
                print parameter, "---", avgScore
                resultList = [level, rate, interval, intervalBeaver, runtime, numExp, avgScore] + eachScore
                resultWriter.writerow(resultList)
