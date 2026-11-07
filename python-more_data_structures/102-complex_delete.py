#!/usr/bin/python3
def complex_delete(a_dictionary, value):
    for key in [k for k, v in a_dictionary.items() if v == value]:
        del a_dictionary[key]
    return a_dictionary
