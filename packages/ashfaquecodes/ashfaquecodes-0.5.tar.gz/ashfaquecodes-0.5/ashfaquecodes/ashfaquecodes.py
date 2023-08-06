'''
    Author : Ashfaque Alam
    Date : June 22, 2022
    Colors the printed outputs
'''
from collections import OrderedDict
import re
import colorama
from colorama import Fore
from colorama import Style

colorama.init()

def blue_print_start():
    print(Style.RESET_ALL)
    print(Fore.BLUE + Style.BRIGHT)


def red_print_start():
    print(Style.RESET_ALL)
    print(Fore.RED + Style.BRIGHT)


def green_print_start():
    print(Style.RESET_ALL)
    print(Fore.GREEN + Style.BRIGHT)


def color_print_reset():
    print(Style.RESET_ALL)


#################
##### USAGE #####
#################

# import pprint
# pp = pprint.PrettyPrinter(indent=4)
# red_print_start()
# pp.pprint("--------------------------")
# color_print_reset()

### or, ###

# import pprint
# print(f'{Style.RESET_ALL} {Fore.LIGHTMAGENTA_EX}')
# print(">>>>>>>>><<<<<<<<")
# pp = pprint.PrettyPrinter(indent=4)
# pp.pprint(VARIABLE_NAME)
# print(f'{Style.RESET_ALL}')

'''
    ENDS
'''



'''
    Author : Ashfaque Alam
    Date : July 17, 2022
    Pass a list of non-unique elements in this function and get a unique list returned.
'''
def unique_list(non_unique_list : list) -> list:
    import time

    start_time = time.time()
    # unique_lst = sorted(set(non_unique_list))    # ? This approach is a few mili-secs faster than: `list(set(non_unique_list))`
    unique_lst = list(set(non_unique_list))    # ? This approach is a few mili-secs slower than: `sorted(set(non_unique_list))`
    end_time = time.time()
    # print("Time taken to sort the list -----> ", end_time - start_time)

    return unique_lst
'''
    ENDS
'''



'''
    Author : Ashfaque Alam
    Date : October 1, 2022
    Pass a list of duplicate dictionaries in this function and get a unique list of dictionaries returned.
'''
def unique_list_of_dicts(non_unique_list_of_dicts : list) -> list:
    import time
    start_time = time.time()

    unique_lst_of_dicts = [dict(sub) for sub in set(frozenset(dct.items()) for dct in non_unique_list_of_dicts)]
    # unique_lst_of_dicts = list(map(dict, set(tuple(sorted(sub.items())) for sub in non_unique_list_of_dicts)))

    end_time = time.time()
    # print("Time taken -----> ", end_time - start_time)

    return unique_lst_of_dicts
'''
    ENDS
'''



'''
    Author : Ashfaque Alam
    Date : October 1, 2022
    Pass a list of empty and non-empty dictionaries in this function and get a list of non-empty dictionaries returned.
'''
def remove_empty_dicts_from_list(list_with_empty_dicts : list) -> list:
    import time
    start_time = time.time()

    list_with_no_empty_dicts = list(filter(None, list_with_empty_dicts))    # ? Fastest - 0.2ms for 300 items in list
    # list_with_no_empty_dicts = [item for item in list_with_empty_dicts if item]    # ? Second Fastest - 0.3ms for 300 items in list

    # for item in list_with_no_empty_dicts.copy():    # ? Slowest amongst the methods written above - 1.5ms for 300 items in list
    #     if item == {}: list_with_no_empty_dicts.remove(item)

    end_time = time.time()
    # print("Time taken -----> ", end_time - start_time)

    return list_with_no_empty_dicts
'''
    ENDS
'''



'''
    Author : Ashfaque Alam
    Date : October 1, 2022
    Pass a list of non-empty dictionaries in this function and get a sorted list of dictionaries returned according to your desired sorting key of the dict.
'''
def sort_list_of_dicts(unsorted_list : list, key : str, desc : bool = False) -> list:
    import time
    start_time = time.time()

    if desc:
        from operator import itemgetter
        sorted_list = sorted(unsorted_list, key=itemgetter(key), reverse=True)    # ? Sorting list of dicts in descending order according to the values of `key`.
    else:
        sorted_list = sorted(unsorted_list, key=lambda d: d[key])    # ? Sorting list of dicts in ascending order according to the values of `key`.

    end_time = time.time()
    # print("Time taken to sort the list -----> ", end_time - start_time)

    return sorted_list

#################
##### USAGE #####
#################

# from ashfaquecodes.ashfaquecodes import sort_list_of_dicts
# sort_list_of_dicts(unsorted_list = unsorted_lst, key = 'dict_key_name', desc = True)

'''
    ENDS
'''



'''
    Author : Ashfaque Alam
    Date : July 17, 2022
    Calculate execution time of your code and you can assign it in a variable and can also send it in json response.
'''
def get_execution_start_time() -> float:
    import time
    execution_start_time = time.perf_counter()
    return execution_start_time    # * Current time, BEFORE execution of our code.

