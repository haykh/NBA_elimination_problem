import numpy as np
import helper as hlp
from init import EastTeams, WestTeams, dates, wins, gamesleft, h2h

def write_gamesleft():
    root = 'gamesleft/'
    for date_i in range(161, len(dates) + 1):
        for i in range(len(EastTeams)):
            index = 0
            gij = np.array([0] * (len(EastTeams) + len(WestTeams)))
            for j in range(len(EastTeams)):
                if i != j:
                    gij[index] = gamesleft(date_i, i, "east", j, "east")
                index += 1
            for j in range(len(WestTeams)):
                gij[index] = gamesleft(date_i, i, "east", j, "west")
                index += 1

            np.savetxt(root + str(date_i) + '_' + EastTeams[i] + '.dat', gij, delimiter = ' ')

        for i in range(len(WestTeams)):
            index = 0
            gij = np.array([0] * (len(EastTeams) + len(WestTeams)))
            for j in range(len(WestTeams)):
                if i != j:
                    gij[index] = gamesleft(date_i, i, "west", j, "west")
                index += 1
            for j in range(len(EastTeams)):
                gij[index] = gamesleft(date_i, i, "west", j, "east")
                index += 1

            np.savetxt(root + str(date_i) + '_' + WestTeams[i] + '.dat', gij, delimiter = ' ')

        hlp.printProgress(date_i, len(dates) - 1, prefix = 'Progress:', barLength = 50)

def write_h2h():
    root = 'h2h/'
    for date_i in range(len(dates) + 1):
        for i in range(len(EastTeams)):
            index = 0
            qij = np.array([0] * len(EastTeams))
            for j in range(len(EastTeams)):
                if i != j:
                    qij[index] = h2h(date_i, i, j, "east")
                index += 1
            np.savetxt(root + str(date_i) + '_' + EastTeams[i] + '.dat', qij, delimiter = ' ')

        for i in range(len(WestTeams)):
            index = 0
            qij = np.array([0] * len(WestTeams))
            for j in range(len(WestTeams)):
                if i != j:
                    qij[index] = h2h(date_i, i, j, "west")
                index += 1
            np.savetxt(root + str(date_i) + '_' + WestTeams[i] + '.dat', qij, delimiter = ' ')

        hlp.printProgress(date_i, len(dates) - 1, prefix = 'Progress:', barLength = 50)

def read_gamesleft(date_i, i, EWstring_i, j, EWstring_j):
    root = 'gamesleft/'
    if EWstring_i == 'east':
        team_1 = EastTeams[i]
    else:
        team_1 = WestTeams[i]
    if EWstring_j == 'east':
        team_2 = EastTeams[j]
    else:
        team_2 = WestTeams[j]
    index = j
    if EWstring_i != EWstring_j:
        index += 15
    gij = np.loadtxt(root + str(date_i) + '_' + team_1 + '.dat')
    return gij[index]

def read_h2h(date_i, i, j, EWstring):
    root = 'h2h/'
    if EWstring == 'east':
        team_1 = EastTeams[i]
    else:
        team_1 = WestTeams[i]
    index = j
    qij = np.loadtxt(root + str(date_i) + '_' + team_1 + '.dat')
    return qij[index]
