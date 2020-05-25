# Hackerrank Pattern Mining
# CS 412 HW 1 Spring 2020
# WORKING CODE

import sys
import itertools
import re


def getHackerrankInput():
    input = list()
    for line in sys.stdin.readlines():
        input.append(line.strip())
    return input


def getMinsup(inputData):
    return int(inputData[0])


def getTransactions(inputData):
    return inputData[1:]


def getInput():

    input = ['2', 'B A C E D', 'A C', 'C B D']
    # input = ['2', 'T1 T10 T5 T9', 'T5 T2 T1', 'T1 T10 T9 T2']
    # input = ['2', 'data mining', 'frequent pattern mining', 'mining frequent patterns from the transaction dataset', 'closed and maximal pattern mining']
    return input


def createTransactionsDict(transactions):
    '''

    :param transactions: List of original transactions
    transactions: ['B A C E D', 'A C', 'C B D']
    :return: dictionary of all the transcations with sup, create subsets of them and their support
    transactionDict: {'TID4': ['closed', 'and', 'maximal', 'pattern', 'mining'],
                            'TID1': ['data', 'mining'],
                            'TID3': ['mining', 'frequent', 'patterns', 'from', 'the', 'transaction', 'dataset'],
                            'TID2': ['frequent', 'pattern', 'mining']}
    '''

    transactionsDict = dict()
    for index, items in enumerate(transactions):
        words = items.split()
        transactionsDict['TID'+str(index+1)] = words

    return transactionsDict


def getFrequencyOfEachItem(transactionDict):
    '''
    :param transactionDict: {'TID4': ['closed', 'and', 'maximal', 'pattern', 'mining'],
                            'TID1': ['data', 'mining'],
                            'TID3': ['mining', 'frequent', 'patterns', 'from', 'the', 'transaction', 'dataset'],
                            'TID2': ['frequent', 'pattern', 'mining']}
    :return: dict of frequency of each item
    '''
    item_to_frequency = dict()
    for words in transactionDict.values():
        for word in words:
            if word not in item_to_frequency:
                item_to_frequency[word] = 1
            else:
                item_to_frequency[word] += 1

    return item_to_frequency


def findsubsets(s, n):
    return [list(i) for i in itertools.combinations(s, n)]


def createFrequentOneItemDict(minsup, item_to_frequencyDict):

    one_itemset = dict()
    one_itemset[1] = dict()
    for item in item_to_frequencyDict:
        if item_to_frequencyDict[item] >= minsup:
            one_itemset[1][item] = item_to_frequencyDict[item]
    return one_itemset


def sort_nicely(l):
    """ Sort the given list in the way that humans expect. """
    convert = lambda text: int(text) if text.isdigit() else text
    alphanum_key = lambda key: [convert(c) for c in re.split('([0-9]+)', key) ]
    l.sort(key=alphanum_key)
    return l


def sortPatternsInDictionary(k_itemsetDictionary):
    ''' Sort inside the dictionary itself
    :param k_itemsetDictionary:
            {1: {'pattern': 2, 'mining': 4, 'frequent': 2}, 2: {'pattern mining': 2, 'mining frequent': 2}}
    :return: {1: {'pattern': 2, 'mining': 4, 'frequent': 2}, 2: {'mining pattern': 2, 'frequent mining': 2}}
    '''

    # Take k=1 from k_itemsetDictionary
    sorted_k_itemsetDictionary = dict()
    sorted_k_itemsetDictionary[1] = k_itemsetDictionary[1]

    # Sort patterns from k=2 onwards
    for k in range(2,len(k_itemsetDictionary.keys())+1):
        sorted_k_itemsetDictionary[k] = dict()
        for aSubset in k_itemsetDictionary[k].keys():
            aSubsetList = aSubset.split()
            # Natural Sorting
            naturallySortedList = sort_nicely(aSubsetList)
            stitchSubsetString = " ".join(naturallySortedList)
            sorted_k_itemsetDictionary[k][stitchSubsetString] = k_itemsetDictionary[k][aSubset]

    return sorted_k_itemsetDictionary


