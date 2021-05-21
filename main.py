import schedTest.UNIFRAMEWORK as uni
import schedTest.OurAnalysis as our

import taskCreation.tgPath as create

import numpy as np
import os
import sys
import random
import itertools
from itertools import repeat
from multiprocessing import Pool

import plot  # plot results


random.seed(331)  # set seed to have same task sets for each plot


def store_results(results, path, filename):
    file = os.path.join(path, filename)
    if not os.path.exists(path):
        os.makedirs(path)
    np.save(file, results)


def load_results(path, filename):
    file = os.path.join(path, filename)
    results = np.load(file, allow_pickle=True)
    return results


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


def test_scheme(gScheme, tasksets_difutil, multiproc=0):
    '''Test a scheme for all tasksets in tasksets_difutil'''
    print('Scheme:', gScheme)
    results = []
    for tasksets in tasksets_difutil:  # tasksets are aggregated like this
        acceptance = []
        if multiproc == 0:  # without multiprocessing
            for taskset in tasksets:
                acceptance.append(_test_scheme(gScheme, taskset))
        else:  # with multiprocessing
            with Pool(multiproc) as p:
                acceptance = p.starmap(
                    _test_scheme, zip(repeat(gScheme), tasksets))
        results.append(sum(acceptance)/len(tasksets))

    return results


