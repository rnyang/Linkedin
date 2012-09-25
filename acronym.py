#!/bin/python

import csv

full_names = []
acronyms = []

common_words = ['THE','AND','OF','LLC','INC','CO','SA','CORP','LTD','ASA','&','GROUP','COM','COR','LIMITED']

def readShort():
    with open('Short011.csv', 'rb') as short011:
        shortReader = csv.reader(short011, delimiter=',')
        for row in shortReader:
            full_name = row[2]
            full_names.append(full_name)

    with open('Short012.csv', 'rb') as short012:
        shortReader = csv.reader(short012, delimiter=',')
        for row in shortReader:
            acronym = row[2]
            acronyms.append(acronym)

    myAcronyms = map(toAcronym, full_names)

    acroDict = {}
    unknownAcroDict = {}

    for i in range(len(full_names)):
        try:
            acroDict[myAcronyms[i]].append(full_names[i])
        except:
            acroDict[myAcronyms[i]] = [full_names[i]]

    for acro in acronyms:
        try:
            unknownAcroDict[acro] = acroDict[acro]
        except:
            unknownAcroDict[acro] = ["*** NO MATCH ***"]

    with open('acronymLKND.csv', 'wb') as outfile:
        outWriter = csv.writer(outfile, delimiter=',')
        for acro in unknownAcroDict.keys():
            outstring = [acro] + unknownAcroDict[acro]
            outWriter.writerow(outstring)

def toAcronym(full_name):
    split = full_name.split(' ')
    acronym = ""
    for word in split:
        acronym += word[0]

    """
    TODO

    * Remove common words e.g. 'of', 'the', 'llc'
    * Numbers to Letters (2 -> T)
    * Remove single letters and characters e.g. '&', '2'

    """

    # Initial: Remove all common words

    new_acro = ""
    for word in split:
        if word not in common_words:
            new_acro += word[0]

    print new_acro


    return acronym

def main():
    readShort()
    return 0

main()
