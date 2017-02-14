import csv
import os
import sys

import test_config

import matplotlib.pyplot as plt
import numpy as np

def plot_baselines(count_baseline, type_baseline, target):
    count_data = []
    for (_, sites, targets) in count_baseline:
        count_data += [targets for x in range(sites)]

    sorted_data = np.sort(count_data) / float(max(count_data))
    yvals = np.arange(len(sorted_data)) / float(len(sorted_data))

    plt.plot(sorted_data, '--', label="count-policy")

    type_data = []
    for (_, sites, targets) in type_baseline:
        type_data += [targets for x in range(sites)]

    sorted_data = np.sort(type_data) / float(max(count_data))

    yvals = np.arange(len(sorted_data)) / float(len(sorted_data))
    plt.plot(sorted_data, label="type-policy")

    plt.xlabel('Ratio of indirect Callsites')
    plt.ylabel('Ratio of Calltargets')
    plt.title(target)
    plt.show()

#plt.figure(figsize=[6,6])
#x = np.arange(0,100,0.00001)
#y = x*np.sin(2*pi*x)
#plt.plot(y)
#plt.axis('off')
#plt.gca().set_position([0, 0, 1, 1])
#plt.savefig("test.svg")

def main(argv):
    test_dir = test_config.get_test_dir(argv)

    for test_target in test_config.configure_targets(argv):
        result = test_target.generate_baseline_all()

        for opt in result.keys():
            ((count_baseline, type_baseline), problem_string) = result[opt]
            plot_baselines(count_baseline, type_baseline, test_target.name())
            return

main(sys.argv[1:])