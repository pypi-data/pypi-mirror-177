"""
Basic Statistic Analysis

Contents:
DChemPy.Statistic.CovAnalysis: Covariance analysis of full feature matrix
DChemPy.Statistic.FeatRelation: Draw scatter plot of two features and calculate correlation coefficients
DChemPy.Statistic.CorAnalysis: Correlation analysis of full feature matrix
"""

import numpy as np
import scipy
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
import os


def CovAnalysis(X, y, title, draw_pair_num=0, directory=None, notes=''):
    """
    Covariance analysis of full feature matrix

    :param X: Feature matrix, numpy.array, shape (num_samples, num_features)
    :param y: Label values, numpy.array, shape (num_samples, )
    :param title: Title, numpy.array, shape (num_features, )
    :param draw_pair_num: Number of feature pairs with highest abs(cov), int, default as 0
    :param directory: Directory to save outputs, default as 'None', for example 'data_out'
    :param notes: Notes in file name, default as '99'

    :return: None

    example:
    DChemPy.Statistic.CovAnalysis(X, y, title, draw_pair_num=10, directory='xxx')
    """
    if type(y) is np.ndarray:
        y = y.reshape(y.shape[0], )
    elif type(y) is list:
        y = np.array(y).reshape(len(y), )
    if type(title) is np.ndarray:
        title = title.reshape(title.shape[0], )
    elif type(title) is list:
        title = np.array(title).reshape(len(title), )
    for i in range(X.shape[1]):
        X[:, i] = (X[:, i] - np.mean(X[:, i])) / np.std(X[:, i])
    cov_m = np.cov(X, rowvar=False)
    if directory is None:
        save_name = Path('', 'Cov01' + notes + '_CovMatrix_' + str(cov_m.shape[1]) + '_Features.csv')
    else:
        if not os.path.exists(directory):
            os.mkdir(directory)
        save_name = Path('', directory, 'Cov01' + notes + '_CovMatrix_' + str(cov_m.shape[1]) + '_Features.csv')
    np.savetxt(fname=save_name, X=cov_m, fmt='%s', delimiter=',')
    fig = plt.figure(figsize=(10, 8), dpi=250)
    ax = fig.add_axes([0.05, 0.08, 0.91, 0.86])
    im = ax.imshow(cov_m, cmap='plasma_r', origin='lower')
    ax.set_xlabel('Features', fontsize=15)
    ax.set_ylabel('Features', fontsize=15)
    plt.suptitle('Covariance Matrix of ' + str(X.shape[1]) + ' Features', fontsize=20)
    cb = plt.colorbar(im)
    cb.set_label('Covariance', fontsize=15)
    if directory is None:
        save_name = Path('', 'Cov02' + notes + '_CovMatrix_' + str(cov_m.shape[1]) + '_Features.png')
    else:
        save_name = Path('', directory, 'Cov02' + notes + '_CovMatrix_' + str(cov_m.shape[1]) + '_Features.png')
    plt.savefig(save_name)
    data = []
    for i in range(cov_m.shape[0]):
        for j in range(cov_m.shape[1] - i - 1):
            data.append([i, j + 1 + i, cov_m[i, j + 1 + i]])
    data_m = np.array(data)
    fig = plt.figure(figsize=(10, 8), dpi=250)
    ax = fig.add_axes([0.09, 0.08, 0.88, 0.85])
    ax.hist(data_m[:, -1], bins=40, density=False, facecolor='#3CB371', edgecolor='#006400', alpha=0.9)
    ax.set_xlabel('Covariance', fontsize=17)
    ax.set_ylabel('Times', fontsize=17)
    plt.suptitle('Distribution of Covariance of ' + str(X.shape[1]) + ' Features', fontsize=20)
    if directory is None:
        save_name = Path('', 'Cov03' + notes + '_CovDis_' + str(cov_m.shape[1]) + '_Features.png')
    else:
        save_name = Path('', directory, 'Cov03' + notes + '_CovDis_' + str(cov_m.shape[1]) + '_Features.png')
    plt.savefig(save_name)
    plt.close()
    if draw_pair_num:
        permu = np.argsort(-np.abs(data_m[:, -1]))
        data_m_p = data_m[permu, :]
        for _ in range(draw_pair_num):
            x_label = title[int(data_m_p[_, 0]), ]
            y_label = title[int(data_m_p[_, 1]), ]
            if '/' in x_label:
                x_label = x_label.split('/')[0]
            if '/' in y_label:
                y_label = y_label.split('/')[0]
            c_v = data_m_p[_, 2]
            x_data = X[:, int(data_m_p[_, 0])].flatten().tolist()
            y_data = X[:, int(data_m_p[_, 1])].flatten().tolist()
            fig = plt.figure(figsize=(10, 8), dpi=250)
            ax = fig.add_axes([0.11, 0.08, 0.88, 0.82])
            sc = ax.scatter(x_data, y_data, alpha=0.4, c=y, cmap='plasma_r', marker='o')
            ax.set_xlabel(x_label, fontsize=17)
            ax.set_ylabel(y_label, fontsize=17)
            plt.suptitle('Distribution of Data of ' + x_label + '\n vs ' + y_label + '   Covariance: ' + str(
                round(c_v, 5)), fontsize=20)
            plt.colorbar(sc)
            if directory is None:
                save_name = Path('', 'Cov04' + notes + '_Top-' + str(_ + 1) + '_' + x_label + '-' + y_label +
                                 '_' + str(round(c_v, 4)) + '.png')
            else:
                save_name = Path('', directory, 'Cov04' + notes + '_Top-' + str(_ + 1) + '_' + x_label + '-' + y_label +
                                 '_' + str(round(c_v, 4)) + '.png')
            plt.savefig(save_name)
            plt.close()