def _test_scheme(gScheme, taskset):
    # Find correct scheme
    if gScheme == 'Our - all 0':
        # make arrival curve
        arr_curves = [our.arr_sporadic(task['period']) for task in taskset]
        # do sched test
        return our.sched_test(taskset, arr_curves, choose_xvec=1)
    elif gScheme == 'Our - 3 vec':
        # make arrival curve
        arr_curves = [our.arr_sporadic(task['period']) for task in taskset]
        # do sched test
        return our.sched_test(taskset, arr_curves, choose_xvec=5)
    elif gScheme == 'Uniframework - all 0':
        return uni.UniFramework_all0(taskset)
    elif gScheme == 'Uniframework - 3 vec':
        return uni.UniFramework(taskset)
    elif gScheme == 'Our D1.0':
        # make arrival curve
        arr_curves = [our.arr_sporadic(task['period']) for task in taskset]
        # do sched test
        return our.sched_test(taskset, arr_curves, choose_xvec=4)
    elif gScheme == 'Our D1.1':
        # make arrival curve
        arr_curves = [our.arr_sporadic(task['period']) for task in taskset]
        # set deadlines
        _set_deadlines(taskset, 1.1)
        # do sched test
        return our.sched_test(taskset, arr_curves, choose_xvec=4)
    elif gScheme == 'Our D1.2':
        # make arrival curve
        arr_curves = [our.arr_sporadic(task['period']) for task in taskset]
        # set deadlines
        _set_deadlines(taskset, 1.2)
        # do sched test
        return our.sched_test(taskset, arr_curves, choose_xvec=4)
    elif gScheme == 'Our D1.3':
        # make arrival curve
        arr_curves = [our.arr_sporadic(task['period']) for task in taskset]
        # set deadlines
        _set_deadlines(taskset, 1.3)
        # do sched test
        return our.sched_test(taskset, arr_curves, choose_xvec=4)
    elif gScheme == 'Our D1.4':
        # make arrival curve
        arr_curves = [our.arr_sporadic(task['period']) for task in taskset]
        # set deadlines
        _set_deadlines(taskset, 1.4)
        # do sched test
        return our.sched_test(taskset, arr_curves, choose_xvec=4)
    elif gScheme == 'Our D1.5':
        # make arrival curve
        arr_curves = [our.arr_sporadic(task['period']) for task in taskset]
        # set deadlines
        _set_deadlines(taskset, 1.5)
        # do sched test
        return our.sched_test(taskset, arr_curves, choose_xvec=4)
    elif gScheme == 'Our all 0':  # ------------------------
        # make arrival curve
        arr_curves = [our.arr_sporadic(task['period']) for task in taskset]
        # set deadlines
        _set_deadlines(taskset, 1.3)
        # do sched test
        return our.sched_test(taskset, arr_curves, choose_xvec=1)
    elif gScheme == 'Our all 1':
        # make arrival curve
        arr_curves = [our.arr_sporadic(task['period']) for task in taskset]
        # set deadlines
        _set_deadlines(taskset, 1.3)
        # do sched test
        return our.sched_test(taskset, arr_curves, choose_xvec=2)
    elif gScheme == 'Our heu 1':
        # make arrival curve
        arr_curves = [our.arr_sporadic(task['period']) for task in taskset]
        # set deadlines
        _set_deadlines(taskset, 1.3)
        # do sched test
        return our.sched_test(taskset, arr_curves, choose_xvec=3)
    elif gScheme == 'Our heu 2':
        # make arrival curve
        arr_curves = [our.arr_sporadic(task['period']) for task in taskset]
        # set deadlines
        _set_deadlines(taskset, 1.3)
        # do sched test
        return our.sched_test(taskset, arr_curves, choose_xvec=4)
    elif gScheme == 'Our exhaust':
        # make arrival curve
        arr_curves = [our.arr_sporadic(task['period']) for task in taskset]
        # set deadlines
        _set_deadlines(taskset, 1.3)
        # do sched test
        return our.sched_test(taskset, arr_curves, choose_xvec=0)
    # ==Show that Heuristic is useful==
    elif gScheme in ['All 1 H', 'All 1 L']:
        # make arrival curve
        arr_curves = [our.arr_sporadic(task['period']) for task in taskset]
        # do sched test
        return our.sched_test(taskset, arr_curves, choose_xvec=2)
    elif gScheme in ['All 0 H', 'All 0 L']:
        # make arrival curve
        arr_curves = [our.arr_sporadic(task['period']) for task in taskset]
        # do sched test
        return our.sched_test(taskset, arr_curves, choose_xvec=1)
    elif gScheme in ['Heuristic Lin H', 'Heuristic Lin L']:
        # make arrival curve
        arr_curves = [our.arr_sporadic(task['period']) for task in taskset]
        # do sched test
        return our.sched_test(taskset, arr_curves, choose_xvec=4)
    elif gScheme == ['Exhaust H', 'Exhaust L']:
        # make arrival curve
        arr_curves = [our.arr_sporadic(task['period']) for task in taskset]
        # do sched test
        return our.sched_test(taskset, arr_curves, choose_xvec=0)
    # Tasks with release jitter
    elif gScheme == 'SOTA J10':
        tasksetJ = _make_jitter_tasks(taskset, 0.1)
        return uni.UniFramework(tasksetJ)
    elif gScheme == 'SOTA J20':
        tasksetJ = _make_jitter_tasks(taskset, 0.2)
        return uni.UniFramework(tasksetJ)
    elif gScheme == 'Our J10':
        arr_curves = [our.arr_jit(tsk['period'], 0.1) for tsk in taskset]
        tasksetJ = _make_jitter_tasks(taskset, 0.1)
        return our.sched_test(tasksetJ, arr_curves, choose_xvec=4)
    elif gScheme == 'Our J20':
        tasksetJ = _make_jitter_tasks(taskset, 0.2)
        arr_curves = [our.arr_jit(tsk['period'], 0.2) for tsk in taskset]
        return our.sched_test(tasksetJ, arr_curves, choose_xvec=4)
    # ==logarithmic arrival curve==
    elif gScheme == 'SOTA log':
        return uni.UniFramework(taskset)
    elif gScheme == 'Our J10':
        arr_curves = [our.arr_log(tsk['period']) for tsk in taskset]
        return our.sched_test(taskset, arr_curves, choose_xvec=4)
    else:
        return False


def _set_deadlines(taskset, param):
    for tsk in taskset:
        tsk['deadline'] = tsk['period'] * param


def _make_jitter_tasks(taskset, jit):
    tasksetJ = [dict(tsk) for tsk in taskset]
    for tsk in tasksetJ:
        tsk['period'] *= (1-jit)
        tsk['deadline'] *= (1-jit)
    return tasksetJ


