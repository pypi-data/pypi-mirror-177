"""
Modify dataset

Contents:
    DChemPy.Dataset.YCtoB: Change Continuous label values into Binary values {0, 1}
    DChemPy.Dataset.XCtoB: Change Continuous feature matrix into Binary features {0, 1}
    DChemPy.Dataset.ExtractX: Cut the Feature Matrix by given feature name list
    DChemPy.Dataset.DrawDisY: Draw the distribution of label values by hist plot
"""

import numpy as np
import math
import matplotlib.pyplot as plt
import os
from pathlib import Path


def YCtoB(y, directory=None, notes='01'):
    """
    Turn Continuous label values into Binary values {0, 1}

    :param y: Label Values with type of numpy.array and shape of (num_samples, 1)
    :param directory: Directory to save outputs, default as 'None', for example 'data_out'
    :param notes: Notes in file name, default as '01'

    :return: None

    example:
    DChemPy.Dataset.YCtoB(y, directory='data_out')
    """
    if type(y) is np.ndarray:
        y = y.reshape(y.shape[0], 1)
    elif type(y) is list:
        y = np.array(y).reshape(len(y), 1)
    y_01 = np.zeros((y.shape[0], 1))
    y_mean = np.mean(y)
    for i in range(y.shape[0]):
        if y[i, 0] >= y_mean:
            y_01[i, 0] += 1
    if directory is None:
        np.savetxt('Values' + notes + '_' + str(y_01.shape[0]) + '.csv', y_01, fmt='%s', delimiter=',')
    else:
        if not os.path.exists(directory):
            os.mkdir(directory)
        save_name = Path('', directory, 'Values' + notes + '_' + str(y_01.shape[0]) + '.csv')
        np.savetxt(save_name, y_01, fmt='%s', delimiter=',')


def XCtoB(X, title, divide_pos=[-0.5, -0.15, 0, 0.15, 0.5], directory=None, notes='01'):
    """
    Turn Continuous X into Binary values {0, 1}
    noted: title will be expanded by the set of divide_pos

    :param X: Feature Matrix
    :param title: Title with type of numpy.array and shape of (num_featrues, 1)
    :param divide_pos: List of dividing points of feature values, default as [-0.5, -0.15, 0, 0.15, 0.5]
                       noted: One continuous feature will be divided into len(divide_pos)+1 binary features
    :param directory: Directory to save outputs, default as 'None', for example 'data_out'
    :param notes: Notes in file name, default as '01'

    :return: None

    example:
    DChemPy.Dataset.YCtoB(y, directory='data_out')
    """
    if type(title) is np.ndarray:
        title = title.reshape(title.shape[0], 1)
    elif type(title) is list:
        title = np.array(title).reshape(len(title), 1)
    if directory is None:
        save_name = Path('', 'Interval_Data.txt')
    else:
        if not os.path.exists(directory):
            os.mkdir(directory)
        save_name = Path('', directory, 'Interval_Data.txt')
    inter = []
    f1 = open(save_name, 'w')
    for i in range(X.shape[1]):
        t_min = min(X[:, i])
        t_max = max(X[:, i]) * 1.01
        t_mean = np.mean(X[:, i])
        if 'Wavelength' not in title[i, 0] and 'AbsorbedEnergy' not in title[i, 0]:
            if t_min != 0:
                temp = [round(t_min, max(1, 2 - math.floor(np.log10(abs(t_min)))))]
            else:
                temp = [0.0]
            for j in range(len(divide_pos)):
                if divide_pos[j] < 0:
                    t = t_mean + divide_pos[j] * (t_mean - t_min)
                elif divide_pos[j] > 0:
                    t = t_mean + divide_pos[j] * (t_max - t_mean)
                else:
                    t = t_mean
                if t != 0:
                    temp.append(round(t, max(1, 2 - math.floor(np.log10(abs(t))))))
                else:
                    temp.append(0)
            if t_max != 0:
                temp.append(round(t_max, max(1, 2 - math.floor(np.log10(abs(t_max))))))
            else:
                temp.append(0)
        elif 'Wavelength' in title[i, 0]:
            t1 = math.ceil(t_min / 50)
            t2 = math.floor(t_max / 50)
            temp = np.arange(t1 * 50, t2 * 50, 50).flatten().tolist()
        else:
            temp = []
            for j in range(len(inter[-1])):
                temp.append(
                    round(1239.842 / inter[-1][j], max(1, 2 - math.floor(np.log10(abs(1239.842 / inter[-1][j]))))))
            temp = np.sort(temp)
        inter.append(temp)
        for j in range(len(temp)):
            f1.write(str(temp[j]))
            if j != len(temp) - 1:
                f1.write(',')
        f1.write('\n')
    f1.close()
    m = []
    for i in range(X.shape[1]):
        t = np.mean(X[:, i])
        s = str(round(t, max(1, 2 - math.floor(np.log10(abs(t))))))
        m.append(s)
    out_l = []
    title_l = []
    t_num = title.shape[0]
    for i in range(t_num):
        tt = title[i] + '(' + m[i] + ')'
        print(tt)
        d = inter[i]
        d = np.array(d)
        d = d.astype(str).flatten().tolist()
        print(d)
        d_temp = np.zeros((X.shape[0], len(d) + 1))
        t_list = X[:, i].flatten().tolist()
        for j in range(X.shape[0]):
            t = t_list[j]
            for k in range(len(d) + 1):
                if k == 0 and t < float(d[0]):
                    d_temp[j, 0] = 1
                elif k == len(d) and t >= float(d[-1]):
                    d_temp[j, -1] = 1
                elif (k != 0 and k != len(d)) and (float(d[k - 1]) <= t < float(d[k])):
                    d_temp[j, k] = 1
        out_l.append(d_temp)
        e = []
        for k in range(len(d) + 1):
            if k == 0:
                e.append(tt + '<' + d[0])
            elif k == len(d):
                e.append(d[-1] + '<=' + tt)
            else:
                e.append(d[k - 1] + '<=' + tt + '<' + d[k])
        e = np.array(e).reshape(len(e), 1)
        title_l.append(e)
    o = out_l[0].copy()
    for i in range(len(out_l) - 1):
        o = np.hstack((o, out_l[i + 1]))
    del_list = []
    for j in range(o.shape[1]):
        if np.sum(o[:, j]) == 0:
            del_list.append(j)
    o = np.delete(o, del_list, axis=1)
    ttt = title_l[0].copy()
    for i in range(len(title_l) - 1):
        ttt = np.vstack((ttt, title_l[i + 1]))
    ttt = np.delete(ttt, del_list, axis=0)
    X_temp = np.zeros((o.shape[0], o.shape[1]))
    index = -1
    a = []
    for i in range(o.shape[0]):
        if str(o[i, :].flatten().tolist()) not in a:
            a.append(str(o[i, :].flatten().tolist()))
            index += 1
            for j in range(o.shape[1]):
                X_temp[index, j] += o[i, j]
        else:
            ii = a.index(str(o[i, :].flatten().tolist()))
    X_out = X_temp[:index + 1, :]
    if directory is None:
        np.savetxt('Features_'+notes+str(X_out.shape[0])+'_'+str(X_out.shape[1])+'.csv', X_out, fmt='%s', delimiter=',')
        np.savetxt('Title_'+notes+str(X_out.shape[1])+'.csv', ttt, fmt='%s', delimiter=',')
    else:
        if not os.path.exists(directory):
            os.mkdir(directory)
        save_name = Path('', directory, 'Features_' + notes + str(X_out.shape[0]) + '_' + str(X_out.shape[1]) + '.csv')
        np.savetxt(save_name, X_out, fmt='%s', delimiter=',')
        save_name = Path('', directory, 'Title_' + notes + str(X_out.shape[1]) + '.csv')
        np.savetxt(save_name, ttt, fmt='%s', delimiter=',')