def get_execution_end_time(execution_start_time : float, print_time : bool = False) -> str:
    import time
    # * Calculating execution time of our API and it's also sent in the API Response.
    execution_end_time = time.perf_counter()    # * Current time, AFTER execution of our code.
    total_execution_time = (execution_end_time - execution_start_time) * 1000
    if 1000 <= total_execution_time < 60000:    # * i.e., seconds
        total_execution_time /= 1000    # * Converting it in seconds.
        total_execution_time_str = str(round(total_execution_time, 2)) + " secs"    # * Converting it into string for API Response.
        if print_time:
            print('\n ##### Execution Time: {:.4f} secs ##### \n'.format(total_execution_time))
    elif total_execution_time >= 60000:    # * i.e., minutes
        total_execution_time /= 60000    # * Converting it in minutes.
        total_execution_time_mins_str = int(total_execution_time)    # * Extracting the decimal part (whole number)
        total_execution_time_secs_str = round((float('0' + str(total_execution_time - int(total_execution_time))[1:]) * 60), 2)    # * Converting fraction mins to secs
        total_execution_time_str = str(total_execution_time_mins_str) + " mins " + str(total_execution_time_secs_str) + " secs"    # * Converting it into string for API Response.
        if print_time:
            print('\n ##### Execution Time: {:.4f} mins ##### \n'.format(total_execution_time))
    else:    # * i.e., milliseconds
        if print_time:
            print('\n ##### Execution Time: {:.2f} ms ##### \n'.format(total_execution_time))
        total_execution_time_str = str(round(total_execution_time, 2)) + " ms"

    return total_execution_time_str


#################
##### USAGE #####
#################

# from ashfaquecodes.ashfaquecodes import (
#     execution_start_time
#     , total_execution_time_str
# )
# execution_start_time = get_execution_start_time()
# total_execution_time_str = get_execution_end_time(execution_start_time, print_time = True)

'''
    ENDS
'''



'''
    Author : Ashfaque Alam
    Date : April 19, 2022
    Custom Decorator to calculate execution time of a function.
'''
from functools import wraps
import time
import pprint
# pp = pprint.PrettyPrinter(indent=4)
# pp.pprint(dict)
"""helper function to estimate view execution time"""
def timer(func):
    @wraps(func)    # used for copying func metadata
    def wrapper(*args, **kwargs):
        start_time = time.perf_counter()    # record start time
        result = func(*args, **kwargs)    # func execution
        end_time = time.perf_counter()    # record start time
        ## total_time = end_time - start_time    # Calculate time taken in secs
        total_time = (end_time - start_time) * 1000    # Calculating time taken in ms

        # output execution time to console
        if 1000 <= total_time < 60000:    # * i.e., seconds
            total_time /= 1000    # * Converting it in seconds.
            red_print_start()
            total_execution_time_str = str(round(total_time, 2)) + " secs"    # * Converting it into string for API Response.
            print('\n ##### Execution Time: {} ##### \n'.format(total_execution_time_str))
            # print('\n ##### Execution Time: {:.4f} secs ##### \n'.format(total_time))
            color_print_reset()

        elif total_time >= 60000:    # * i.e., minutes
            total_time /= 60000    # * Converting it in minutes.
            total_execution_time_mins_str = int(total_time)    # * Extracting the decimal part (whole number)
            total_execution_time_secs_str = round((float('0' + str(total_time - int(total_time))[1:]) * 60), 2)    # * Converting fraction mins to secs
            total_execution_time_str = str(total_execution_time_mins_str) + " mins " + str(total_execution_time_secs_str) + " secs"    # * Converting it into string for API Response.
            red_print_start()
            print('\n ##### Execution Time: {} ##### \n'.format(total_execution_time_str))
            # print('\n ##### Execution Time: {:.4f} mins ##### \n'.format(total_time))
            color_print_reset()

        else:    # * i.e., milliseconds
            total_execution_time_str = str(round(total_time, 2)) + " ms"
            red_print_start()
            print('\n ##### Execution Time: {} ##### \n'.format(total_execution_time_str))
            # print('\n ##### Execution Time: {:.2f} ms ##### \n'.format(total_time))
            color_print_reset()

        # ? DEPRECATED :-
        # if len(str(round(total_time))) >= 4:
        #     total_time /= 1000
        #     red_print_start()
        #     print('\n ##### Function {}{} {} took {:.4f} secs ##### \n'.format(func.__name__, args, kwargs, total_time))    # first item in the args, ie `args[0]` is `self`
        #     color_print_reset()
        # else:
        #     red_print_start()
        #     print('\n ##### Function {}{} {} took {:.2f} ms ##### \n'.format(func.__name__, args, kwargs, total_time))
        #     color_print_reset()

        return result
    return wrapper


#################
##### USAGE #####
#################

# from ashfaquecodes.ashfaquecodes import timer
# @timer
# def your_function(request):
    # pass

'''
    END
'''