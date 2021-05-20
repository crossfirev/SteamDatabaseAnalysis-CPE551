##
##          Steam Dataset Analysis
##          CPE 551 - Final Project
##
## Author:Matthew Lepis
## Date of Last Edit: 5/19/2021
##
## Dataset Used: Steam Store Games (Clean dataset)')
##             : Includes game database information gathered from May 2019')
##             : https://www.kaggle.com/nikdavis/steam-store-games?select=steam.csv')
##
## Demonstration:       https://www.youtube.com/watch?v=pZ9TigDik6w
## GitHub Repository:   https://github.com/crossfirev/SteamDatabaseAnalysis-CPE551
##

from tqdm import tqdm
import pandas as pd
from time import sleep
import matplotlib.pyplot as plt

def developerOp(data, numOfGames, stepCount, numOfGamesThreshold, numOnGraph, showGraph):
    # Extracting unique developer names
    uniqueDevs = data['developer'].unique()

    # Checks for multiple developers and splits, for future operation
    for i in range(len(uniqueDevs)):
        if ";" in uniqueDevs[i]: #uniqueDevs[i].find(';') != -1:
            uniqueDevs[i] = uniqueDevs[i].split(';')

    # devData is a 2D list, [0] 1st column is the name of a developer (it is a list of unique developers)   [type: str/list (depending on dev count)]
    #                       [1] 2nd column is the developer score                                           [type: float]
    #                       [2] 3rd column is the number of games they have in this dataset sample          [type: int]
    devData = [uniqueDevs, [0]*len(uniqueDevs), [0]*len(uniqueDevs)]

    print('[ ', stepCount, ' ] |\tAverage game review scores, by Developer', '\t\t\t|')
    tqdmDesc = ''.join(['[ ', str(stepCount), '.1 ] |\tProcessing Developer Statistics...', '\t\t\t\t\t|'])
    sleep(2)
    for i in tqdm(range(numOfGames), desc= tqdmDesc): # Selects a game sample; also runs a progress bar
        for j in range(len(devData[0])): # Iterates through the unique dev list, compares to the selected game's dev, then adds the score to that dev's score
            if type(devData[0][j]) == str: # Checking if single developer
                if devData[0][j] in data['developer'].iloc[i]:
                    devData[1][j] += data['percent_ratings'].iloc[j]
                    devData[2][j] += 1
            else:   # if multiple developers
                for k in range(len(devData[0][j])): # looping through the multiple dev list of the selected game
                    if devData[0][j][k] in data['developer'].iloc[i]:
                        devData[1][j] += data['percent_ratings'].iloc[j]
                        devData[2][j] += 1
                devData[0][j] = ';'.join(devData[0][j]) # Returning multi dev games to string format for a ';' delimiter
    sleep(2)
    for i in range(len(devData[0])):
        devData[1][i] = devData[1][i] / devData[2][i]

    devNScore = pd.DataFrame(index= devData[0], data= ({'dev_score': devData[1], 'num_games': devData[2]}))
    print('[', ''.join([str(stepCount), '.2 ] |\tFiltering: Games per developer\t\t\t\t\t\t| Number of Unique Developers, pre-filter:']), devNScore['dev_score'].size)

    devNScore.drop(devNScore[devNScore['num_games'] <= numOfGamesThreshold].index, inplace= True)
    print('[', ''.join([str(stepCount), '.2 ] |\t\t\t\t\t\t\t\t\t\t\t\t\t\t| Number of Unique Developers, post-filter:']), devNScore['dev_score'].size)

    devNScore = devNScore.sort_values(by= 'dev_score', ascending= False)
    print('[', ''.join([str(stepCount), '.3 ] |\tDisplaying DataFrame data\t\t\t\t\t\t\t| ']))
    print('-' * 110)
    print(devNScore)
    devNScoreReturn = devNScore

    if devNScore['dev_score'].size > numOnGraph:
        devNScore.drop(devNScore.tail((devNScore['dev_score'].size-numOnGraph)).index, inplace = True)
    devNScore = devNScore.sort_values(by='dev_score', ascending= True)

    print('-' * 110)
    print('[', ''.join([str(stepCount), '.4 ] |\tSaving Graph as \'1developerFigure.png\'\t\t\t\t| ']))

    fig = plt.figure()
    ax  = fig.add_subplot(111)
    ax2 = ax.twiny()
    width = 0.4

    devNScore.dev_score.plot(kind='barh', color='red' , ax=ax , width=width, position=0, label= 'Avg. Game Review Score')
    devNScore.num_games.plot(kind='barh', color='blue', ax=ax2, width=width, position=1, label= 'Number of Games')
    handles1, labels1 = ax.get_legend_handles_labels()
    handles2, labels2 = ax2.get_legend_handles_labels()
    handles1.extend(handles2)
    labels1.extend(labels2)
    ax.set_ylabel('Developers')
    ax.set_xlabel('Avg. Game Review Score [%]')
    ax.set_xticks(range(0, 101, 5))
    ax2.set_xlabel('Number of Games')
    ax2.set_xticks(range(max(devNScore['num_games'])+1))
    plt.title('Average game review scores, by Developer')
    fig.legend(handles1, labels1, loc='center right')
    fig.savefig("1developerFigure.png", dpi= 260, bbox_inches='tight')
    if showGraph == 'y':
        plt.show()
    stepCount += 1

    return devNScoreReturn, numOfGames, stepCount