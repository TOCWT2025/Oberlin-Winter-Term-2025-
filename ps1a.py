###########################
# 6.0002 Problem Set 1a: Space Cows 
# Name:
# Collaborators:
# Time:

from ps1_partition import get_partitions
import time

#================================
# Part A: Transporting Space Cows
#================================

# Problem 1
def load_cows(filename):
    file = []
    fixer = str()
    a=open(filename)
    for line in a:
        file.append(a.readline())
    midval = []
    retval = {}
    for line in file:
        midval.append(str.split(line,","))
    for inner in midval:
        retval[inner[0]] = int(inner[1])
    for key in retval:
        fixer = str(retval.get(key))
        retval[key] = (str.removesuffix(fixer,"\n")) #gets rid of the page breaks
    return retval
# Problem 2
def cow_transport_1(cows,limit=10):
    """
    Does one trip!
    """
    highest = ()
    highestval = 0
    retval = []
    legacy = []
    cowval = list(cows.values())
    cow = list(cows.keys())
    while limit>=0:
        for i in range(len(cows)):
            if int(cowval[i]) > highestval and int(cowval[i])<=limit and cow[i] not in legacy:
                highestval = int(cowval[i])
                highest = cow[i]
        if highestval > 0:
            retval.append(highest)
        else:
            return retval
        limit = limit - highestval
        legacy.append(highest)
        highestval = 0
        highest = ()
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
    cowmanip = list(cows)
    fulltrip=[]
    while len(cowmanip)>=1:
        cowdict = {}
        for cow in cowmanip:
            cowdict[cow] = cows[cow]
        trip = cow_transport_1(cowdict,limit=10)
        print(trip)
        for x in trip:
            cowmanip.remove(x)
            print(cowmanip)
        fulltrip.append(trip)
    return fulltrip


# Problem 3
def remove_impossible(cows,limit=10):
    """
    Creates partitions then removes ones that are impossible due to weight limits!
    """
    midlist = []
    hi = list(get_partitions(cows))
    val = 0
    for i in hi:
        for trip in i:
            for j in trip:
                val += int(cows[j])
            if val > limit and i not in midlist:
                midlist.append(i)
            val = 0
    for i in midlist:
        hi.remove(i)
    return(hi)
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
    lowestlength = 1000
    besttrip=[]
    partlist = remove_impossible(cows,limit=10)
    for trip in partlist:
        if len(trip) < lowestlength:
            besttrip = trip
            lowestlength = len(trip)

    return besttrip
cows = load_cows("ps1_cow_data.txt")
print(cows)
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
    start = time.time()
    a = greedy_cow_transport(cows)
    end = time.time()
    print("Took",end - start,"seconds. Number of trips is",len(a))
    print()
    start = time.time()
    b = brute_force_cow_transport(cows)
    end = time.time()
    print("Took",end - start,"seconds. Number of trips is",len(b))
compare_cow_transport_algorithms()