def ExtractX(X, origin_title, subset_title, directory=None, notes=''):
    """
    Cut the Feature Matrix by given feature name list

    :param X: Feature Matrix
    :param origin_title: old title with type of numpy.array and shape of (num_featrues, 1)
    :param subset_title: new title with type of numpy.array and shape of (num_featrues_new, 1)
    :param directory: Directory to save outputs, default as 'None', for example 'data_out'
    :param notes: Notes in file name, default as ''

    :return: None

    example:
    DChemPy.Dataset.ExtractX(X, title_old, title_new, directory='data_out')
    """
    data_out = []
    title_out = []
    if type(origin_title) is np.ndarray:
        t_l_f = list(origin_title.flatten())
    if type(subset_title) is np.ndarray:
        t_l = list(subset_title.flatten())
    for i in range(len(t_l_f)):
        t = t_l_f[i]
        if t in t_l:
            title_out.append(t)
            data_out.append(i)
    X_out = X[:, data_out]
    title_out = np.array(title_out).reshape(len(title_out), 1)
    if directory is None:
        np.savetxt('Features_'+notes+str(X_out.shape[0])+'_'+str(X_out.shape[1])+'.csv', X_out, fmt='%s', delimiter=',')
        np.savetxt('Title_'+notes+str(title_out.shape[0])+'.csv', title_out, fmt='%s', delimiter=',')
    else:
        if not os.path.exists(directory):
            os.mkdir(directory)
        save_name = Path('', directory, 'Features_' + notes + str(X_out.shape[0]) + '_' + str(X_out.shape[1]) + '.csv')
        np.savetxt(save_name, X_out, fmt='%s', delimiter=',')
        save_name = Path('', directory, 'Title_' + notes + str(title_out.shape[0]) + '.csv')
        np.savetxt(save_name, title_out, fmt='%s', delimiter=',')


def DrawDisY(y, name='Y', bins=30, directory=None):
    """
    Draw the distribution of label values

    :param y: Label Value with type of numpy.array and shape of (num_samples, 1)
    :param name: Title of hist plot and Name of saved plot, default as 'Y'
    :param bins: number of bins in hist plot, default as 30
    :param directory: Directory to save outputs, default as 'None', for example 'data_out'

    :return: None

    example:
    DChemPy.Dataset.DrawDisY(y, directory='data_out')
    """
    plt.figure(figsize=(5, 3), dpi=250)
    plt.title('y_dis of ' + name, fontsize=15)
    plt.hist(y, bins=bins, facecolor='lightskyblue', edgecolor='dodgerblue')
    plt.ylabel('Counts', fontsize=15)
    plt.xlabel('Generation(Epoch)', fontsize=15)
    save_name = name + '.png'
    if directory is None:
        plt.savefig(save_name, bbox_inches='tight')
    else:
        if not os.path.exists(directory):
            os.mkdir(directory)
        save_name = Path('', directory, save_name)
        plt.savefig(save_name, bbox_inches='tight')
