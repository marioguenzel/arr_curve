'''Plot from SSSEvaluation'''

from __future__ import division
import sys
import numpy as np
import matplotlib.pyplot as plt
import random
import math

import os


def pickColor(ischeme):
    color = ''
    if ischeme == 'EL DM':  # --- 1 DM Evaluation.
        color = '#000000'
    elif ischeme == 'UniFramework':
        color = '#0000ff'

    elif ischeme in [  # --- 5 Evaluation.
            'Our D1.0'
    ]:
        color = '#99ff99'
    elif ischeme in [
            'Our D1.1'
    ]:
        color = '#4dff4d'
    elif ischeme in [
            'Our D1.2'
    ]:
        color = '#00e600'
    elif ischeme in [
            'Our D1.3'
    ]:
        color = '#00b300'
    elif ischeme in [
            'Our D1.4'
    ]:
        color = '#006600'
    elif ischeme in [
            'Our D1.5'
    ]:
        color = '#000000'

    elif ischeme in [
            'SOTA J Spor'
    ]:
        color = '#c44dff'

    elif ischeme in [
            'SOTA J CPA'
    ]:
        color = '#339966'

    elif ischeme in [
            'All 0'
    ]:
        color = '#009900'

    elif ischeme in [
            'All 1'
    ]:
        color = '#3366ff'
    elif ischeme in [
            'Heuristic Lin'
    ]:
        color = '#ff9933'
    elif ischeme in [
            'Exhaust'
    ]:
        color = '#ff0000'
    elif ischeme in [
            'Our J', 'Comb 3'
    ]:
        color = '#000000'

    else:  # --- Other: Randomly.
        color = "#%06x" % random.randint(0, 0xFFFFFF)
    return color


def pickMarker(ischeme):  # TODO adjust
    marker = ''
    if ischeme in [
            'EL DM',
            'EL EDF',
            'EL EQDF any lam in [-10,10]',
            'EL SAEDF any lam in [-10,10]',
            'EL-fix DM D1.5', 'EL-var DM D1.5',
            'EL-fix EDF D1.5', 'EL-var EDF D1.5'
    ]:
        marker = 'o'
    elif ischeme in [  # --- 5 Evaluation.
            'Our D1.0',
            'Comb 3'
    ]:
        marker = '>'
    elif ischeme in [
            'Our D1.1',
            'All 0'
    ]:
        marker = '*'
    elif ischeme in [
            'Our D1.2',
            'Exhaust'

    ]:
        marker = 'x'
    elif ischeme in [
            'Our D1.3'
    ]:
        marker = '<'
    elif ischeme in [
            'Our D1.4',
            'All 1'
    ]:
        marker = 'v'
    elif ischeme in [
            'Our D1.5',
            'Heuristic Lin'
    ]:
        marker = 'o'
    else:
        randommarker = ['o', 'v', '^', '<', '>', '1', '2', '3', '4', '8', 's', '|',
                        'p', 'P', '*', '+', 'x', 'X', 'D', 'd']
        # marker = '<'
        marker = random.choice(randommarker)
    return marker


def pickName(ischeme):  # TODO adjust
    name = ''
    if ischeme == 'UniFramework':  # --- 1 DM Evaluation.
        name = 'CNH16'
    elif ischeme == 'SOTA J Spor':
        name = 'SOTA Spor'
    elif ischeme == 'SOTA J CPA':
        name = 'SOTA CPA'
    elif ischeme == 'Our J':
        name = 'Our'
    elif ischeme == 'EL-fixed':
        name = 'EL-fix'
    elif ischeme == 'FP':
        name = 'GUC21'
    else:
        name = ischeme
    return name


def pickLineStyle(ischeme):
    if ischeme in [
            'SuspJit',
            'SuspBlock',
            'Dong and Liu',
            'Liu and Anderson',
            'EL EQDF lam=-1',
            'EL EQDF lam=+1',
            'EL SAEDF lam=-1',
            'EL SAEDF lam=+1',
            'EL-fix DM D1.0', 'EL-var DM D1.0',
            'EL-fix EDF D1.0', 'EL-var EDF D1.0',
            'EL-fix DM D1.2', 'EL-var DM D1.2',
            'EL-fix EDF D1.2', 'EL-var EDF D1.2'
    ]:
        linestyle = '--'
    elif ischeme in [
            'SuspObl',
            'Susp as Comp',
    ]:
        linestyle = ':'
    else:
        linestyle = '-'
    return linestyle


def plot(schemes, results_plot, plotpath, plotname='', Ncol=3):
    """
    prints all plots
    """
    # create figure
    fig = plt.figure()

    # create a virtual outer subsplot for putting big x-ylabel
    ax = fig.add_subplot(111)
    fig.subplots_adjust(top=0.8, left=0.2, right=0.95, bottom=0.2, hspace=0.3)

    ax.set_xlabel('Utilization (%)', size=23)
    ax.set_ylabel('Acceptance Ratio', size=23)
    ax.spines['top'].set_color('black')
    ax.spines['bottom'].set_color('black')
    ax.spines['left'].set_color('black')
    ax.spines['right'].set_color('black')
    ax.tick_params(labelcolor='black', top=False,
                   bottom=False, left=False, right=False, labelsize=20)
    ax.set_yticks([0, 0.25, 0.50, 0.75, 1.0])

    # plot results
    for ischeme, results in zip(schemes, results_plot):
        x, y = zip(*results)

        ax.plot(x, y,
                pickLineStyle(ischeme),
                color=pickColor(ischeme),
                marker=pickMarker(ischeme),
                markersize=8,
                markevery=1,
                fillstyle='none',
                label=pickName(ischeme),
                linewidth=1.8,
                clip_on=False)

    # legend
    ax.legend(
        bbox_to_anchor=(0.42, 1.15),
        loc=10,
        markerscale=1.3,
        ncol=Ncol,
        borderaxespad=0.,
        labelspacing=0.2,  # space between rows
        handlelength=1.8,  # length of the legend line under marker
        handletextpad=0.5,  # space between handle and text
        columnspacing=1.,  # space between columns
        prop={'size': 18})

    ax.grid()

    # ax.set_title('No. of tasks: '+str(numberoftasks)+', Self-suspension length: ' +
    # str(minsstype)+"-"+str(maxsstype), size=10, y=0.99, fontsize=20)

    if not os.path.exists(plotpath):
        os.makedirs(plotpath)
    file = os.path.join(plotpath, plotname + '.pdf')
    fig.savefig(file, bbox_inches='tight')