def FeatRelation(X, y, title, T_1='', T_2='y', x_label=None, y_label=None,
                 T_1_LOG=False, T_2_LOG=False, directory=None, notes=''):
    """
    Draw scatter plot of two features and calculate correlation coefficients
    
    :param X: Feature matrix, numpy.array, shape (num_samples, num_features)
    :param y: Label values, numpy.array, shape (num_samples, )
    :param title: Title, numpy.array, shape (num_features, )
    :param T_1: Name of Feature 1, string
    :param T_2: Name of Feature 2, string, default as 'y'
    :param x_label: Label of Feature 1 on plot, default as None (None means same as T_1)
    :param y_label: Label of Feature 2 on plot, default as None (None means same as T_2)
    :param T_1_LOG: Whether use lg(X[:, title.index(T_1)])
    :param T_2_LOG: Whether use lg(X[:, title.index(T_2)])
    :param directory: Directory to save outputs, default as 'None', for example 'data_out'
    :param notes: Notes in file name, default as ''
    
    :return: None
    
    example:
    DChemPy.Statistic.FeatRelation(X, y, title, T_1='XXX', T_2='y', directory='xxx')
    """
    if type(y) is np.ndarray:
        y = y.reshape(y.shape[0], )
    elif type(y) is list:
        y = np.array(y).reshape(len(y), )
    if type(title) is np.ndarray:
        title = title.reshape(title.shape[0], )
    elif type(title) is list:
        title = np.array(title).reshape(len(title), )
    if x_label is None:
        x_label = T_1
    if y_label is None:
        y_label = T_2
    t_l = title.flatten().tolist()
    t_1 = t_l.index(T_1)
    if T_2 != 'y':
        t_2 = t_l.index(T_2)
    if '/' in x_label:
        x_label = x_label.split('/')[0]
    if '/' in y_label:
        y_label = y_label.split('/')[0]
    xxx = X[:, t_1].flatten().tolist()
    if T_1_LOG:
        x_data = np.log(xxx).flatten().tolist()
        x_label = 'Log(' + x_label + ')'
    else:
        x_data = xxx
    if T_2 != 'y':
        yy = X[:, t_2].flatten().tolist()
        if T_2_LOG:
            y_data = np.log(yy).flatten().tolist()
            y_label = 'Log(' + y_label + ')'
        else:
            y_data = X[:, t_2].flatten().tolist()
    else:
        y_data = y.flatten().tolist()
    x_1 = pd.Series(x_data)
    x_2 = pd.Series(y_data)
    pearson = x_1.corr(x_2, method="pearson")
    spearman = x_1.corr(x_2, method="spearman")
    kendall = x_1.corr(x_2, method="kendall")
    m = np.vstack((np.array(x_data), np.array(y_data)))
    print(m.shape)
    m[0, :] /= np.std(m[0, :])
    m[1, :] /= np.std(m[1, :])
    co = np.cov(m)[0, 1]
    if directory is None:
        save_name = Path('', 'FeatRelation' + notes + '_' + x_label + '_' + y_label + '.png')
    else:
        if not os.path.exists(directory):
            os.mkdir(directory)
        save_name = Path('', directory, 'Relation' + notes + '_' + x_label + '_' + y_label + '.png')
    fig = plt.figure(figsize=(9.2, 8.6), dpi=250)
    ax = fig.add_axes([0.16, 0.10, 0.80, 0.68])
    sc = ax.scatter(x_data, y_data, alpha=0.5, c=y, cmap='magma', marker='o', zorder=5)
    ax.grid(zorder=1)
    ax.set_xlabel(x_label, fontsize=15)
    ax.set_ylabel(y_label, fontsize=15)
    plt.suptitle('Distribution of Data of \n' + x_label + '\n & \n' + y_label + '\nPearson:' + str(round(pearson, 5)) +
                 '      Spearman:' + str(round(spearman, 5)) + '\nKendall:' + str(
        round(kendall, 5)) + '      Covariance:' + str(round(co, 5)), fontsize=18)
    plt.colorbar(sc)
    plt.savefig(save_name)


