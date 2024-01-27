# -*- coding: utf-8 -*-
"""
by phk
"""

import json
import pandas as pd
import csv

def remove_empty_values(list_of_dictionaries):
    for dictionary in list_of_dictionaries:
        keys_to_remove = [key for key, value in dictionary.items() if value == '' or value == 'pol']
        for key in keys_to_remove:
            del dictionary[key]
    return list_of_dictionaries


def transform_dictionary(old_dictionary):
    new_key = old_dictionary['id']
    new_values = [value for key, value in old_dictionary.items() if key != 'id']
    return {new_key: new_values}


def process_list_of_dictionaries(list_of_dictionaries):
    new_list = {}
    for dictionary in list_of_dictionaries:
        new_dictionary = transform_dictionary(dictionary)
        new_list.update(new_dictionary)
    return new_list

def add_identifiers(x1, x2):
    for key in x2:
        if key in x1:
            identifiers = [element[0] for element in x2[key] if element[0].startswith('b')]
            x1[key].extend(identifiers)
    return x1


def remove_duplicates_preserving_order(lst):
    result = []
    for element in lst:
        if element not in result:
            result.append(element)
    return result

def create_new_dictionary(old_dictionary):
    new_dictionary = {}
    for key, values in old_dictionary.items():
        # Search for identifiers starting with 'b'
        identifiers_b = [value for value in values if isinstance(value, str) and value.startswith('b')]
        for id_b in identifiers_b:
            # Assign to 'b' identifiers the appropriate keywords without duplicates
            new_values = remove_duplicates_preserving_order([value for value in values if not value.startswith('b')])
            new_dictionary[id_b] = new_values
    return new_dictionary

#GET AND PREPARE DATA
'''

Based on files from:
- https://github.com/CHC-Computations/Powiazane-metadane-Biblioteki-Nauki-i-Biblioteki-Narodowej and
- https://docs.google.com/spreadsheets/d/1-MYkyJfW5u1T4Cv-ofiLDx140FvAFbjVHq3Qo-7UwV4/edit?usp=sharing

'''

#Library of Science and National Library of Poland mapping

with open("/content/drive/MyDrive/Granty, współpraca naukowa/POIR/elb faseta clarin kwds/Linked_metadata_of_the_Science_ Library_and_the_ National_Library_part1.json", 'r') as file:
    dict1 = json.load(file)
with open("/content/drive/MyDrive/Granty, współpraca naukowa/POIR/elb faseta clarin kwds/Linked_metadata_of_the_Science_ Library_and_the_ National_Library_part2.json", 'r') as file:
    dict2 = json.load(file)

bib_nau_bn_mapping = {**dict1, **dict2}


#IDs of bibliographic records from Library of Science with automatic keywords from Clarin

with open("/content/drive/MyDrive/Granty, współpraca naukowa/POIR/elb faseta clarin kwds/clarin_keywords_bibliotekanauki - clarin_keywords_bibliotekanauki.csv", mode='r', encoding='utf-8') as file:
    csv_reader = csv.DictReader(file)
    clarin_kwds = [row for row in csv_reader]

clarin_kwds = remove_empty_values(clarin_kwds)
clarin_kwds = process_list_of_dictionaries(clarin_kwds)
clarin_kwds_connected = add_identifiers(clarin_kwds, bib_nau_bn_mapping)
clarin_kwds_final = create_new_dictionary(clarin_kwds_connected)

with open("elb_clarin_faseta.json", 'w', encoding='utf-8') as file:
    json.dump(clarin_kwds_final, file, ensure_ascii=False, indent=4)
