from tqdm import tqdm
import pandas as pd
from time import sleep
import matplotlib.pyplot as plt

pd.options.mode.chained_assignment = None

def genresOp(data, numOfGames, stepCount, numOfGamesThreshold, numOnGraph, showGraph):
    # Extracting unique genre names
    uniqueCats = data['genres'].unique()

    # Checks for multiple genres and splits, for future operation
    for i in range(len(uniqueCats)):
        if ";" in uniqueCats[i]: #uniqueCats[i].find(';') != -1:
            uniqueCats[i] = uniqueCats[i].split(';')

    # genData is a 2D list, [0] 1st column is the name of a genre (it is a list of unique genres)   [type: str/list (depending on gen count)]
    #                       [1] 2nd column is the genres score                                           [type: float]
    #                       [2] 3rd column is the number of games they have in this dataset sample          [type: int]
    genData = [uniqueCats, [0]*len(uniqueCats), [0]*len(uniqueCats)]

    print('[ ', stepCount, ' ] |\tAverage game review scores, by Genre Combination', '\t|')
    tqdmDesc = ''.join(['[ ', str(stepCount), '.1 ] |\tProcessing Genre Statistics...', '\t\t\t\t\t\t|'])
    sleep(2)
    for i in tqdm(range(numOfGames), desc= tqdmDesc): # Selects a game sample; also runs a progress bar
        for j in range(len(genData[0])): # Iterates through the unique gen list, compares to the selected game's gen, then adds the score to that gen's score
            if type(genData[0][j]) == str: # Checking if single genres
                if genData[0][j] in data['genres'].iloc[i]:
                    genData[1][j] += data['percent_ratings'].iloc[j]
                    genData[2][j] += 1
            else:   # if multiple genres
                for k in range(len(genData[0][j])): # looping through the multiple gen list of the selected game
                    if genData[0][j][k] in data['genres'].iloc[i]:
                        genData[1][j] += data['percent_ratings'].iloc[j]
                        genData[2][j] += 1
                genData[0][j] = ';'.join(genData[0][j]) # Returning multi gen games to string format for a ';' delimiter
    sleep(2)
    for i in range(len(genData[0])):
        genData[1][i] = genData[1][i] / genData[2][i]

    genNScore = pd.DataFrame(index= genData[0], data= ({'gen_score': genData[1], 'num_games': genData[2]}))
    genNScore2 = pd.DataFrame(index= range(len(genData[0])), data= ({'unclean_gen_names': genData[0], 'gen_score': genData[1], 'num_games': genData[2]}))

    print('[', ''.join([str(stepCount), '.2 ] |\tFiltering: Games per genres\t\t\t\t\t\t\t| Number of Unique Genres, pre-filter:']), genNScore['gen_score'].size)

    genNScore.drop(genNScore[genNScore['num_games'] <= numOfGamesThreshold*30].index, inplace= True)
    genNScore2.drop(genNScore2[genNScore2['num_games'] <= numOfGamesThreshold*30].index, inplace= True)
    print('[', ''.join([str(stepCount), '.2 ] |\t\t\t\t\t\t\t\t\t\t\t\t\t\t| Number of Unique Genres, post-filter:']), genNScore['gen_score'].size)

    genNScore = genNScore.sort_values(by= 'gen_score', ascending= False)
    print('[', ''.join([str(stepCount), '.3 ] |\tDisplaying DataFrame data\t\t\t\t\t\t\t| ']))
    print('-' * 110)
    print(genNScore)
    genNScoreReturn = genNScore

    if genNScore['gen_score'].size > numOnGraph:
        genNScore.drop(genNScore.tail((genNScore['gen_score'].size-numOnGraph)).index, inplace = True)
    genNScore = genNScore.sort_values(by='gen_score', ascending= True)

    print('-' * 110)
    print('[', ''.join([str(stepCount), '.4 ] |\tSaving Graph as \'5genres1Figure.png\'\t\t\t\t| ']))
    print('#' * 110)

    fig = plt.figure()
    ax  = fig.add_subplot(111)
    ax2 = ax.twiny()
    width = 0.4

    genNScore.gen_score.plot(kind='barh', color='red' , ax=ax , width=width, position=0, label= 'Avg. Game Review Score')
    genNScore.num_games.plot(kind='barh', color='blue', ax=ax2, width=width, position=1, label= 'Number of Games')
    handles1, labels1 = ax.get_legend_handles_labels()
    handles2, labels2 = ax2.get_legend_handles_labels()
    handles1.extend(handles2)
    labels1.extend(labels2)
    ax.set_ylabel('Genres')
    ax.set_xlabel('Avg. Game Review Score [%]')
    ax.set_xticks(range(0, 101, 5))
    ax2.set_xlabel('Number of Games')
    ax2.set_xticks(range(0, max(genNScore['num_games'])+1, int((max(genNScore['num_games'])+1)/15)))
    plt.title('Average game review scores, by Genre Combinations')
    fig.legend(handles1, labels1, loc='center right')
    fig.savefig("5genres1Figure.png", dpi= 260, bbox_inches='tight')
    if showGraph == 'y':
        plt.show()
    stepCount += 1

    for i in range(genNScore2['unclean_gen_names'].size):
        if ';' in genNScore2['unclean_gen_names'].iloc[i]:
            genNScore2['unclean_gen_names'].iloc[i] = genNScore2['unclean_gen_names'].iloc[i].split(';')
    uniqueCatNames = []
    for i in range(genNScore2['unclean_gen_names'].size):
        if type(genNScore2['unclean_gen_names'].iloc[i]) == list:
            for j in range(len(genNScore2['unclean_gen_names'].iloc[i])):
                if genNScore2['unclean_gen_names'].iloc[i][j] not in uniqueCatNames:
                    uniqueCatNames.append(genNScore2['unclean_gen_names'].iloc[i][j])
        elif type(genNScore2['unclean_gen_names'].iloc[i]) == str:
            if genNScore2['unclean_gen_names'].iloc[i] not in uniqueCatNames:
                uniqueCatNames.append(genNScore2['unclean_gen_names'].iloc[i])
        else:
            print("NOT SUPPOSE TO GET HERE!")

    genData2 = [uniqueCatNames, [0] * len(uniqueCatNames), [0] * len(uniqueCatNames)]

    print('[ ', stepCount, ' ] |\tAverage game review scores, by Genre', '\t\t\t\t|')
    tqdmDesc = ''.join(['[ ', str(stepCount), '.1 ] |\tProcessing Genre Statistics...', '\t\t\t\t\t\t|'])
    sleep(2)
    for i in tqdm(range(numOfGames), desc= tqdmDesc): # Selects a game sample; also runs a progress bar
        for j in range(len(genData2[0])): # Iterates through the unique gen list, compares to the selected game's gen, then adds the score to that gen's score
            if genData2[0][j] in data['genres'].iloc[i]:
                genData2[1][j] += data['percent_ratings'].iloc[j]
                genData2[2][j] += 1
    sleep(2)
    for i in range(len(genData2[0])):
        genData2[1][i] = genData2[1][i] / genData2[2][i]

    genNScore2Final = pd.DataFrame(index= genData2[0], data= ({'gen_score': genData2[1], 'num_games': genData2[2]}))
    print('[', ''.join([str(stepCount), '.2 ] |\tFiltering: Games per genres\t\t\t\t\t\t\t| Number of Unique Genres, pre-filter:']),genNScore2Final['gen_score'].size)
    genNScore2Final.drop(genNScore2Final[genNScore2Final['num_games'] <= numOfGamesThreshold*30].index, inplace=True)
    print('[', ''.join([str(stepCount), '.2 ] |\t\t\t\t\t\t\t\t\t\t\t\t\t\t| Number of Unique Genres, post-filter:']),genNScore2Final['gen_score'].size)

    genNScore2Final = genNScore2Final.sort_values(by= 'gen_score', ascending= False)
    print('[', ''.join([str(stepCount), '.3 ] |\tDisplaying DataFrame data\t\t\t\t\t\t\t| ']))
    print('-' * 110)
    print(genNScore2Final)
    genNScoreReturn2 = genNScore2Final

    genNScore2Final = genNScore2Final.sort_values(by='gen_score', ascending=True)

    print('-' * 110)
    print('[', ''.join([str(stepCount), '.4 ] |\tSaving Graph as \'6genres2Figure.png\'\t\t\t\t| ']))

    fig = plt.figure()
    ax  = fig.add_subplot(111)
    ax2 = ax.twiny()
    width = 0.4

    genNScore2Final.gen_score.plot(kind='barh', color='red' , ax=ax , width=width, position=0, label= 'Avg. Game Review Score')
    genNScore2Final.num_games.plot(kind='barh', color='blue', ax=ax2, width=width, position=1, label= 'Number of Games')
    handles1, labels1 = ax.get_legend_handles_labels()
    handles2, labels2 = ax2.get_legend_handles_labels()
    handles1.extend(handles2)
    labels1.extend(labels2)
    ax.set_ylabel('Genres')
    ax.set_xlabel('Avg. Game Review Score [%]')
    ax.set_xticks(range(0, 101, 5))
    ax2.set_xlabel('Number of Games')
    ax2.set_xticks(range(0, max(genNScore2Final['num_games'])+1, int((max(genNScore2Final['num_games'])+1)/15)))
    plt.title('Average game review scores, by Genre')
    fig.legend(handles1, labels1, loc='center right')
    fig.savefig("6genres2Figure.png", dpi= 260, bbox_inches='tight')
    if showGraph == 'y':
        plt.show()

    stepCount += 1

    return genNScoreReturn, genNScoreReturn2, numOfGames, stepCount