def formatPatterns(k_itemsetDictionary):

    # Create dictionary from k_itemsetDictionary to minsupToPatternsDictionary
    # in form of {minsup : patterns, minsup : patterns}
    minsupToPatternsDictionary = dict()
    for k, items in k_itemsetDictionary.items():
        for item in items.keys():
            minsupOfItem = k_itemsetDictionary[k][item]
            if minsupOfItem not in minsupToPatternsDictionary:
                minsupToPatternsDictionary[minsupOfItem] = [item]
            else:
                minsupToPatternsDictionary[minsupOfItem].append(item)

    # Sort nicely the patterns for each minsup in minsupToPatternsDictionary
    for k, patterns in minsupToPatternsDictionary.items():
        # Natural Sorting again
        sortedPatterns = sort_nicely(patterns)
        minsupToPatternsDictionary[k] = sortedPatterns

    return minsupToPatternsDictionary


def mineFrequentPatterns(minsup, transactions):
    '''
    :param minsup: int
    :param transactions: list of strings separated by spaces eg: ['B A C E D', 'A C', 'C B D']
    :return:
    '''

    transactionsDict = createTransactionsDict(transactions)
    item_to_frequencyDict = getFrequencyOfEachItem(transactionsDict)
    k_itemsetDictionary = createFrequentOneItemDict(minsup, item_to_frequencyDict)
    allWords = k_itemsetDictionary[1].keys()

    # Make frequent k item dictionaries
    k = 2  # Starting from 2, we have k_itemsetDictionary for k=1 already
    while True:
        subsetOfWords = findsubsets(allWords, k)
        # print "subsetOfWords", subsetOfWords
        if len(subsetOfWords) == 0:
            break
        k_itemsetDictionary[k] = dict()
        for aSubset in subsetOfWords:
            stitchSubsetString = " ".join(aSubset)
            k_itemsetDictionary[k][stitchSubsetString] = 0

        # Find frequency of each subset in the k_itemsetDictionary
        for aSubset in k_itemsetDictionary[k].keys():
            aSubsetList = aSubset.split()
            for words in transactionsDict.values():
                if (set(aSubsetList).issubset(set(words))):
                    k_itemsetDictionary[k][aSubset] += 1

        # Remove infrequent items from k_itemsetDictionary[k]
        deleteInfrequentSubsets = list()
        for aSubset in k_itemsetDictionary[k].keys():
            if k_itemsetDictionary[k][aSubset] < minsup:
                deleteInfrequentSubsets.append(aSubset)
        for aSubset in deleteInfrequentSubsets:
            del k_itemsetDictionary[k][aSubset]

        # Parse dictionary to remove any k that has empty dict
        deleteK = [k for k in k_itemsetDictionary if not k_itemsetDictionary[k]]
        for k in deleteK:
            del k_itemsetDictionary[k]

        k += 1

    # k_itemsetDictionary {1: {'A': 2, 'C': 3, 'B': 2, 'D': 2}, 2: {'A C': 2, 'B D': 2, 'C B': 2, 'C D': 2},
    # 3: {'C B D': 2}}

    # Sort patterns in dictionary itself
    # sorted_k_itemsetDictionary {1: {'A': 2, 'C': 3, 'B': 2, 'D': 2}, 2: {'A C': 2, 'B C': 2, 'C D': 2, 'B D': 2},
    # 3: {'B C D': 2}}
    sorted_k_itemsetDictionary = sortPatternsInDictionary(k_itemsetDictionary)

    # minsupToPatternsDictionary {2: ['A', 'A C', 'B', 'B C', 'B C D', 'B D', 'C D', 'D'], 3: ['C']}
    minsupToPatternsDictionary = formatPatterns(sorted_k_itemsetDictionary)

    printFrequentPatterns(minsupToPatternsDictionary)

    return minsupToPatternsDictionary


def printFrequentPatterns(minsupToPatternsDictionary):

    for k in sorted(minsupToPatternsDictionary, reverse=True):
        for patterns in minsupToPatternsDictionary[k]:
            printString = str(k) + " " + "[" + patterns + "]"
            print (printString)


def getMinsupToListOfPatterns(minsupToPatternsDictionary):
    ''' First make list of list in patterns from minsupToPatternsDictionary
    Like this minsupToListOfPatterns {2: [['A'], ['A', 'C'], ['B'], ['B', 'C'], ['B', 'C', 'D'], ['B', 'D'],
    ['C', 'D'], ['D']], 3: [['C']]} '''

    minsupToListOfPatterns = dict()
    for k, patterns in minsupToPatternsDictionary.items():
        minsupToListOfPatterns[k] = list()
        for pattern in patterns:
            patternList = pattern.split()
            minsupToListOfPatterns[k].append(patternList)
    return minsupToListOfPatterns


