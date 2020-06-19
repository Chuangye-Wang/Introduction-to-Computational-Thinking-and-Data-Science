###########################
# 6.0002 Problem Set 1a: Space Cows 
# Name:
# Collaborators:
# Time:

from ps1_partition import get_partitions
import time
import pandas as pd
import csv

#================================
# Part A: Transporting Space Cows
#================================

# Problem 1
def load_cows(filename):
    """
    Read the contents of the given file.  Assumes the file contents contain
    data in the form of comma-separated cow name, weight pairs, and return a
    dictionary containing cow names as keys and corresponding weights as values.

    Parameters:
    filename - the name of the data file as a string

    Returns:
    a dictionary of cow name (string), weight (int) pairs
    """
    # TODO: Your code here
    pass
    f = open(filename)
    data = f.readlines()
    f.close()
    reader = csv.reader(data)
    a = {}
    for row in reader:
        a[row[0]] = int(row[1])
    
    return a
# Problem 2
def greedy_cow_transport(cows,limit=10):
    """
    Uses a greedy heuristic to determine an allocation of cows that attempts to
    minimize the number of spaceship trips needed to transport all the cows. The
    returned allocation of cows may or may not be optimal.
    The greedy heuristic should follow the following method:

    1. As long as the current trip can fit another cow, add the largest cow that will fit
        to the trip
    2. Once the trip is full, begin a new trip to transport the remaining cows

    Does not mutate the given dictionary of cows.

    Parameters:
    cows - a dictionary of name (string), weight (int) pairs
    limit - weight limit of the spaceship (an int)
    
    Returns:
    A list of lists, with each inner list containing the names of cows
    transported on a particular trip and the overall list containing all the
    trips
    """
    # TODO: Your code here
    start_time = time.time()
    
    cowscopy = sorted(cows.items(), key = lambda cows: cows[1], reverse = True)
    trips = [] # total list of all trips
    trip = [] # the names of cows transported in one trip
    tws = 0.0 # total weight
    records = []
    while(len(records) < len(cows)):
        for item in cowscopy:
            if (item not in records) and (tws + item[1]) <= limit:
                tws += item[1]
                trip.append(item[0])
                records.append(item)
        trips.append(trip)
        trip = []
        tws = 0.0
    
    print('executed time = ', time.time() - start_time)
    
    return trips
        
# Problem 3
def brute_force_cow_transport(cows,limit=10):
    """
    Finds the allocation of cows that minimizes the number of spaceship trips
    via brute force.  The brute force algorithm should follow the following method:

    1. Enumerate all possible ways that the cows can be divided into separate trips 
        Use the given get_partitions function in ps1_partition.py to help you!
    2. Select the allocation that minimizes the number of trips without making any trip
        that does not obey the weight limitation
            
    Does not mutate the given dictionary of cows.

    Parameters:
    cows - a dictionary of name (string), weight (int) pairs
    limit - weight limit of the spaceship (an int)
    
    Returns:
    A list of lists, with each inner list containing the names of cows
    transported on a particular trip and the overall list containing all the
    trips
    """
    # TODO: Your code here
    start_time = time.time()
    # use get_partitions to generate all the possible combinations of cows
    cowsa = get_partitions(cows) 
    summ = 0.0
    count = 0
    tripslen = []
    trips = []
    for row in cowsa:
        for trip in row:
            for i in trip:
                summ += cows[i]
            if summ <= limit:
                summ = 0.0
                continue
            else:
                count = 1
                break
        if count == 0:
            trips.append(row)
            tripslen.append(len(row))
        summ = 0.0
        count = 0
    minpos = tripslen.index(min(tripslen))
    finaltrips = trips[minpos]
    print('executed time = ', time.time() - start_time)
    
    return finaltrips

        
# Problem 4
def compare_cow_transport_algorithms():
    """
    Using the data from ps1_cow_data.txt and the specified weight limit, run your
    greedy_cow_transport and brute_force_cow_transport functions here. Use the
    default weight limits of 10 for both greedy_cow_transport and
    brute_force_cow_transport.
    
    Print out the number of trips returned by each method, and how long each
    method takes to run in seconds.

    Returns:
    Does not return anything.
    """
    # TODO: Your code here
    
    filename = 'ps1_cow_data.txt'
    cowsa = load_cows(filename)
    start_time = time.time()
    trips_by_greedy = greedy_cow_transport(cowsa)
    timeforgreedy = time.time() - start_time

    start_time = time.time()
    trips_by_brute = brute_force_cow_transport(cowsa)
    timeforbrute = time.time() - start_time

    print('1. trips searched by Greedy alogorithm is ', trips_by_greedy, '\n cost time = ', timeforgreedy)
    print('2. trips searched by Greedy alogorithm is ', trips_by_brute, '\n cost time = ', timeforbrute)
    

#%%
compare_cow_transport_algorithms()
    
    