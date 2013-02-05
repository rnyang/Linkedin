#!/bin/python

"""
* LINKEDIN ANALYSIS PROJECT II
* R Yang
* 
* Goal: Match names from unify100_1.out with names from NorthAmerica_Companies.csv
* 
* University of Chicago 2013
"""

import csv
import time

def readNA():
    
    na = {}
    with open('NorthAmerica_Companies.csv', 'rb') as naFILE:
        naReader = csv.reader(naFILE, delimiter=',')
        for row in naReader:
            #print row[0], row[9]
            na[row[9]] = row[0]
            #na.append(row[9])

    u100 = []
    with open('unify100_1.out', 'rb') as u100FILE:
        uReader = csv.reader(u100FILE, delimiter='\t')
        for row in uReader:
            #u100[row[1]] = row[0]
            u100.append(row[1])

    return [na, u100]

def main():

    myData = readNA()
    na = myData[0]
    u100 = myData[1]

    na_names = na.keys()

    output = []

    count = 0
    for company in u100:
        for name in na_names:
            if name.find(company + " ") == 0:
                #print company, name
                #time.sleep(1)
                count += 1
                #print count

                out_list = [company, name, na[name]]
                output.append(out_list)
    print "count: ", count
    
    print "NA: ", len(na)
    print "u100: ", len(u100)

    with open('na_match.csv', 'wb') as outFILE:
        outwriter = csv.writer(outFILE, delimiter=',')

        for i in output:
            outwriter.writerow(i)

    print output[0]
    print output[1]
    print output[2]

    
main()