def mineClosedPatterns(minsupToPatternsDictionary):
    '''
    :param minsupToPatternsDictionary: {2: ['A', 'A C', 'B', 'B C', 'B C D', 'B D', 'C D', 'D'], 3: ['C']}
    :return:
    '''

    # First make list of list in patterns from minsupToPatternsDictionary
    # Like this minsupToListOfPatterns {2: [['A'], ['A', 'C'], ['B'], ['B', 'C'], ['B', 'C', 'D'], ['B', 'D'],
    # ['C', 'D'], ['D']], 3: [['C']]}
    minsupToListOfPatterns = getMinsupToListOfPatterns(minsupToPatternsDictionary)

    # Mine closed patterns
    # closedPatternsListDict {2: [['A', 'C'], ['B', 'C', 'D']], 3: [['C']]}
    closedPatternsListDict = dict()
    for k, listOfPatterns in sorted(minsupToListOfPatterns.items(), reverse=True):
        closedPatternsListDict[k] = list()
        for index, pattern in enumerate(listOfPatterns):
            subsets = listOfPatterns[:index] + listOfPatterns[index+1:]
            # print "pattern", pattern, "subsets", subsets
            subsetFound = False
            for aSubset in subsets:
                if (set(pattern).issubset(set(aSubset))):
                    subsetFound = True
                    break
            if not subsetFound:
                closedPatternsListDict[k].append(pattern)

    # Parse dictionary to remove any k that has empty dict
    closedPatternsListDict = removeEmptyKeysinDict(closedPatternsListDict)

    # Stitch, join lists, make it string
    # closedPatternsDict {2: ['A C', 'B C D'], 3: ['C']}
    closedPatternsDict = stitchListsinDict(closedPatternsListDict)

    # Print patterns
    printFrequentPatterns(closedPatternsDict)

    return closedPatternsDict


def modifyList(originalList, removableObject):
    modifiedList = list()
    for item in originalList:
        if item != removableObject:
            modifiedList.append(item)

    return modifiedList


def mineMaxPatterns(minsupToPatternsDictionary):

    # First make list of list in patterns from minsupToPatternsDictionary
    # Like this minsupToListOfPatterns {2: [['A'], ['A', 'C'], ['B'], ['B', 'C'], ['B', 'C', 'D'], ['B', 'D'],
    # ['C', 'D'], ['D']], 3: [['C']]}
    minsupToListOfPatterns = getMinsupToListOfPatterns(minsupToPatternsDictionary)

    allPatterns = list()
    for patterns in minsupToListOfPatterns.values():
        for aPattern in patterns:
            allPatterns.append(aPattern)

    maxPatternsListDict = dict()
    for k, patterns in sorted(minsupToListOfPatterns.items(), reverse=True):
        maxPatternsListDict[k] = list()
        for index, pattern in enumerate(patterns):
            subsets = modifyList(originalList=allPatterns, removableObject=pattern)
            subsetFound = False
            for aSubset in subsets:
                if (set(pattern).issubset(set(aSubset))):
                    subsetFound = True
                    break
            if not subsetFound:
                maxPatternsListDict[k].append(pattern)

    # Parse dictionary to remove any k that has empty dict
    maxPatternsListDict = removeEmptyKeysinDict(maxPatternsListDict)

    # Stitch, join lists, make it string
    maxPatternsDict = stitchListsinDict(maxPatternsListDict)

    # Print patterns
    printFrequentPatterns(maxPatternsDict)

    return maxPatternsDict


def removeEmptyKeysinDict(aDict):
    # Parse dictionary to remove any k that has empty dict
    deleteK = [k for k in aDict if not aDict[k]]
    for k in deleteK:
        del aDict[k]
    return aDict


def stitchListsinDict(aDict):
    newDict = dict()
    for k, patterns in sorted(aDict.items(), reverse=True):
        newDict[k] = list()
        for pattern in patterns:
            stitchPattern = " ".join(pattern)
            newDict[k].append(stitchPattern)
    return newDict


if __name__ == '__main__':

    # input = getHackerrankInput()
    input = getInput()

    minsup = getMinsup(inputData=input)
    transactions = getTransactions(inputData=input)

    # Frequent Patterns:
    minsupToPatternsDictionary = mineFrequentPatterns(minsup, transactions)
    print("")
    # Closed Patterns:
    closedPatternsDict = mineClosedPatterns(minsupToPatternsDictionary)
    print("")
    # Max Patterns:
    maxPatternsDict = mineMaxPatterns(minsupToPatternsDictionary)
