import numpy as np
from pulp import *

from init import EastTeams, WestTeams, dates, wins, gamesleft
from write_inits import read_gamesleft, read_h2h

max_difference = 90
playoff_teams = 8

start_from = 120

for team_k in range(len(EastTeams)):
    # EASTS PLAY
    date1 = 'None'
    date2 = 'None'
    # print EastTeams[team_k]
    # Strong constraint eliminations (early)
    for date_i in range(start_from, len(dates) + 1): # TO BE FIXED
        # wins all EAST teams have so far
        wins_sofar = [wins(date_i, j, "east") for j in range(len(EastTeams))]

        # play all inter-conference games in our favor
        for j in range(len(WestTeams)):
            wins_sofar[team_k] += read_gamesleft(date_i, team_k, "east", j, "west")

        #
        # optimization problem
        #
        number_of_teams = len(EastTeams)
        prob = LpProblem(EastTeams[team_k] + "_" + dates[date_i - 1], LpMinimize)

        # variables
        xs = [LpVariable("x_{0}_{1}".format(i, j), lowBound = 0, cat = "Integer")\
              for i in range(number_of_teams) for j in [x for x in xrange(number_of_teams) if x != i]]
        zs = [LpVariable("z_{0}".format(i), cat = "Binary") \
              for i in [x for x in xrange(number_of_teams) if x != team_k]]

        def getIndex1(indI, indJ):
            index = 0
            test_arr = [[i, j] for i in range(number_of_teams) for j in [x for x in xrange(number_of_teams) if x != i]]
            for k in test_arr:
                if [indI, indJ] == k:
                    return index
                else:
                    index += 1
        def getIndex2(indI):
            index = 0
            test_arr = [x for x in xrange(number_of_teams) if x != team_k]
            for k in test_arr:
                if indI == k:
                    return index
                else:
                    index += 1

        # function to minimize
        prob += sum([xs[getIndex1(team_k, i)] for i in [x for x in xrange(number_of_teams) if x != team_k]])

        # constraints #1
        for i in range(number_of_teams - 1):
            for j in range(i + 1, number_of_teams):
                prob += xs[getIndex1(i, j)] + xs[getIndex1(j, i)] == read_gamesleft(date_i, i, "east", j, 'east')

        # constraints #2
        def totalPoints(j):
            return wins_sofar[j] + \
                sum([xs[getIndex1(j, i)] for i in [x for x in xrange(number_of_teams) if x != j]])

        for j in [x for x in xrange(number_of_teams) if x != team_k]:
            prob += (totalPoints(j) - totalPoints(team_k)) <= \
                max_difference * zs[getIndex2(j)] - 1

        #constraints #3
        prob += sum([zs[getIndex2(j)] for j in [x for x in xrange(number_of_teams) if x != team_k]]) <= playoff_teams - 1
        # prob.writeLP(EastTeams[team_k] + "_" + str(date_i) + ".lp")
        prob.solve(PULP_CBC_CMD())

        if prob.status == 1:
            continue
        else:
            # print "eliminated in", dates[date_i - 1]
            date1 = dates[date_i - 1]
            break

    # Weak constraint eliminations (late)
    for date_i in range(start_from, len(dates) + 1): # TO BE FIXED
        # wins all EAST teams have so far
        wins_sofar = [wins(date_i, j, "east") for j in range(len(EastTeams))]

        # play all inter-conference games in our favor
        for j in range(len(WestTeams)):
            wins_sofar[team_k] += read_gamesleft(date_i, team_k, "east", j, "west")

        #
        # optimization problem
        #
        number_of_teams = len(EastTeams)
        prob = LpProblem(EastTeams[team_k] + "_" + dates[date_i - 1], LpMinimize)

        # variables
        xs = [LpVariable("x_{0}_{1}".format(i, j), lowBound = 0, cat = "Integer") \
              for i in range(number_of_teams) for j in [x for x in xrange(number_of_teams) if x != i]]
        zs = [LpVariable("z_{0}".format(i), cat = "Binary") \
              for i in [x for x in xrange(number_of_teams) if x != team_k]]

        def getIndex1(indI, indJ):
            index = 0
            test_arr = [[i, j] for i in range(number_of_teams) for j in [x for x in xrange(number_of_teams) if x != i]]
            for k in test_arr:
                if [indI, indJ] == k:
                    return index
                else:
                    index += 1
        def getIndex2(indI):
            index = 0
            test_arr = [x for x in xrange(number_of_teams) if x != team_k]
            for k in test_arr:
                if indI == k:
                    return index
                else:
                    index += 1

        # function to minimize
        prob += sum([xs[getIndex1(team_k, i)] for i in [x for x in xrange(number_of_teams) if x != team_k]])

        # constraints #1
        for i in range(number_of_teams - 1):
            for j in range(i + 1, number_of_teams):
                prob += xs[getIndex1(i, j)] + xs[getIndex1(j, i)] == read_gamesleft(date_i, i, "east", j, 'east')

        # constraints #2
        def totalPoints(j):
            return wins_sofar[j] + \
                sum([xs[getIndex1(j, i)] for i in [x for x in xrange(number_of_teams) if x != j]])

        for j in [x for x in xrange(number_of_teams) if x != team_k]:
            h2h_total_jk = xs[getIndex1(j, team_k)] + read_h2h(date_i, j, team_k, "east")
            h2h_total_kj = xs[getIndex1(team_k, j)] + read_h2h(date_i, team_k, j, "east")
            prob += (totalPoints(j) - totalPoints(team_k)) + \
                    (h2h_total_jk - h2h_total_kj) * 0.001 <= \
                max_difference * zs[getIndex2(j)]

        #constraints #3
        prob += sum([zs[getIndex2(j)] for j in [x for x in xrange(number_of_teams) if x != team_k]]) <= playoff_teams - 1
        # prob.writeLP(EastTeams[team_k] + "_" + str(date_i) + ".lp")
        prob.solve(PULP_CBC_CMD())

        if prob.status == 1:
            continue
        else:
            # print "eliminated in", dates[date_i - 1]
            date2 = dates[date_i - 1]
            break
    if date1 == 'None' or date2 == 'None':
        print EastTeams[team_k], "Playoffs"
    else:
        if date1 == date2:
            print EastTeams[team_k], date1
        else:
            print EastTeams[team_k], date1, date2

    # results.append([EastTeams[team_k], date1, date2])


