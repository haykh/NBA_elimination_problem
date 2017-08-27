#!/bin/python3

import numpy as np

#getting game logs
gamelogs=np.genfromtxt('2016_17_NBA_Scores-Table.csv', delimiter=';', unpack=True, dtype=None)

#getting division info
divinfo=np.genfromtxt('Division_Info-Table1.csv', delimiter=';', unpack=True, dtype=None)

#output file for the result
clinch_dates=np.genfromtxt('Sample_NBA_Clinch_Dates-Table1.csv', delimiter=';', unpack=True, dtype=None)

#define the function which prints the conference standings nicely
def PrintConf(arrayy):
    print '{0:29} {1:10}'.format('Team', 'W     L  WinPercentage PointDiff')
    for i in range(15):
        print '{0:25} {1:5d} {2:5d} {3:10.2f} {4:10d}'.format(arrayy[i][0], int(arrayy[i][1]),int(arrayy[i][2]),arrayy[i][3],int(arrayy[i][4]))
    print('\n')
    return


#read all dates

dates=[]
i=0
while i<1230:
    dates.append(gamelogs[0,1+i])
    i=i+1

def getUniqueItems(iterable):
    result = []
    for item in iterable:
        if item not in result:
            result.append(item)
    return result

dates=getUniqueItems(dates)

#number of gameday
gameday=80


#define conference standings table

w, h = 5, 15;
WestTeams=[]


EastTeams=[]


#west and east teams
for i in range(30):
    if (divinfo[2,i+1]=='West'):
        WestTeams.append(divinfo[0,i+1])
    else:
        EastTeams.append(divinfo[0,i+1])


WestConf = [[0.0 for x in range(w)] for y in range(h)]

EastConf = [[0.0 for x in range(w)] for y in range(h)]


games_left = [[0 for x in range(31)] for y in range(31)]

HeadToHead = [[0 for x in range(31)] for y in range(31)]



for i in range(15):
    games_left[i+1][0]=WestTeams[i]

for i in range(15):
    games_left[i+16][0]=EastTeams[i]

for i in range(15):
    games_left[0][i+1]=WestTeams[i]

for i in range(15):
    games_left[0][i+16]=EastTeams[i]

    #print(games_left)


    #fill tables with the teams' names
for i in range(15):
    WestConf[i][0]=WestTeams[i]

for i in range(15):
    EastConf[i][0]=EastTeams[i]




for i in range(15):
    HeadToHead[i+1][0]=WestTeams[i]

for i in range(15):
    HeadToHead[i+16][0]=EastTeams[i]

for i in range(15):
    HeadToHead[0][i+1]=WestTeams[i]

for i in range(15):
    HeadToHead[0][i+16]=EastTeams[i]




#iterate through the game logs and fill in wins, losses, and point differential in WestConf and East Conf arrays