if __name__ == '__main__':

    # Input check
    if len(sys.argv) == 1:
        print('Please provide additional arguments.')
        print('1st:  0:sched test + plot, 1: plot only')
        print('2nd:  argument to choose schedulability test')
        quit()

    # Settings
    gTotBucket = 10  # total number of task sets per utilization
    gTasksinBkt = 10  # tasks per set

    gUStart = 0  # utilization start
    gUEnd = 100  # utilization end
    gUStep = 5  # utilization step

    # Share from period - wcet for self-suspension:
    gMaxsstype = 0.5  # maximal total self-suspension length
    gMinsstype = 0.0  # minimal total self-suspension length

    gSSofftypes = 0  # number of segments does not matter

    deadline_stretch = 1

    Ncol = 3  # number of columns in Legend
    datapath = 'data'
    plotpath = 'plot'
    plotname = ' '  # name for plots, to be changed when choosing schedulability tests

    # Choose schedulability tests
    scheme_flag = sys.argv[2]

    if scheme_flag == '0':
        # comparison all 0.
        gSchemes = ['Our - all 0', 'Uniframework - all 0']
        plotname = '0_comparison'
    elif scheme_flag == '1':
        # comparison 3 vectors from old paper.
        gSchemes = ['Our - 3 vec', 'Uniframework - 3 vec']
        plotname = '1_comparison'
    elif scheme_flag == '2':
        # increase deadline.
        gSchemes = ['Our D1.0', 'Our D1.1', 'Our D1.2',
                    'Our D1.3', 'Our D1.4', 'Our D1.5']
        plotname = '2_our_increase_dl'
    elif scheme_flag == '3':
        # comparison different vectors.
        # Deadline = 1.3 period
        gSchemes = ['Our all 0', 'Our all 1', 'Our heu 1',
                    'Our heu 2', 'Our exhaust']
        plotname = '3_our_comp_vectors'
    # ==Show that Heuristic is useful==
    # 10 tasks per set
    # Deadline = 1.3 period
    elif scheme_flag == '10':
        # high suspension
        gSchemes = ['All 0 H', 'All 1 H', 'Heuristic Lin H', 'Exhaust H']
        plotname = '10_heuristic_useful'
        gTasksinBkt = 3
        deadline_stretch = 1.3
        gMaxsstype = 0.4  # maximal total self-suspension length
        gMinsstype = 0.2  # minimal total self-suspension length
    elif scheme_flag == '11':
        # low suspension
        gSchemes = ['All 0 L', 'All 1 L', 'Heuristic Lin L', 'Exhaust L']
        plotname = '11_heuristic_useful'
        gTasksinBkt = 3
        deadline_stretch = 1.3
        gMaxsstype = 0.2  # maximal total self-suspension length
        gMinsstype = 0.0  # minimal total self-suspension length
    # ==Benefit with DL increase==
    elif scheme_flag == '12':
        gSchemes = ['Our D1.0', 'Our D1.1', 'Our D1.2',
                    'Our D1.3', 'Our D1.4', 'Our D1.5']
        plotname = '12_deadline_increase'
    # ==Tasks with release jitter==
    elif scheme_flag == '13':
        gSchemes = ['SOTA J10', 'Our J10', 'SOTA J20', 'Our J20']
        plotname = '13_release_jitter'
    # ==logarithmic arrival curve==
    elif scheme_flag == '14':
        gSchemes = ['SOTA log', 'Our log']
        plotname = '14_log'
    else:
        print('second input argument not valid')
        quit()

    # Create task sets
    if sys.argv[1] == '0':
        tasksets_difutil = create_tasksets(
            gUStart, gUEnd, gUStep, gTasksinBkt, gTotBucket, gMinsstype, gMaxsstype)

    # Deadline stretch
    if deadline_stretch != 1:
        for tsksets in tasksets_difutil:
            for tskset in tsksets:
                for tsk in tskset:
                    tsk['deadline'] = tsk['period'] * deadline_stretch

    # Schedulability test + store results
    if sys.argv[1] == '0':
        for gScheme in gSchemes:
            # test
            results = list(zip(itertools.count(start=gUStart, step=gUStep),
                               test_scheme(gScheme, tasksets_difutil, multiproc=10)))
            print(list(results))
            # store results
            store_results(results, datapath, gScheme + '.npy')

    # plot results
    if sys.argv[1] in ['0', '1']:
        results_plot = [load_results(datapath, gScheme + '.npy')
                        for gScheme in gSchemes]

        plot.plot(gSchemes, results_plot, plotpath, plotname, Ncol)
