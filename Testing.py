# -*- coding: utf-8 -*-
"""
Created on Sat Nov  7 

@authors: Ricardo Contreras, Diego Rivera
"""

import numpy as np

#Pick the top 100 most used pins out of a leaked pin list. Blacklist is optional
def getTop100Pins(pins, blacklist=None):
    if blacklist is not None:
        for i in range(0, blacklist.shape[0]):
            pins = np.delete(pins,np.where(pins==blacklist[i]))
    (unique, counts) = np.unique(pins, return_counts=True)
    _type=np.dtype([('pins',unique.dtype),('counts',counts.dtype)])
    frequencies = np.empty(len(unique),dtype=_type)
    frequencies['pins'] = unique
    frequencies['counts'] = counts
    frequencies = frequencies[np.argsort(-1*frequencies['counts'])]
    top100 = frequencies[:100]
    return top100

def file_read(fname):
        content_array = []
        with open(fname) as f:
                #Content_list is the list that contains the read lines.     
                for line in f:
                        content_array.append(line)
                #print(content_array)
                return content_array;

if __name__ == "__main__": 
    
    pins4digit = np.array(file_read('RockYou-4-digit.txt')) #Dataset 4 digit pins
    pins6digit = np.array(file_read('RockYou-6-digit.txt')) #Dataset 6 digit pins
    ddbl4digit = np.array(file_read('DD-4-digit-2740.txt')) #Data Driven blacklist 4 digits
    iosbl4digit = np.array(file_read('iOS-4-digit.txt'))    #IOS blacklist 4 digits
    iosbl6digit = np.array(file_read('iOS-6-digit.txt'))    #IOS Blacklist 6 digits
    
    #Create random test set of 1000 pins, out of the leaked pin lists
    test_set_4digits = np.random.choice(pins4digit, size=1000)
    test_set_6digits = np.random.choice(pins6digit, size=1000)
    
    #Remove blacklisted pins out of the base leaked pin sets. 
    blpins4digit = pins4digit
    for i in range(0, iosbl4digit.shape[0]):
            blpins4digit = np.delete(blpins4digit,np.where(blpins4digit==iosbl4digit[i]))
    blpins6digit = pins6digit
    for i in range(0, iosbl6digit.shape[0]):
            blpins6digit = np.delete(blpins6digit,np.where(blpins6digit==iosbl6digit[i]))
            
    #Create test sets excluding blacklisted pins. 
    bltest_set_4digits = np.random.choice(blpins4digit, size=1000)
    bltest_set_6digits = np.random.choice(blpins6digit, size=1000)
    
    #Select most common pins to use in the attack. Pins are sorted in descending
    # order by number of occurences in the leaked test set. 
    attack_list4digit = getTop100Pins(pins4digit)
    attack_list6digit = getTop100Pins(pins6digit)

    #This array will tell us how many pins match the one we used for a guess
    test_results_4digit = np.array(np.zeros(1000)) #Number of tests
    test_results_6digit = np.array(np.zeros(1000))
    
    print('------Test 4 Digit pins, no blacklisting')
    for i in range(0, 100):
        value = attack_list4digit['pins'][i]
        #print('Pin: ', value)
        indices = np.where(test_set_4digits == value)
        test_results_4digit[indices] = 1
        unique, counts = np.unique(test_results_4digit, return_counts=True)
        hits = counts[np.where(unique==1)]
        print('Iteration: ', i+1,' Number of hits: ', hits)
    
    print('------Test 6 Digit pins, no blacklisting')
    for i in range(0, 100):
        value = attack_list6digit['pins'][i]
        #print('Pin: ', value)
        indices = np.where(test_set_6digits == value)
        test_results_6digit[indices] = 1
        unique, counts = np.unique(test_results_6digit, return_counts=True)
        hits = counts[np.where(unique==1)]
        print('Iteration: ', i+1,' Number of hits: ', hits)
       
    #Create attack lists of top 100 pins in the leaked dataset, but excluding 
    # Pins in the blacklist. 
    attack_list4digit = getTop100Pins(pins4digit, blacklist=iosbl4digit)
    attack_list6digit = getTop100Pins(pins6digit, blacklist=iosbl6digit)

    #Reset test results
    test_results_4digit = np.array(np.zeros(1000)) #Number of tests
    test_results_6digit = np.array(np.zeros(1000))
    
    print('------Test 4 Digit pins, WITH blacklisting')
    for i in range(0, 100):
        value = attack_list4digit['pins'][i]
        #print('Pin: ', value)
        indices = np.where(bltest_set_4digits == value)
        test_results_4digit[indices] = 1
        unique, counts = np.unique(test_results_4digit, return_counts=True)
        hits = counts[np.where(unique==1)]
        print('Iteration: ', i+1,' Number of hits: ', hits)
    
    print('------Test 6 Digit pins, WITH blacklisting')
    for i in range(0, 100):
        value = attack_list6digit['pins'][i]
        #print('Pin: ', value)
        indices = np.where(bltest_set_6digits == value)
        test_results_6digit[indices] = 1
        unique, counts = np.unique(test_results_6digit, return_counts=True)
        hits = counts[np.where(unique==1)]
        print('Iteration: ', i+1,' Number of hits: ', hits)
        
    
    
    