def process_data(gameday):


    if gameday<=161:
        for i in range(1230):
            if (gamelogs[0,i+1]!=dates[gameday]):
                if gamelogs[1,1+i] in WestTeams:
                    for k in range(15):
                        if(str(WestConf[k][0])==str(gamelogs[1,i+1])):
                            if (gamelogs[5,i+1]=='Home'):
                                WestConf[k][1]=WestConf[k][1]+1
                                WestConf[k][3]=WestConf[k][1]/(WestConf[k][1]+WestConf[k][2])*100.0
                                WestConf[k][4]=WestConf[k][4]+int(gamelogs[3,1+i])-int(gamelogs[4,1+i])
                            if (gamelogs[5,1+i]=='Away'):
                                WestConf[k][2]=WestConf[k][2]+1
                                WestConf[k][3]=WestConf[k][1]/(WestConf[k][1]+WestConf[k][2])*100.0
                                WestConf[k][4]=WestConf[k][4]+int(gamelogs[3,1+i])-int(gamelogs[4,1+i])

                if gamelogs[1,1+i] in EastTeams:
                    for l in range(15):
                        if(EastConf[l][0]==gamelogs[1,1+i]):
                            if (gamelogs[5,1+i]=='Home'):
                                EastConf[l][1]=EastConf[l][1]+1
                                EastConf[l][3]=EastConf[l][1]/(EastConf[l][1]+EastConf[l][2])*100.0
                                EastConf[l][4]=EastConf[l][4]+int(gamelogs[3,1+i])-int(gamelogs[4,1+i])
                            else:
                                EastConf[l][2]=EastConf[l][2]+1
                                EastConf[l][3]=EastConf[l][1]/(EastConf[l][1]+EastConf[l][2])*100.0
                                EastConf[l][4]=EastConf[l][4]+int(gamelogs[3,1+i])-int(gamelogs[4,1+i])

                if gamelogs[2,1+i] in WestTeams:
                    for k in range(15):
                        if(WestConf[k][0]==gamelogs[2,1+i]):
                            if (gamelogs[5,1+i]=='Home'):
                                WestConf[k][2]=WestConf[k][2]+1
                                WestConf[k][3]=WestConf[k][1]/(WestConf[k][1]+WestConf[k][2])*100.0
                                WestConf[k][4]=WestConf[k][4]+int(gamelogs[4,1+i])-int(gamelogs[3,1+i])
                            else:
                                WestConf[k][1]=WestConf[k][1]+1
                                WestConf[k][3]=WestConf[k][1]/(WestConf[k][1]+WestConf[k][2])*100.0
                                WestConf[k][4]=WestConf[k][4]+int(gamelogs[4,1+i])-int(gamelogs[3,1+i])

                if gamelogs[2,1+i] in EastTeams:
                    for k in range(15):
                        if(EastConf[k][0]==gamelogs[2,1+i]):
                            if (gamelogs[5,1+i]=='Home'):
                                EastConf[k][2]=EastConf[k][2]+1
                                EastConf[k][3]=EastConf[k][1]/(EastConf[k][1]+EastConf[k][2])*100.0
                                EastConf[k][4]=EastConf[k][4]+int(gamelogs[4,1+i])-int(gamelogs[3,1+i])
                            else:
                                EastConf[k][1]=EastConf[k][1]+1
                                EastConf[k][3]=EastConf[k][1]/(EastConf[k][1]+EastConf[k][2])*100.0
                                EastConf[k][4]=EastConf[k][4]+int(gamelogs[4,1+i])-int(gamelogs[3,1+i])

                for p in range(31):
                    if (gamelogs[1,1+i]==games_left[p][0]):
                        for z in range(31):
                            if (gamelogs[2,1+i]==games_left[0][z]):
                                games_left[z][p]=games_left[z][p]-1
                                games_left[p][z]=games_left[p][z]-1
                                if (gamelogs[5,1+i]=="Home"):
                                    HeadToHead[p][z]=HeadToHead[p][z]+1
                                else:
                                    HeadToHead[z][p]=HeadToHead[z][p]+1
            else:
                break


    if gameday>=162:
        for i in range(1230):
                if gamelogs[1,1+i] in WestTeams:
                    for k in range(15):
                        if(str(WestConf[k][0])==str(gamelogs[1,i+1])):
                            if (gamelogs[5,i+1]=='Home'):
                                WestConf[k][1]=WestConf[k][1]+1
                                WestConf[k][3]=WestConf[k][1]/(WestConf[k][1]+WestConf[k][2])*100.0
                                WestConf[k][4]=WestConf[k][4]+int(gamelogs[3,1+i])-int(gamelogs[4,1+i])
                            if (gamelogs[5,1+i]=='Away'):
                                WestConf[k][2]=WestConf[k][2]+1
                                WestConf[k][3]=WestConf[k][1]/(WestConf[k][1]+WestConf[k][2])*100.0
                                WestConf[k][4]=WestConf[k][4]+int(gamelogs[3,1+i])-int(gamelogs[4,1+i])

                if gamelogs[1,1+i] in EastTeams:
                    for l in range(15):
                        if(EastConf[l][0]==gamelogs[1,1+i]):
                            if (gamelogs[5,1+i]=='Home'):
                                EastConf[l][1]=EastConf[l][1]+1
                                EastConf[l][3]=EastConf[l][1]/(EastConf[l][1]+EastConf[l][2])*100.0
                                EastConf[l][4]=EastConf[l][4]+int(gamelogs[3,1+i])-int(gamelogs[4,1+i])
                            else:
                                EastConf[l][2]=EastConf[l][2]+1
                                EastConf[l][3]=EastConf[l][1]/(EastConf[l][1]+EastConf[l][2])*100.0
                                EastConf[l][4]=EastConf[l][4]+int(gamelogs[3,1+i])-int(gamelogs[4,1+i])

                if gamelogs[2,1+i] in WestTeams:
                    for k in range(15):
                        if(WestConf[k][0]==gamelogs[2,1+i]):
                            if (gamelogs[5,1+i]=='Home'):
                                WestConf[k][2]=WestConf[k][2]+1
                                WestConf[k][3]=WestConf[k][1]/(WestConf[k][1]+WestConf[k][2])*100.0
                                WestConf[k][4]=WestConf[k][4]+int(gamelogs[4,1+i])-int(gamelogs[3,1+i])
                            else:
                                WestConf[k][1]=WestConf[k][1]+1
                                WestConf[k][3]=WestConf[k][1]/(WestConf[k][1]+WestConf[k][2])*100.0
                                WestConf[k][4]=WestConf[k][4]+int(gamelogs[4,1+i])-int(gamelogs[3,1+i])

                if gamelogs[2,1+i] in EastTeams:
                    for k in range(15):
                        if(EastConf[k][0]==gamelogs[2,1+i]):
                            if (gamelogs[5,1+i]=='Home'):
                                EastConf[k][2]=EastConf[k][2]+1
                                EastConf[k][3]=EastConf[k][1]/(EastConf[k][1]+EastConf[k][2])*100.0
                                EastConf[k][4]=EastConf[k][4]+int(gamelogs[4,1+i])-int(gamelogs[3,1+i])
                            else:
                                EastConf[k][1]=EastConf[k][1]+1
                                EastConf[k][3]=EastConf[k][1]/(EastConf[k][1]+EastConf[k][2])*100.0
                                EastConf[k][4]=EastConf[k][4]+int(gamelogs[4,1+i])-int(gamelogs[3,1+i])

                for p in range(31):
                    if (gamelogs[1,1+i]==games_left[p][0]):
                        for z in range(31):
                            if (gamelogs[2,1+i]==games_left[0][z]):
                                games_left[z][p]=games_left[z][p]-1
                                games_left[p][z]=games_left[p][z]-1
                                if (gamelogs[5,1+i]=="Home"):
                                    HeadToHead[p][z]=HeadToHead[p][z]+1
                                else:
                                    HeadToHead[z][p]=HeadToHead[z][p]+1



    for i in range(1230):
            for p in range(31):
                if (gamelogs[1,1+i]==games_left[p][0]):
                    for z in range(31):
                        if (gamelogs[2,1+i]==games_left[0][z]):
                            games_left[z][p]=games_left[z][p]+1
                            games_left[p][z]=games_left[p][z]+1

    return 0


