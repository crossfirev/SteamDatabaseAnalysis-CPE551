def dataFilterAndClean(data, reviewCountThreshold, ownerCountThreshold, sampleSizeFrac, randomSample, stepCount):
    ## Making a total review rating column
    totalRatings = [0]*data['positive_ratings'].size
    for i in range(len(totalRatings)):
        totalRatings[i] = data['positive_ratings'].iloc[i] + data['negative_ratings'].iloc[i]
    data['total_ratings'] = totalRatings

    ## Filtering out the games with less than 'reviewCountThreshold' reviews
    data.drop(data[data['total_ratings'] < reviewCountThreshold].index, inplace= True)
    print('[ ', stepCount, ' ] |\tFiltering: less than', reviewCountThreshold ,'reviews', '\t\t\t\t\t| Dataset Size:', data['developer'].size)
    ## Filtering out the games with less than ownerCountThreshold[1] owners, as it's a lowest bracket and I think they aren't very
    #                   meaningful to the end result. This reduced the dataset from 27,075 game samples to 8,479.
    data.drop(data[data['owners'] == ownerCountThreshold[0]].index, inplace= True)
    print('[ ', stepCount, ' ] |\tFiltering: less than', ownerCountThreshold[1], 'owners', '\t\t\t\t| Dataset Size:', data['developer'].size)

    ## Filtering out non-english data, as I can't read them.
    data.drop(data[data['english'] == '0'].index, inplace= True)
    print('[ ', stepCount, ' ] |\tFiltering: non-english', '\t\t\t\t\t\t\t\t| Dataset Size:', data['developer'].size)

    i = 0
    k = range(data['developer'].size)
    while i in k:
        if not data['developer'].iloc[i].isascii():
            data.drop(data.index[i], inplace=True)
            k = range(data['developer'].size)
        i += 1
    i = 0
    k = range(data['publisher'].size)
    while i in k:
        if not data['publisher'].iloc[i].isascii():
            data.drop(data.index[i], inplace=True)
            k = range(data['publisher'].size)
        i += 1

    ## Sample size to take from the dataset
    if randomSample != -1:
        data = data.sample(frac=sampleSizeFrac, random_state=randomSample)
    else:
        data = data.sample(frac=sampleSizeFrac)
    numOfGames = data['name'].size

    if sampleSizeFrac != 1.0:
        print('[ ', stepCount, ' ] |\tDownsizing dataset by', sampleSizeFrac*100, '%\t\t\t\t\t\t| Dataset Size:', data['developer'].size)

    ## Discarding unused data columns
    data = data.drop(columns=['appid', 'name', 'release_date', 'english', 'platforms', 'required_age', 'steamspy_tags', 'achievements', 'average_playtime', 'median_playtime', 'owners', 'price'])

    ## Making a percentage review rating column
    percentageRatings = [0]*numOfGames
    for i in range(len(percentageRatings)):
        percentageRatings[i] = (data['positive_ratings'].iloc[i] / data['total_ratings'].iloc[i])*100
    data['percent_ratings'] = percentageRatings

    stepCount += 1
    return data, numOfGames, stepCount