def CorAnalysis(X, y, title, directory=None, notes=''):
    """
    Correlation analysis of full feature matrix
    
    :param X: Feature matrix, numpy.array, shape (num_samples, num_features)
    :param y: Label values, numpy.array, shape (num_samples, )
    :param title: Title, numpy.array, shape (num_features, )
    :param directory: Directory to save outputs, default as 'None', for example 'data_out'
    :param notes: Notes in file name, default as ''
    
    :return: None
    
    example:
    DChemPy.Statistic.CorAnalysis(X, y, title, directory='xxx')
    """
    if type(y) is np.ndarray:
        y = y.reshape(y.shape[0], )
    elif type(y) is list:
        y = np.array(y).reshape(len(y), )
    if type(title) is np.ndarray:
        title = title.reshape(title.shape[0], )
    elif type(title) is list:
        title = np.array(title).reshape(len(title), )
    y_s = pd.Series(y)
    pearson = []
    spearman = []
    kendall = []
    for i in range(X.shape[1]):
        x_i = pd.Series(X[:, i].flatten().tolist())
        pearson.append(x_i.corr(y_s, method="pearson"))
        spearman.append(x_i.corr(y_s, method="spearman"))
        kendall.append(x_i.corr(y_s, method="kendall"))
    # Pearson Correlation Coefficient
    pearson = np.array(pearson).reshape(len(pearson), 1)
    m_1 = np.hstack((title, pearson))
    arg = np.argsort(-pearson, axis=0).flatten().tolist()
    m_1 = m_1[arg, :]
    t = np.array(['Feature_Name', 'Pearson_Correlation_Coefficient'])
    m_1 = np.vstack((t, m_1))
    if directory is None:
        save_name = Path('', 'Cor01' + notes + '_PearsonCC_' + str(m_1.shape[0] - 1) + '_Features.csv')
    else:
        if not os.path.exists(directory):
            os.mkdir(directory)
        save_name = Path('', directory, 'Cor01' + notes + '_PearsonCC_' + str(m_1.shape[0] - 1) + '_Features.csv')
    np.savetxt(save_name, m_1, fmt='%s', delimiter=',')
    # Speraman Correlation Coefficient
    spearman = np.array(spearman).reshape(len(spearman), 1)
    m_2 = np.hstack((title, spearman))
    arg = np.argsort(-spearman, axis=0).flatten().tolist()
    m_2 = m_2[arg, :]
    t = np.array(['Feature_Name', 'Spearman_Correlation_Coefficient'])
    m_2 = np.vstack((t, m_2))
    if directory is None:
        save_name = Path('', 'Cor02' + notes + '_SpearmanCC_' + str(m_1.shape[0] - 1) + '_Features.csv')
    else:
        save_name = Path('', directory, 'Cor02' + notes + '_SpearmanCC_' + str(m_1.shape[0] - 1) + '_Features.csv')
    np.savetxt(save_name, m_2, fmt='%s', delimiter=',')
    # Kendall Correlation Coefficient
    kendall = np.array(kendall).reshape(len(kendall), 1)
    m_3 = np.hstack((title, kendall))
    arg = np.argsort(-kendall, axis=0).flatten().tolist()
    m_3 = m_3[arg, :]
    t = np.array(['Feature_Name', 'Kendall_Correlation_Coefficient'])
    m_3 = np.vstack((t, m_3))
    if directory is None:
        save_name = Path('', 'Cor03' + notes + '_KendallCC_' + str(m_1.shape[0] - 1) + '_Features.csv')
    else:
        save_name = Path('', directory, 'Cor03' + notes + '_KendallCC_' + str(m_1.shape[0] - 1) + '_Features.csv')
    np.savetxt(save_name, m_3, fmt='%s', delimiter=',')
