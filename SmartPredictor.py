# This file contains functions that update hourly demand predictions based on yesterday's demand increase

DAY_ZERO_OLYMPIC_DEMAND_MULTIPLIER = 15



# These demand schedules come from Hau and Jamie's demand model: 
# https://github.com/hauchu1998/C6800_Smart_Cities/blob/main/notebooks/result.txt

SUNDAY_AVG_DEMANDS = [13698, 3777, 2105, 2579, 5811, 2468, 6153, 969, 3322, 1559, 9348, 1742, 5944, 2402, 195, 2151]
MONDAY_AVG_DEMANDS = [21999, 11125, 3576, 3839, 11117, 3645, 10982, 2522, 8665, 3723, 16246, 3511, 9391, 5731, 410, 5241]
TUESDAY_AVG_DEMANDS = [22671, 11854, 4051, 4524, 12508, 4080, 12424, 2792, 9241, 4121, 17618, 3877, 10126, 6267, 430, 5670]
WEDNESDAY_AVG_DEMANDS = [22710, 12411, 4296, 4732, 12835, 4443, 12664, 2857, 9574, 4300, 18658, 4071, 10621, 6438, 454, 5970]
THURSDAY_AVG_DEMANDS = [21878, 11908, 4171, 4599, 12336, 4281, 12451, 2766, 9325, 4011, 18214, 3807, 10208, 6145, 436, 5806]
FRIDAY_AVG_DEMANDS = [21373, 11921, 4444, 4708, 13688, 4322, 12270, 2672, 8970, 4109, 18342, 3986, 10886, 6108, 427, 5747]
SATURDAY_AVG_DEMANDS = [14382, 6229, 3653, 4171, 12335, 4165, 10791, 1729, 5125, 2743, 14446, 2942, 9273, 3886, 278, 3607]

SUNDAY_RG_DEMANDS = [21610, 7779, 3514, 3881, 10970, 4019, 10144, 2592, 10423, 4825, 18916, 4604, 9235, 4327, 473, 7779]
MONDAY_RG_DEMANDS = [20937, 11220, 4317, 5464, 13210, 4845, 11778, 3222, 10665, 5351, 20776, 4769, 10920, 6215, 543, 7633]
TUESDAY_RG_DEMANDS = [21262, 11260, 4514, 4888, 12803, 5250, 11885, 3199, 10683, 5070, 21445, 4814, 11212, 6898, 540, 7545]
WEDNESDAY_RG_DEMANDS = [20537, 11308, 4436, 4973, 12829, 5344, 11846, 3157, 10677, 5145, 21281, 4790, 11228, 6902, 566, 5540]
THURSDAY_RG_DEMANDS = [21307, 11450, 4527, 5052, 12701, 5246, 11939, 3049, 10511, 5012, 21515, 4740, 11368, 6922, 522, 7248]
FRIDAY_RG_DEMANDS = [21514, 10670, 4533, 4640, 12694, 5002, 11984, 2777, 9392, 4103, 18818, 3933, 10616, 6807, 447, 5558]
SATURDAY_RG_DEMANDS = [19715, 5701, 3484, 3790, 12155, 3845, 10899, 1891, 4580, 2616, 13435, 2691, 8878, 5075, 282, 3851]

OLYMPICS_MULTIPLIER = [23, 23, 23, 23, 23, 23, 23, 23, 23, 23, 23, 23, 23, 23, 23, 23]

AVG_DEMAND_DICT = {
    "Sunday": SUNDAY_AVG_DEMANDS,
    "Monday": MONDAY_AVG_DEMANDS,
    "Tuesday": TUESDAY_AVG_DEMANDS,
    "Wednesday": WEDNESDAY_AVG_DEMANDS,
    "Thursday": THURSDAY_AVG_DEMANDS,
    "Friday": FRIDAY_AVG_DEMANDS,
    "Saturday": SATURDAY_AVG_DEMANDS
}

RG_DEMAND_DICT = {
    "Sunday": SUNDAY_RG_DEMANDS,
    "Monday": MONDAY_RG_DEMANDS,
    "Tuesday": TUESDAY_RG_DEMANDS,
    "Wednesday": WEDNESDAY_RG_DEMANDS,
    "Thursday": THURSDAY_RG_DEMANDS,
    "Friday": FRIDAY_RG_DEMANDS,
    "Saturday": SATURDAY_RG_DEMANDS
}


def calculate_olympic_demand_multiplier(predicted_demand : list, real_demand : list, multiplier_list : list):
    """
    calculate_demand_multiplier(predicted_demand, real_demand) calculates the demand multiplier
    for a given day based on the predicted and real demand for that day
    """
    new_multiplier_list = [0] * len(predicted_demand)
    for i in range(len(predicted_demand)):
        new_multiplier_list[i] = (real_demand[i] / predicted_demand[i]) * 0.5 + multiplier_list[i] * 0.5 # weighted average of new multipliers and olympics multipliers
    return new_multiplier_list

def apply_multiplier(reg_demand_list : list, rg_demand_list : list, multiplier_list : list):
    """
    apply_multiplier(demand_list, multiplier) applies a multiplier to the difference in demand between
    rg_demand_list and reg_demand_list if that difference is positive
    """
    updated_demands = [0] * len(rg_demand_list)
    for i in range(len(reg_demand_list)):
        if rg_demand_list[i] - reg_demand_list[i] >= 0:
            updated_demands[i] = reg_demand_list[i] + (rg_demand_list[i] - reg_demand_list[i]) * multiplier_list[i]
        else:
            updated_demands[i] = rg_demand_list[i]
    return updated_demands

def get_demands(day_of_week : str, actual_demands : list):
    """
    get_demands(day_of_week, actual_demands, predicted_demands) returns a list of demands for a given day
    based on the actual demands from the previous day and the predicted demands for the current day
    """
    if actual_demands == [] or len(actual_demands) != 16:
        return apply_multiplier(AVG_DEMAND_DICT[day_of_week], RG_DEMAND_DICT[day_of_week], OLYMPICS_MULTIPLIER)
    mult = calculate_olympic_demand_multiplier(AVG_DEMAND_DICT[day_of_week], actual_demands, OLYMPICS_MULTIPLIER)
    return apply_multiplier(AVG_DEMAND_DICT[day_of_week], RG_DEMAND_DICT[day_of_week], mult)

def get_percentage_increase(day_of_week : str, demands : list):
    """
    get_percentage_increase(day_of_week, actual_demands) returns the percentage increase in demand
    of the given demands list versus typical non-sports demand of the given day of the week
    """
    return (int) ((sum(demands) / sum(AVG_DEMAND_DICT[day_of_week])) * 100)