for team_k in range(len(WestTeams)):
    # WESTS PLAY
    date1 = 'None'
    date2 = 'None'
    # print WestTeams[team_k]
    # Strong constraint eliminations (early)
    for date_i in range(start_from, len(dates) + 1): # TO BE FIXED
        # wins all WEST teams have so far
        wins_sofar = [wins(date_i, j, "west") for j in range(len(WestTeams))]

        # play all inter-conference games in our favor
        for j in range(len(EastTeams)):
            wins_sofar[team_k] += read_gamesleft(date_i, team_k, "west", j, "east")

        #
        # optimization problem
        #
        number_of_teams = len(WestTeams)
        prob = LpProblem(WestTeams[team_k] + "_" + dates[date_i - 1], LpMinimize)

        # variables
        xs = [LpVariable("x_{0}_{1}".format(i, j), lowBound = 0, cat = "Integer")\
              for i in range(number_of_teams) for j in [x for x in xrange(number_of_teams) if x != i]]
        zs = [LpVariable("z_{0}".format(i), cat = "Binary") \
              for i in [x for x in xrange(number_of_teams) if x != team_k]]

        def getIndex1(indI, indJ):
            index = 0
            test_arr = [[i, j] for i in range(number_of_teams) for j in [x for x in xrange(number_of_teams) if x != i]]
            for k in test_arr:
                if [indI, indJ] == k:
                    return index
                else:
                    index += 1
        def getIndex2(indI):
            index = 0
            test_arr = [x for x in xrange(number_of_teams) if x != team_k]
            for k in test_arr:
                if indI == k:
                    return index
                else:
                    index += 1

        # function to minimize
        prob += sum([xs[getIndex1(team_k, i)] for i in [x for x in xrange(number_of_teams) if x != team_k]])

        # constraints #1
        for i in range(number_of_teams - 1):
            for j in range(i + 1, number_of_teams):
                prob += xs[getIndex1(i, j)] + xs[getIndex1(j, i)] == read_gamesleft(date_i, i, "west", j, 'west')

        # constraints #2
        def totalPoints(j):
            return wins_sofar[j] + \
                sum([xs[getIndex1(j, i)] for i in [x for x in xrange(number_of_teams) if x != j]])

        for j in [x for x in xrange(number_of_teams) if x != team_k]:
            prob += (totalPoints(j) - totalPoints(team_k)) <= \
                max_difference * zs[getIndex2(j)] - 1

        #constraints #3
        prob += sum([zs[getIndex2(j)] for j in [x for x in xrange(number_of_teams) if x != team_k]]) <= playoff_teams - 1
        # prob.writeLP(EastTeams[team_k] + "_" + str(date_i) + ".lp")
        prob.solve(PULP_CBC_CMD())

        if prob.status == 1:
            continue
        else:
            # print "eliminated in", dates[date_i - 1]
            date1 = dates[date_i - 1]
            break

    # Weak constraint eliminations (late)
    for date_i in range(start_from, len(dates) + 1): # TO BE FIXED
        # wins all WEST teams have so far
        wins_sofar = [wins(date_i, j, "west") for j in range(len(WestTeams))]

        # play all inter-conference games in our favor
        for j in range(len(EastTeams)):
            wins_sofar[team_k] += read_gamesleft(date_i, team_k, "west", j, "east")

        #
        # optimization problem
        #
        number_of_teams = len(WestTeams)
        prob = LpProblem(WestTeams[team_k] + "_" + dates[date_i - 1], LpMinimize)

        # variables
        xs = [LpVariable("x_{0}_{1}".format(i, j), lowBound = 0, cat = "Integer")\
              for i in range(number_of_teams) for j in [x for x in xrange(number_of_teams) if x != i]]
        zs = [LpVariable("z_{0}".format(i), cat = "Binary") \
              for i in [x for x in xrange(number_of_teams) if x != team_k]]

        def getIndex1(indI, indJ):
            index = 0
            test_arr = [[i, j] for i in range(number_of_teams) for j in [x for x in xrange(number_of_teams) if x != i]]
            for k in test_arr:
                if [indI, indJ] == k:
                    return index
                else:
                    index += 1
        def getIndex2(indI):
            index = 0
            test_arr = [x for x in xrange(number_of_teams) if x != team_k]
            for k in test_arr:
                if indI == k:
                    return index
                else:
                    index += 1

        # function to minimize
        prob += sum([xs[getIndex1(team_k, i)] for i in [x for x in xrange(number_of_teams) if x != team_k]])

        # constraints #1
        for i in range(number_of_teams - 1):
            for j in range(i + 1, number_of_teams):
                prob += xs[getIndex1(i, j)] + xs[getIndex1(j, i)] == read_gamesleft(date_i, i, "west", j, 'west')

        # constraints #2
        def totalPoints(j):
            return wins_sofar[j] + \
                sum([xs[getIndex1(j, i)] for i in [x for x in xrange(number_of_teams) if x != j]])

        for j in [x for x in xrange(number_of_teams) if x != team_k]:
            h2h_total_jk = xs[getIndex1(j, team_k)] + read_h2h(date_i, j, team_k, "west")
            h2h_total_kj = xs[getIndex1(team_k, j)] + read_h2h(date_i, team_k, j, "west")
            prob += (totalPoints(j) - totalPoints(team_k)) + \
                    (h2h_total_jk - h2h_total_kj) * 0.001 <= \
                max_difference * zs[getIndex2(j)]

        #constraints #3
        prob += sum([zs[getIndex2(j)] for j in [x for x in xrange(number_of_teams) if x != team_k]]) <= playoff_teams - 1
        # prob.writeLP(EastTeams[team_k] + "_" + str(date_i) + ".lp")
        prob.solve(PULP_CBC_CMD())

        if prob.status == 1:
            continue
        else:
            # print "eliminated in", dates[date_i - 1]
            date2 = dates[date_i - 1]
            break
    if date1 == 'None' or date2 == 'None':
        print WestTeams[team_k], "Playoffs"
    else:
        if date1 == date2:
            print WestTeams[team_k], date1
        else:
            print WestTeams[team_k], date1, date2

    # results.append([WestTeams[team_k], date1, date2])
