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

def publisherOp(data, numOfGames, stepCount, numOfGamesThreshold, numOnGraph, showGraph):
    # Extracting unique publisher names
    uniquePubs = data['publisher'].unique()

    # Checks for multiple publishers and splits, for future operation
    for i in range(len(uniquePubs)):
        if ";" in uniquePubs[i]: #uniquePubs[i].find(';') != -1:
            uniquePubs[i] = uniquePubs[i].split(';')

    # pubData is a 2D list, [0] 1st column is the name of a publisher (it is a list of unique publishers)   [type: str/list (depending on pub count)]
    #                       [1] 2nd column is the publisher score                                           [type: float]
    #                       [2] 3rd column is the number of games they have in this dataset sample          [type: int]
    pubData = [uniquePubs, [0]*len(uniquePubs), [0]*len(uniquePubs)]

    print('[ ', stepCount, ' ] |\tAverage game review scores, by Publisher', '\t\t\t|')
    tqdmDesc = ''.join(['[ ', str(stepCount), '.1 ] |\tProcessing Publisher Statistics...', '\t\t\t\t\t|'])
    sleep(2)
    for i in tqdm(range(numOfGames), desc= tqdmDesc): # Selects a game sample; also runs a progress bar
        for j in range(len(pubData[0])): # Iterates through the unique pub list, compares to the selected game's pub, then adds the score to that pub's score
            if type(pubData[0][j]) == str: # Checking if single publisher
                if pubData[0][j] in data['publisher'].iloc[i]:
                    pubData[1][j] += data['percent_ratings'].iloc[j]
                    pubData[2][j] += 1
            else:   # if multiple publishers
                for k in range(len(pubData[0][j])): # looping through the multiple pub list of the selected game
                    if pubData[0][j][k] in data['publisher'].iloc[i]:
                        pubData[1][j] += data['percent_ratings'].iloc[j]
                        pubData[2][j] += 1
                pubData[0][j] = ';'.join(pubData[0][j]) # Returning multi pub games to string format for a ';' delimiter
    sleep(2)
    for i in range(len(pubData[0])):
        pubData[1][i] = pubData[1][i] / pubData[2][i]

    pubNScore = pd.DataFrame(index= pubData[0], data= ({'pub_score': pubData[1], 'num_games': pubData[2]}))
    print('[', ''.join([str(stepCount), '.2 ] |\tFiltering: Games per publisher\t\t\t\t\t\t| Number of Unique Publishers, pre-filter:']), pubNScore['pub_score'].size)

    pubNScore.drop(pubNScore[pubNScore['num_games'] <= numOfGamesThreshold].index, inplace= True)
    print('[', ''.join([str(stepCount), '.2 ] |\t\t\t\t\t\t\t\t\t\t\t\t\t\t| Number of Unique Publishers, post-filter:']), pubNScore['pub_score'].size)

    pubNScore = pubNScore.sort_values(by= 'pub_score', ascending= False)
    print('[', ''.join([str(stepCount), '.3 ] |\tDisplaying DataFrame data\t\t\t\t\t\t\t| ']))
    print('-' * 110)
    print(pubNScore)
    pubNScoreReturn = pubNScore

    if pubNScore['pub_score'].size > numOnGraph:
        pubNScore.drop(pubNScore.tail((pubNScore['pub_score'].size-numOnGraph)).index, inplace = True)
    pubNScore = pubNScore.sort_values(by='pub_score', ascending= True)

    print('-' * 110)
    print('[', ''.join([str(stepCount), '.4 ] |\tSaving Graph as \'2publisherFigure.png\'\t\t\t\t| ']))

    fig = plt.figure()
    ax  = fig.add_subplot(111)
    ax2 = ax.twiny()
    width = 0.4

    pubNScore.pub_score.plot(kind='barh', color='red' , ax=ax , width=width, position=0, label= 'Avg. Game Review Score')
    pubNScore.num_games.plot(kind='barh', color='blue', ax=ax2, width=width, position=1, label= 'Number of Games')
    handles1, labels1 = ax.get_legend_handles_labels()
    handles2, labels2 = ax2.get_legend_handles_labels()
    handles1.extend(handles2)
    labels1.extend(labels2)
    ax.set_ylabel('Publishers')
    ax.set_xlabel('Avg. Game Review Score [%]')
    ax.set_xticks(range(0, 101, 5))
    ax2.set_xlabel('Number of Games')
    ax2.set_xticks(range(0, max(pubNScore['num_games'])+1, int((max(pubNScore['num_games'])+1)/15)))
    plt.title('Average game review scores, by Publisher')
    fig.legend(handles1, labels1, loc='center right')
    fig.savefig("2publisherFigure.png", dpi= 260, bbox_inches='tight')
    if showGraph == 'y':
        plt.show()
    stepCount += 1

    return pubNScoreReturn, numOfGames, stepCount