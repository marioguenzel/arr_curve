import schedTest.UNIFRAMEWORK as uni
import schedTest.OurAnalysis as our

import taskCreation.tgPath as create

import numpy as np
import os
import sys
import random


random.seed(331)  # set seed to have same task sets for each plot


def plot_results():
    '''Plot the results'''
    # TODO
    pass


def create_tasksets(
    UStart,  # start of utilization
    UEnd,  # end of utilization
    UStep,  # utilization step
    TasksinBkt,  # tasks per set
    TotBucket,  # number of task sets per utilization
    Minsstype,  # minimal ratio of self-suspension
    Maxsstype,  # maximal ratio of self-suspension
):
    '''Create tasksets according to description.'''
    tasksets_difutil = []  # task set differentiated by utilization

    for u in range(UStart, UEnd, UStep):
        tasksets = []
        for i in range(0, TotBucket, 1):
            percentageU = u / 100
            # Create task set with predefined parameters.
            tasks = create.taskGeneration_p(
                TasksinBkt, percentageU, Minsstype, Maxsstype, vRatio=1, numLog=int(2))
            # Sort tasks by period.
            sortedTasks = sorted(tasks, key=lambda item: item['period'])
            tasksets.append(sortedTasks)  # add
            for itask in tasks:
                if itask['period'] != itask['deadline']:
                    print('period and deadline are different')
                    breakpoint()
        tasksets_difutil.append(tasksets)  # add

    return tasksets_difutil


if __name__ == '__main__':

    # Input check
    if len(sys.argv) == 1:
        print('Please provide additional arguments.')
        print('1st:  0:sched test + plot, 1: plot only')
        print('2nd:  argument to choose schedulability test')
        quit()

    # Settings
    gTotBucket = 500  # total number of task sets per utilization
    gTasksinBkt = 10  # tasks per set

    gUStart = 0  # utilization start
    gUEnd = 100  # utilization end
    gUStep = 5  # utilization step

    # Share from period - wcet for self-suspension:
    gMaxsstype = 0.5  # maximal total self-suspension length
    gMinsstype = 0.0  # minimal total self-suspension length

    gSSofftypes = 0  # number of segments does not matter

    Ncol = 3  # number of columns in Legend

    # Create task sets
    if sys.argv[1] == '0':
        tasksets_difutil = create_tasksets(
            gUStart, gUEnd, gUStep, gTasksinBkt, gTotBucket, gMinsstype, gMaxsstype)

    pass
