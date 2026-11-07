#!/usr/bin/python3
def weight_average(my_list=[]):
    if not my_list:
        return 0
    return sum(s * w for s, w in my_list) / sum(w for s, w in my_list)
