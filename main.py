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


## Import statements
import pandas as pd
pd.set_option("display.max_rows", 8, "display.max_columns", 18)
pd.options.mode.chained_assignment = None

# Importing self-made code
import DataFilterAndClean as dFC
import DeveloperOp  as dOp
import PublisherOp  as pOp
import CategoriesOp as cOp
import GenresOp as gOp

## Function Definitions
def ownerBracketSwitch(x):
    return {
        'a': ('0-20000', '20,000'),
        'b': ('20000-50000', '50,000'),
        'c': ('50000-100000', '100,000'),
        'd': ('100000-200000', '200,000'),
        'e': ('200000-500000', '500,000'),
        'f': ('500000-1000000', '1,000,000'),
        'g': ('1000000-2000000', '2,000,000'),
        'h': ('2000000-5000000', '5,000,000'),
        'i': ('5000000-10000000', '10,000,000'),
        'j': ('10000000-20000000', '20,000,000'),
        'k': ('20000000-50000000', '50,000,000'),
        'l': ('50000000-100000000', '100,000,000'),
        'm': ('100000000-200000000', '200,000,000'),
    }[x]
def isValidInt(inputStr, range1, range2, warning):
    while True:
        input1 = int(input(inputStr))
        if input1 <= range1 or input1 > range2:
            print('[ ERR ] |\tInput: out of range\t\t\t\t|', warning)
            continue
        else:
            break
    return input1

def isValidFloat(inputStr, range1, range2, warning):
    while True:
        input1 = float(input(inputStr))
        if input1 <= range1 or input1 > range2:
            print('[ ERR ] |\tInput: out of range\t\t\t\t|', warning)
            continue
        else:
            break
    return input1

def isValidStr(inputStr, warning):
    while True:
        input1 = input(inputStr)
        if input1 in ['y', 'n']:
            break
        else:
            print('[ ERR ] |\tInput: out of range\t\t\t\t|', warning)
            continue

    return input1

def isValidOwner(inputStr, warning):
    while True:
        input1 = input(inputStr)
        if input1 in ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm']:
            break
        else:
            print('[ ERR ] |\tInput: out of range\t\t\t\t|', warning)
            continue
    return input1

print('#'*110)
print('CPE 551 - Final Project')
print('\t\t\t Title:\tSteam Dataset Analysis')
print('\t\t\tAuthor:\tMatthew Lepis')
print(' Date of Last Edit:\t5/19/2021')
print(' ')
print('Dataset Used: Steam Store Games (Clean dataset)')
print('            : Includes game database information gathered from May 2019')
print('            : https://www.kaggle.com/nikdavis/steam-store-games?select=steam.csv')
print(' ')


stepCount = 1                                   # Program Progress Step Counter

## Reading in dataset data; "steam.csv"
data = pd.read_csv('steam.csv')
print('#'*110)
print('[ ', stepCount, ' ] |\tRead in the dataset', '\t\t\t\t\t\t\t\t| Dataset Sample Count:', data['developer'].size,''.join(['\n','#'*110]))
print('#'*110)
stepCount += 1

###### USER INPUT #######################################################################################################################################################
reviewCountThreshold = isValidInt('Total number of reviews deemed acceptable?\n\tChoose between: (0, 3046717]\n', 0, 3046717, 'Valid inputs include: [type: int], 0 < x <= 3046717')   # int; number of reviews to filter out, filters out anything less than the number input                                 #
print('Game samples with',reviewCountThreshold, 'or less total reviews will be filtered out.')
print('#'*110)

ownerCountThreshold = ownerBracketSwitch(isValidOwner('Total number of owners deemed acceptable?\n\tChoose between: [a, m]\n\t\ta: 20,000\n\t\tb: 50,000\n\t\tc: 100,000\n\t\td: 200,000\n\t\te: 500,000\n\t\tf: 1,000,000\n\t\tg: 2,000,000\n\t\th: 5,000,000\n\t\ti: 10,000,000\n\t\tj: 20,000,000\n\t\tk: 50,000,000\n\t\tl: 100,000,000\n\t\tm: 200,000,000\n', 'Valid inputs include: [type: str], \'a\' through \'m\''))   # tuple; char a through m passed through 'ownerBracketSwitch()' to get the bracket of owners for the filter threshold   #
print('Game samples with',ownerCountThreshold[1], 'or less owners will be filtered out.')
print('#'*110)

sampleSizeFrac = isValidFloat('What fraction of the cleaned dataset shall be used?:\n\tValid inputs include: [type: float], 0.0 < x <= 1.0\n', 0.0, 1.0, 'Valid inputs include: [type: float], 0.0 < x <= 1.0')                              # float between 0 and 1; fractional size of the sample taken from the whole dataset                                     #
if sampleSizeFrac == 1:
    print(sampleSizeFrac * 100, '% of the current dataset will be utilized.')
else:
    print('Only', sampleSizeFrac*100, '% of the current dataset will be utilized.')
print('#'*110)

randomSample = isValidInt('Random or not?:\n\tValid inputs include: [type: int], -1 < x <= 100, -1 for random, anything else for static.\n', -2, 100, 'Valid inputs include: [type: int], -1 < x <= 100, -1 for random, anything else for static')                                # any pos int or -1; randomizes the sample choice, -1 makes it random, pos int sets the random state constant.          #
if sampleSizeFrac != 1:
    if randomSample != -1:
        print('Random seed:',randomSample, 'was chosen.')
    else:
        print('Randomness ensues...')
print('#'*110)

numOfGamesThreshold = isValidInt('Number of games per grouping allowed:\n\tChoose between: (0, 100]\n', 0, 100, 'Valid inputs include: [type: int], 0 < x <= 100')
print('#'*110)

numOnGraph = isValidInt('Number of grouping to show on endpoint graphs:\n\tChoose between: (0, 100]\n', 0, 100, 'Valid inputs include: [type: int], 0 < x <= 100')
print('#'*110)

showGraph = isValidStr('Show graphs?\n\tChoose \'y\' or \'n\'.\n', 'Valid inputs include: [type: str], \'y\' or \'n\'')
print('#'*110)
print('#'*110)
#########################################################################################################################################################################



### CALLING dataFilterAndClean from DataFilterAndClean.py [dFC]
# tuple; returns a cleaned 'data', the number of games (samples) within the cleaned 'data', and the program progress counter: stepCount


cleaned = dFC.dataFilterAndClean(data, reviewCountThreshold, ownerCountThreshold, sampleSizeFrac, randomSample, stepCount)

### CALLING developerOp from DeveloperOp.py [dOp]
#
devOpOutput = dOp.developerOp(cleaned[0], cleaned[1], cleaned[2], numOfGamesThreshold, numOnGraph, showGraph)
devOpDF = devOpOutput[0]
print('#'*110)
print('#'*110)

pubOpOutput = pOp.publisherOp(cleaned[0], devOpOutput[1], devOpOutput[2], numOfGamesThreshold, numOnGraph, showGraph)
pubOpDF = pubOpOutput[0]
print('#'*110)
print('#'*110)

catOpOutput = cOp.categoriesOp(cleaned[0], pubOpOutput[1], pubOpOutput[2], numOfGamesThreshold, numOnGraph, showGraph)
catOpDF = catOpOutput[0]
print('#'*110)
print('#'*110)

genOpOutput = gOp.genresOp(cleaned[0], catOpOutput[2], catOpOutput[3], numOfGamesThreshold, numOnGraph, showGraph)
genOpDF = genOpOutput[0]
print('#'*110)
print('#'*110)