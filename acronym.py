#!/bin/python

"""
* LINKEDIN ANALYSIS PROJECT
* Runnan Yang
*
* University of Chicago 2012
"""

import csv
import time

full_names = []
acronyms = []

fn_sizeDict = {}
ac_sizeDict = {}

common_words = ['THE','AND','OF','LLC','INC','CO','SA','CORP','LTD','ASA','&','GROUP','COM','COR','LIMITED','COMPANY',]
business_names = ['COMPANY','CORPORATION','ENTERPRISE','GROUP','INTERNATIONAL','INSTITUTE','INCORPORATED']
business_abbrev = ['AB','AD','AG','AS','A/S','ASA','CO.','CO','CORP','INC.','INC','INST','INST.','LIMITED','LLC','LLP','LTD.','NV','OY','OYJ','PLC','S.A.','SA','S/A','SAS']
sector_names = ['BANK','BUSINESS','COMMUNICATIONS','COMPUTER','CONSULTING','ENTERTAINMENT','EXPRESS','GRAPHICS','INSURANCE','INTERNATIONAL','INVESTMENTS','INSTRUMENTS','NETWORKS','SERVICES','SYSTEMS','TECHNOLOGIES','TECHNOLOGY','TECH.','TECH','TELECOM','UNIVERSITY','UNIV.', 'WIRELESS']
gvmt = ['DEPARTMENT','DEPT', 'MINISTRY']
conj_prep = ['AND','OF']

all_common_words = common_words + business_abbrev + business_names + sector_names + gvmt

# Checks if A is contained in B
def equalUpTo(a, b):
    if len(a) > len(b):
        return False
    for char_pos in xrange(min([len(a), len(b)])):
        if a[char_pos] != b[char_pos]:
            return False
    return True

def readShort():

    # Load the files into full_name and acronyms

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

    # Get one-word companies (e.g. Deloitte -> Deloite X)
    # one_word_names = []
    # for full_name in full_names:
    #     if len(full_name.split()) == 1 and full_name not in all_common_words:
    #         one_word_names.append(full_name)

    # Get the acronym for each full name (Simple Case)

    myAcronyms = map(toAcronym, full_names)

    # Acronym : [Full Name]
    acroDict = {}
    unknownAcroDict = {}

    # For each synthetic acronym, add the corresponding  full company name to the dictionary entry
    for i in range(len(full_names)):
        try:
            acroDict[myAcronyms[i]].append(full_names[i])
        except:
            acroDict[myAcronyms[i]] = [full_names[i]]

    # Collect the acronyms with and without full name matches
    for acro in acronyms:
        try:
            unknownAcroDict[acro] = acroDict[acro]
        except:
            unknownAcroDict[acro] = ["*** NO MATCH ***"]

    # Write to acronymLKND.csv
    with open('acronymLKND.csv', 'wb') as outfile:
        outWriter = csv.writer(outfile, delimiter=',')
        for acro in unknownAcroDict.keys():
            outstring = [acro] + unknownAcroDict[acro]
            outWriter.writerow(outstring)

# Transforms full company name to potential acronym

def toAcronym(full_name):

    out = []

    # Add the first letter of each word, space-seperated
    split = full_name.split(' ')
    acronym = ""
    for word in split:
        acronym += word[0]

    new_acro = ""
    for word in split:
        if word not in common_words:
            new_acro += word[0]

    out.append(acronym)
    out.append(new_acro)

    return acronym

def readShortMulti():
    with open('Short011.csv', 'rb') as short011:
        # Read Names
        shortReader = csv.reader(short011, delimiter=',')
        for row in shortReader:
            full_name = row[2]
            full_names.append(full_name)

    with open('Short011.csv', 'rb') as short011:
        # Build Size Dict
        shortReader = csv.reader(short011, delimiter=',')
        for row in shortReader:
            fn_sizeDict[row[2]] = row[1]

    with open('Short012.csv', 'rb') as short012:
        # Read Names
        shortReader = csv.reader(short012, delimiter=',')
        for row in shortReader:
            acronym = row[2]
            acronyms.append(acronym)

    with open('Short012.csv', 'rb') as short012:
        # Build Size Dict
        shortReader = csv.reader(short012, delimiter=',')
        for row in shortReader:
            fn_sizeDict[row[2]] = row[1]

    # Get one-word companies (e.g. Deloitte -> Deloite X)
    # one_word_names = []
    # for full_name in full_names:
    #     if len(full_name.split()) == 1 and full_name not in all_common_words:
    #         one_word_names.append(full_name)

    acroDict = {}

    # For each full name, generate the corresponding acronyms
    for fn in full_names:

        # If the first name belongs to a one-word-name company
        # assign that company's acronym

        # if fn.split()[0] in one_word_names:
        #     fl = fn.split()[0][0]
        #     try:
        #         if fn not in acroDict[fl]:
        #             acroDict[fl].append(fn)
        #     except:
        #         acroDict[fl] = [fn]

        acros = toAcronymMulti(fn)

        for acro in acros:
            # If the generated acronym is used, add it to the dictionary

            subacros = [acro[:x+1] for x in xrange(len(acro))]

            for subac in subacros:
                for acro in acronyms:
                    if subac in acro: # Too Slow (will yield FCC <- Federal Commun, IIT <- Illinois Insti Of)
                    #if subac == acro:
                        try:
                            if fn not in acroDict[acro]:
                                acroDict[acro].append(fn)
                        except:
                            acroDict[acro] = [fn]

    unknownAcroDict = {}

    # For each acronym that we want to find the full name for
    # Try finding its corresponding entry in our dictionary
    for acro in acronyms:
        found = 0

        for key in acroDict.keys():
            if equalUpTo(key, acro): # Allow for partial match 
            # if key == acro:
                found = 1
                try:
                    unknownAcroDict[acro] += acroDict[key]
                except:
                    unknownAcroDict[acro] = acroDict[key]
        if not found:
            unknownAcroDict[acro] = ["*** NO MATCH ***"]
        

    with open('acronymLKND_long.csv', 'wb') as outfile:
        outWriter = csv.writer(outfile, delimiter=',')
        for acro in unknownAcroDict.keys():

            fns = []

            # Filter by company references if large list
            if len(unknownAcroDict[acro]) > 10:

                # Take top 10 by freq
                freqs = [int(fn_sizeDict[x]) for x in unknownAcroDict[acro]]
                tenth = freqs[-9]
                fns = [x for x in unknownAcroDict[acro] if int(fn_sizeDict[x]) > tenth]

                # Freq at least 200
                # fns = [x for x in unknownAcroDict[acro] if fn_sizeDict[x] > 200]

            else:
                fns = unknownAcroDict[acro]

            outstring = [acro] + fns
            outWriter.writerow(outstring)

def toAcronymMulti(full_name):

    out = []
    split = full_name.split(' ')

    # Basic Acronym - First letter of all words (space delimited)
    acronym = ""
    for word in split:
        acronym += word[0]

    out.append(acronym)

    # Acronym with all common words removed

    to_remove = common_words + business_abbrev + business_names + sector_names + gvmt

    new_acro = ""
    for word in split:
        if word not in to_remove:
            new_acro += word[0]

    out.append(new_acro)


    return [acronym, new_acro]

def main():
    #readShort()
    readShortMulti()
    return 0

main()