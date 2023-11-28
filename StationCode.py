import math

############
#DECLARE CONSTANTS
############
# 500 people per car
CAR_CAPACITY = 166
# 3 cars per train
CARS_PER_TRAIN = 3
# $2.25 per ride
FARE = 2.25
# $10000 to operate a train
OPERATING_COST = 10000
# minimum 10 trains per hour
MIN_TRAIN_PER_HOUR = 10
# boarding/alight rate, passengers per second. 1.65 meter doors, 9 doors per car
BOARDING_RATE = 0.87 * 1.65 * 9
ALIGHT_RATE = 0.65 * 1.65 * 9
# share of passengers that leave at each pre-stadium station
DEPART_RATE = 0.2


###########
# DECLARE FUNCITONS
###########


def trains_needed(demand : int, car_capacity : int, cars_per_train : int, min_freq : int):
    """
    trains_needed(demand, car_capacity, cars_per_train, min_freq) calculates the minimum 
    number of trains needed on a given time interval t to meet the passenger demand on
    that interval t. For now, t is measured in hours.

    RETURNS: (trains_needed, fill), where [fill] is the fill percentage of [demand] 
        passengers riding [trains_needed] trains
    """
    passengers_per_train = car_capacity * cars_per_train
    trains_needed = math.ceil(demand / passengers_per_train)
    
    # return min_freq if trains_needed < min_freq
    trains_needed = max(trains_needed, min_freq)
    
    # calculate fill percentage
    fill = demand / (trains_needed * car_capacity * cars_per_train)

    return trains_needed, fill

def simulate_train_run(demands : list, depart_rate : float):
    """
    given a list of station demands [d1, d2, d3] and a depart_rate, return the most amount of
    people on the train at once at any point along the run
    """
    # if only one station on the line, return that station's demand
    if len(demands) == 1:
        return demands[0]

    # otherwise, the train starts with the first station's demand and has passengers board/depart at each station
    current_passengers = demands[0]
    max_passengers = current_passengers
    for demand in demands[1:]:
        current_passengers = current_passengers * (1 - depart_rate) + demand
        max_passengers = max(max_passengers, current_passengers)
    return max_passengers

def trains_needed_on_line(demands : list, depart_rate : float, car_capacity : int, cars_per_train : int, min_freq : int):
    """
    trains_needed_line(demands, depart_rate, car_capacity, cars_per_train, min_freq) calculates the minimum 
    number of trains needed on a line at a given time interval to satisfy the passenger demand of all stations.
    along that line This function assumes that the train
    line has [demands] passengers at each station, and that [depart_rate] of passengers
    leave at each station.
    """
    # calculate the number of passengers per train
    passengers_per_train = car_capacity * cars_per_train

    # calculate the most number of people on the line at any given station
    max_line_demand = simulate_train_run(demands, depart_rate)
    
    # calculate trains needed to meet that demand
    return trains_needed(max_line_demand, car_capacity, cars_per_train, min_freq)


def station_time(demands : list, trains : int, boarding_rate : int, alight_rate : int, depart_rate : int):
    """
    station_time(demands, trains, boarding_rate) returns the average time that a train
    must spend in each station on a line on a given time interval t given that [demands] passengers
    arrive at each station during t, [trains] trains arrive during t, and we have a boarding rate of 
    [boarding rate] and an alighting rate of [alighting rate].
    """
    
    # we can calculate the total boarding time by summing the demands at each station, then
    # that number first by the number of trains, then by the boarding rate of each train
    total_boarding_time = sum(demands) / trains / boarding_rate

    # we can calculate the total alighting time by summing the demands at each station, then
    # subtracting the number of passengers remaining at the final station. We then divide this
    # number of alighted passengers first by the number of trains, then by the alighting rate of each train
    total_alighting_time = (sum(demands) - simulate_train_run(demands, depart_rate)) / trains / alight_rate

    # find average time spent per station by a train on the line
    return (total_boarding_time + total_alighting_time) / len(demands)

def process_demands(demands : list):
    """
    given a list of demands of each station along a line, returns the number of trains needed to meet that demand, the fill percentage,
    and the average time each train spent at each station along the line
    """
    # calculate the number of trains needed to meet the demand of the line
    trains, fill = trains_needed_on_line(demands, DEPART_RATE, CAR_CAPACITY, CARS_PER_TRAIN, MIN_TRAIN_PER_HOUR)

    # calculate the average time each train spent at each station
    time = station_time(demands, trains, BOARDING_RATE, ALIGHT_RATE, DEPART_RATE)

    return trains, fill, time

def print_results(demands : list):
    """
    given a list of demands of each station along a line, prints the number of trains needed to meet that demand, the fill percentage,
    and the average time each train spent at each station along the line
    """
    trains, fill, time = process_demands(demands)
    print("\nRESULTS:")
    print('{0:40}  {1}'.format("Number of stations on line:", len(demands)))
    print('{0:40}  {1}'.format("Average demand at each station:", f"{sum(demands) / len(demands):.0f}"))
    print("")
    if trains == MIN_TRAIN_PER_HOUR:
        print('{0:40} {1}'.format("Trains needed to meet interval demand:", f"{trains} (set by minimum frequency)"))
    else:
        print('{0:40}  {1}'.format("Trains needed to meet interval demand:", trains))

    fill_percentage = str(fill * 100)[:5] + "%"
    print('{0:40}  {1}'.format("Fill percentage:", fill_percentage))
    print('{0:40}  {1}'.format("Average boarding time at each station:", f"{time:.2f} seconds"))

###########
# MAIN
###########

# # Read the input list of station demands, space delimited "d1 d2 d3 ... dn"
# demands = []
# while demands == []:
#     input_list = input("Enter the passenger demands at each station on the line as a space-separated list (ex. '400 200 500 300'):\n")
#     demands = input_list.split()

# # Convert the elements to integers
# demands = [int(demand) for demand in demands]

# # Call the print_results function with the demands list
# print_results(demands)