#print(process_data(162))
#print(games_left)

#PrintConf(WestConf)
#PrintConf(EastConf)

#preliminary sorting of the table - no tiebreaker yet

#WestConf.sort(key=lambda x: x[3],reverse=True)
#EastConf.sort(key=lambda x: x[3],reverse=True)

#print the resulting table

#PrintConf(WestConf)
#PrintConf(EastConf)

#print(H2HPacific)

#calculate everything to this date


def wins(gday, k, conf):
    for x in range(h):
        for y in range(w):
            WestConf[x][y]=0.0

    for x in range(h):
        for y in range(w):
            EastConf[x][y]=0.0
    for x in range(31):
        for y in range(31):
            games_left[x][y]=0.0


    for i in range(15):
        games_left[i+1][0]=WestTeams[i]

    for i in range(15):
        games_left[i+16][0]=EastTeams[i]

    for i in range(15):
        games_left[0][i+1]=WestTeams[i]

    for i in range(15):
        games_left[0][i+16]=EastTeams[i]

        #print(games_left)


        #fill tables with the teams' names
    for i in range(15):
        WestConf[i][0]=WestTeams[i]

    for i in range(15):
        EastConf[i][0]=EastTeams[i]

    process_data(gday)
    if conf == "west":
        return int(WestConf[k][1])
    else:
        return int(EastConf[k][1])



