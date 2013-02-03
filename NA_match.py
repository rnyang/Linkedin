#!/bin/python

"""
* LINKEDIN ANALYSIS PROJECT II
* R Yang
* 
* University of Chicago 2013
"""

import csv

def readNA():
    
    # Load files

    na = []
    with open('NorthAmerica_Companies.csv', 'rb') as na:
        naReader = csv.reader(na, delimiter=',')
        for row in naReader:
            na.append(row[9])

    u100 = []
    with open('unify100_1.out', 'rb') as u100:
        uReader = csv.reader(u100, delimiter='\t')
        for row in uReader:
            u100.append(row[1])

readNA()
            

