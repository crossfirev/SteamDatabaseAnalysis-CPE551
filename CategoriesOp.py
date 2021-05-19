from tqdm import tqdm
import pandas as pd
from time import sleep
import matplotlib.pyplot as plt

pd.options.mode.chained_assignment = None

def categoriesOp(data, numOfGames, stepCount, numOfGamesThreshold, numOnGraph, showGraph):
    # Extracting unique category names
    uniqueCats = data['categories'].unique()

    # Checks for multiple categories and splits, for future operation
    for i in range(len(uniqueCats)):
        if ";" in uniqueCats[i]: #uniqueCats[i].find(';') != -1:
            uniqueCats[i] = uniqueCats[i].split(';')

    # catData is a 2D list, [0] 1st column is the name of a category (it is a list of unique categories)   [type: str/list (depending on cat count)]
    #                       [1] 2nd column is the categories score                                           [type: float]
    #                       [2] 3rd column is the number of games they have in this dataset sample          [type: int]
    catData = [uniqueCats, [0]*len(uniqueCats), [0]*len(uniqueCats)]

    print('[ ', stepCount, ' ] |\tAverage game review scores, by Category Combination', '|')
    tqdmDesc = ''.join(['[ ', str(stepCount), '.1 ] |\tProcessing Category Statistics...', '\t\t\t\t\t|'])
    sleep(2)
    for i in tqdm(range(numOfGames), desc= tqdmDesc): # Selects a game sample; also runs a progress bar
        for j in range(len(catData[0])): # Iterates through the unique cat list, compares to the selected game's cat, then adds the score to that cat's score
            if type(catData[0][j]) == str: # Checking if single categories
                if catData[0][j] in data['categories'].iloc[i]:
                    catData[1][j] += data['percent_ratings'].iloc[j]
                    catData[2][j] += 1
            else:   # if multiple categories
                for k in range(len(catData[0][j])): # looping through the multiple cat list of the selected game
                    if catData[0][j][k] in data['categories'].iloc[i]:
                        catData[1][j] += data['percent_ratings'].iloc[j]
                        catData[2][j] += 1
                catData[0][j] = ';'.join(catData[0][j]) # Returning multi cat games to string format for a ';' delimiter
    sleep(2)
    for i in range(len(catData[0])):
        catData[1][i] = catData[1][i] / catData[2][i]

    catNScore = pd.DataFrame(index= catData[0], data= ({'cat_score': catData[1], 'num_games': catData[2]}))
    catNScore2 = pd.DataFrame(index= range(len(catData[0])), data= ({'unclean_cat_names': catData[0], 'cat_score': catData[1], 'num_games': catData[2]}))

    print('[', ''.join([str(stepCount), '.2 ] |\tFiltering: Games per categories\t\t\t\t\t\t| Number of Unique Categories, pre-filter:']), catNScore['cat_score'].size)

    catNScore.drop(catNScore[catNScore['num_games'] <= numOfGamesThreshold*30].index, inplace= True)
    catNScore2.drop(catNScore2[catNScore2['num_games'] <= numOfGamesThreshold*30].index, inplace= True)
    print('[', ''.join([str(stepCount), '.2 ] |\t\t\t\t\t\t\t\t\t\t\t\t\t\t| Number of Unique Categories, post-filter:']), catNScore['cat_score'].size)

    catNScore = catNScore.sort_values(by= 'cat_score', ascending= False)
    print('[', ''.join([str(stepCount), '.3 ] |\tDisplaying DataFrame data\t\t\t\t\t\t\t| ']))
    print('-' * 110)
    print(catNScore)
    catNScoreReturn = catNScore

    if catNScore['cat_score'].size > numOnGraph:
        catNScore.drop(catNScore.tail((catNScore['cat_score'].size-numOnGraph)).index, inplace = True)
    catNScore = catNScore.sort_values(by='cat_score', ascending= True)

    print('-' * 110)
    print('[', ''.join([str(stepCount), '.4 ] |\tSaving Graph as \'3categories1Figure.png\'\t\t\t| ']))
    print('#'*110)

    fig = plt.figure()
    ax  = fig.add_subplot(111)
    ax2 = ax.twiny()
    width = 0.4

    catNScore.cat_score.plot(kind='barh', color='red' , ax=ax , width=width, position=0, label= 'Avg. Game Review Score')
    catNScore.num_games.plot(kind='barh', color='blue', ax=ax2, width=width, position=1, label= 'Number of Games')
    handles1, labels1 = ax.get_legend_handles_labels()
    handles2, labels2 = ax2.get_legend_handles_labels()
    handles1.extend(handles2)
    labels1.extend(labels2)
    ax.set_ylabel('Categories')
    ax.set_xlabel('Avg. Game Review Score [%]')
    ax.set_xticks(range(0, 101, 5))
    ax2.set_xlabel('Number of Games')
    ax2.set_xticks(range(0, max(catNScore['num_games'])+1, int((max(catNScore['num_games'])+1)/15)))
    plt.title('Average game review scores, by Category Combinations')
    fig.legend(handles1, labels1, loc='center right')
    fig.savefig("3categories1Figure.png", dpi= 260, bbox_inches='tight')
    if showGraph == 'y':
        plt.show()
    stepCount += 1

    for i in range(catNScore2['unclean_cat_names'].size):
        if ';' in catNScore2['unclean_cat_names'].iloc[i]:
            catNScore2['unclean_cat_names'].iloc[i] = catNScore2['unclean_cat_names'].iloc[i].split(';')
    uniqueCatNames = []
    for i in range(catNScore2['unclean_cat_names'].size):
        if type(catNScore2['unclean_cat_names'].iloc[i]) == list:
            for j in range(len(catNScore2['unclean_cat_names'].iloc[i])):
                if catNScore2['unclean_cat_names'].iloc[i][j] not in uniqueCatNames:
                    uniqueCatNames.append(catNScore2['unclean_cat_names'].iloc[i][j])
        elif type(catNScore2['unclean_cat_names'].iloc[i]) == str:
            if catNScore2['unclean_cat_names'].iloc[i] not in uniqueCatNames:
                uniqueCatNames.append(catNScore2['unclean_cat_names'].iloc[i])
        else:
            print("NOT SUPPOSE TO GET HERE!")

    catData2 = [uniqueCatNames, [0] * len(uniqueCatNames), [0] * len(uniqueCatNames)]

    print('[ ', stepCount, ' ] |\tAverage game review scores, by Category', '\t\t\t|')
    tqdmDesc = ''.join(['[ ', str(stepCount), '.1 ] |\tProcessing Category Statistics...', '\t\t\t\t\t|'])
    sleep(2)
    for i in tqdm(range(numOfGames), desc= tqdmDesc): # Selects a game sample; also runs a progress bar
        for j in range(len(catData2[0])): # Iterates through the unique cat list, compares to the selected game's cat, then adds the score to that cat's score
            if catData2[0][j] in data['categories'].iloc[i]:
                catData2[1][j] += data['percent_ratings'].iloc[j]
                catData2[2][j] += 1
    sleep(2)
    for i in range(len(catData2[0])):
        catData2[1][i] = catData2[1][i] / catData2[2][i]

    catNScore2Final = pd.DataFrame(index= catData2[0], data= ({'cat_score': catData2[1], 'num_games': catData2[2]}))

    print('[', ''.join([str(stepCount), '.2 ] |\tFiltering: Games per categories\t\t\t\t\t\t| Number of Unique Categories, pre-filter:']),catNScore2Final['cat_score'].size)
    catNScore2Final.drop(catNScore2Final[catNScore2Final['num_games'] <= numOfGamesThreshold*30].index, inplace=True)
    print('[', ''.join([str(stepCount), '.2 ] |\t\t\t\t\t\t\t\t\t\t\t\t\t\t| Number of Unique Categories, post-filter:']),catNScore2Final['cat_score'].size)

    catNScore2Final = catNScore2Final.sort_values(by= 'cat_score', ascending= False)
    print('[', ''.join([str(stepCount), '.3 ] |\tDisplaying DataFrame data\t\t\t\t\t\t\t| ']))
    print('-' * 110)
    print(catNScore2Final)
    catNScoreReturn2 = catNScore2Final

    catNScore2Final = catNScore2Final.sort_values(by='cat_score', ascending=True)

    print('-' * 110)
    print('[', ''.join([str(stepCount), '.4 ] |\tSaving Graph as \'4categories2Figure.png\'\t\t\t| ']))

    fig = plt.figure()
    ax  = fig.add_subplot(111)
    ax2 = ax.twiny()
    width = 0.4

    catNScore2Final.cat_score.plot(kind='barh', color='red' , ax=ax , width=width, position=0, label= 'Avg. Game Review Score')
    catNScore2Final.num_games.plot(kind='barh', color='blue', ax=ax2, width=width, position=1, label= 'Number of Games')
    handles1, labels1 = ax.get_legend_handles_labels()
    handles2, labels2 = ax2.get_legend_handles_labels()
    handles1.extend(handles2)
    labels1.extend(labels2)
    ax.set_ylabel('Categories')
    ax.set_xlabel('Avg. Game Review Score [%]')
    ax.set_xticks(range(0, 101, 5))
    ax2.set_xlabel('Number of Games')
    ax2.set_xticks(range(0, max(catNScore2Final['num_games'])+1, int((max(catNScore2Final['num_games'])+1)/15)))
    plt.title('Average game review scores, by Category')
    fig.legend(handles1, labels1, loc='center right')
    fig.savefig("4categories2Figure.png", dpi= 260, bbox_inches='tight')
    if showGraph == 'y':
        plt.show()

    stepCount += 1

    return catNScoreReturn, catNScoreReturn2, numOfGames, stepCount