def h2h(gday, k,j,conf):
    for x in range(h):
        for y in range(w):
            WestConf[x][y]=0.0

    for x in range(h):
        for y in range(w):
            EastConf[x][y]=0.0
    for x in range(31):
        for y in range(31):
            games_left[x][y]=0.0
    for x in range(31):
        for y in range(31):
            HeadToHead[x][y]=0.0

    for i in range(15):
        games_left[i+1][0]=WestTeams[i]

    for i in range(15):
        games_left[i+16][0]=EastTeams[i]

    for i in range(15):
        games_left[0][i+1]=WestTeams[i]

    for i in range(15):
        games_left[0][i+16]=EastTeams[i]

        #print(games_left)


        #fill tables with the teams' names
    for i in range(15):
        WestConf[i][0]=WestTeams[i]

    for i in range(15):
        EastConf[i][0]=EastTeams[i]


    for i in range(15):
        HeadToHead[i+1][0]=WestTeams[i]

    for i in range(15):
        HeadToHead[i+16][0]=EastTeams[i]

    for i in range(15):
        HeadToHead[0][i+1]=WestTeams[i]

    for i in range(15):
        HeadToHead[0][i+16]=EastTeams[i]

    process_data(gday)

#    print(HeadToHead[0][k+16])
#    print(HeadToHead[0][j+16])

    if (conf=="west"):
        return int(HeadToHead[k+1][j+1])
    if (conf=="east"):
        return int(HeadToHead[k+16][j+16])



#print(wins(161,2,"west"))
#print(games_left)

#PrintConf(WestConf)
#PrintConf(EastConf)

def gamesleft(gday, p, conf1, j, conf2):

    for x in range(h):
        for y in range(w):
            WestConf[x][y]=0.0

    for x in range(h):
        for y in range(w):
            EastConf[x][y]=0.0
    for x in range(31):
        for y in range(31):
            games_left[x][y]=0.0


    for i in range(15):
        games_left[i+1][0]=WestTeams[i]

    for i in range(15):
        games_left[i+16][0]=EastTeams[i]

    for i in range(15):
        games_left[0][i+1]=WestTeams[i]

    for i in range(15):
        games_left[0][i+16]=EastTeams[i]

        #print(games_left)


        #fill tables with the teams' names
    for i in range(15):
        WestConf[i][0]=WestTeams[i]

    for i in range(15):
        EastConf[i][0]=EastTeams[i]

    process_data(gday)
    if (conf1=="west" and conf2=="west"):
        return int(games_left[p+1][j+1])
    if (conf1=="east" and conf2=="west"):
        return int(games_left[p+16][j+1])

    if (conf1=="west" and conf2=="east"):
        return int(games_left[p+1][j+16])
    if (conf1=="east" and conf2=="east"):
        return int(games_left[p+16][j+16])


#print(gamesleft(162,0,"west",1,"east"))
#print(gamesleft(0,0,"west",1,"east"))


#print(h2h(160,5,6,"east"))
#print(HeadToHead)
