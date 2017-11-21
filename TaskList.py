import os
import os.path as osp

from gitviper.colors import *

import gitviper.utilities as utils
from gitviper.settings import settings

tasks = settings.tasks

occurences_dict = {}
spacing = "   "
window_padding = " "

for k in tasks:
    occurences_dict[k] = []

class Occurence:
    def __init__(self, path, filename, linenumber, linecontent):
        self.filename = filename
        self.path = path
        self.linenumber = linenumber
        self.linecontent = linecontent

def fill_dictionary(lookup, file):
    occurences = []
    fullpath = osp.join(file[0], file[1])
    with open(fullpath, 'r') as myFile:
        try:
            for num, line in enumerate(myFile, 1):
                if lookup in line.lower():
                    occurences.append([num, line])
        except UnicodeDecodeError:
            pass

    if len(occurences) > 0:
        for o in occurences:
            occ = Occurence(file[0], file[1], o[0], o[1])
            occurences_dict[task].append(occ)

print(" " + BG_WHITE + BLACK + "  Tasks  " + RESET)
print()

# get files as list
files = utils.get_files()

# fill dictionary
for task in tasks:
    for f in files:
        fill_dictionary(task.value, f)

# create list of dict entries and ignore empty task-entries
occurences_dict_list = []
for key in occurences_dict:
    if len(occurences_dict[key]) == 0:
        continue
    else:
        occurences_dict_list.append((key, occurences_dict[key]))

# sort list by priority
def getKey(item):
    return item[0].priority
occurences_dict_sorted_by_priority = sorted(occurences_dict_list, reverse=True, key=getKey)

# print table
for kv in occurences_dict_sorted_by_priority:
    key = kv[0]
    value = kv[1]
    real_values = []

    for o in value:
        real_value_entry = []
        linecontent = o.linecontent.strip()

        # strip task regardless of capitalization
        idx = linecontent.lower().find(key.value)
        linecontent = "".join(linecontent.split(linecontent[idx:idx+len(key.value)]))

        # strip commenting symbols
        linecontent = "".join(linecontent.split("#"))
        linecontent = "".join(linecontent.split("//"))
        linecontent = linecontent.strip()

        # add to data used for creating table
        real_value_entry.append(window_padding + key.representation)
        real_value_entry.append(linecontent)
        real_value_entry.append(o.filename.rjust(0).strip())
        real_value_entry.append(str(o.linenumber))

        real_values.append(real_value_entry)

    # find max column widths
    max_widths = [0] * 4
    for v in real_values:
        for i in range(len(v)):
            max_widths[i] = max(max_widths[i], len(v[i]))

    # clamp to window width
    s = len(spacing)
    availablespace = int(utils.get_window_size().x) - max_widths[0] - s - max_widths[2] - s - max_widths[3] - s - len(window_padding)
    max_widths[1] = availablespace

    for v in real_values:
        text = key.color + v[0].ljust(max_widths[0]) + spacing + RESET
        text += v[1][:max_widths[1]].ljust(max_widths[1]) + spacing
        text += v[2].ljust(max_widths[2]) + spacing
        text += v[3].rjust(max_widths[3])
        print(text)

    print()
