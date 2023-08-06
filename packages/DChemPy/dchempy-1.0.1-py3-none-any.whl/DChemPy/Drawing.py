import numpy as np
import matplotlib.pyplot as plt
import os
from pathlib import Path


def TPScatterOneEpoch(true_train, pred_train, true_test, pred_test, notes='99', directory=None, plt_title='Regression'):
    from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
    train_mse = mean_squared_error(true_train, pred_train)
    train_mae = mean_absolute_error(true_train, pred_train)
    train_r2 = r2_score(true_train, pred_train)
    test_mse = mean_squared_error(true_test, pred_test)
    test_mae = mean_absolute_error(true_test, pred_test)
    test_r2 = r2_score(true_test, pred_test)
    fig = plt.figure(figsize=(7, 7.8), dpi=300)
    ax = fig.add_axes([0.15, 0.09, 0.78, 0.74])
    ax.scatter(true_train, pred_train, s=25, alpha=0.75)
    ax.scatter(true_test, pred_test, s=25, alpha=0.75)
    inter = max(max(true_train) - min(true_train), max(true_test) - min(true_test))
    left_limit = min(min(true_test)-0.2*inter, min(true_train)-0.2*inter)
    right_limit = max(max(true_test)+0.2*inter, max(true_train)+0.2*inter)
    ax.plot([left_limit, right_limit], [left_limit, right_limit], 'r:')
    ax.plot([left_limit, right_limit], [left_limit+1, right_limit+1], 'y:')
    ax.plot([left_limit, right_limit], [left_limit-1, right_limit-1], 'y:')
    ax.legend(['Correct', 'Correct+1', 'Correct-1', 'Train', 'Test'], loc='upper left',
              shadow=True, fontsize=17)
    ax.set_xlabel('True Values', fontsize=18)
    ax.set_ylabel('Prediction Values', fontsize=18)
    plt.suptitle(plt_title+' SingleFit True-Predict Scatter' +
                 '\nTrain R^2: '+str(round(train_r2, 5))+'  Test R^2: '+str(round(test_r2, 5)) +
                 '\nTrain MSE: '+str(round(train_mse, 5))+'  Test MSE: '+str(round(test_mse, 5)) +
                 '\nTrain MAE: '+str(round(train_mae, 5))+'  Test MAE: '+str(round(test_mae, 5)), fontsize=18)
    save_name = plt_title+'_'+notes+'_R2-'+str(round(test_r2, 4))+'_Scatter.png'
    if directory is None:
        save_name = Path('', save_name)
    else:
        if not os.path.exists(directory):
            os.mkdir(directory)
        save_name = Path('', directory, save_name)
    plt.savefig(save_name)
    plt.close()


def TPScatterAllEpochTwoSet(true_y, mean_list, std_list, mean_mse, mean_mae, mean_r2, num_epoch,
                            plt_title, draw_type='MeanAllPred-True', notes='03', directory=None):
    fig = plt.figure(figsize=(10, 8), dpi=300)
    ax = fig.add_axes([0.11, 0.08, 0.88, 0.815])
    sc = ax.scatter(true_y, mean_list, alpha=0.55, c=std_list, cmap='viridis', marker='o')
    inter = max(max(true_y) - min(true_y), max(mean_list) - min(mean_list))
    left_limit = min(min(true_y) - 0.2 * inter, min(mean_list) - 0.2 * inter)
    right_limit = max(max(true_y) + 0.2 * inter, max(mean_list) + 0.2 * inter)
    ax.plot([left_limit, right_limit], [left_limit, right_limit], color='#B22222', linestyle=':', linewidth='2')
    ax.plot([left_limit, right_limit], [left_limit + 1, right_limit + 1], color='#FFA500', linestyle=':', linewidth='2')
    ax.plot([left_limit, right_limit], [left_limit - 1, right_limit - 1], color='#FFA500', linestyle=':', linewidth='2')
    ax.legend(['Correct', 'Correct+1', 'Correct-1', 'Mean of Prediction'], loc='upper left', fontsize=17, shadow=True)
    ax.set_xlabel('True Values', fontsize=17)
    ax.set_ylabel('Mean Pred Values (2T)', fontsize=17)
    plt.suptitle(plt_title+' Scatter of '+draw_type+' of ' + str(num_epoch) + ' Rounds\n' +
                 'Mean Pred:  MSE: ' + str(round(mean_mse, 4)) +
                 '  MAE: ' + str(round(mean_mae, 4)) +
                 '  R^2: ' + str(round(mean_r2, 4)), fontsize=21)
    cb = plt.colorbar(sc)
    cb.set_label('Standard Deviation of Prediction Values', fontsize=17)
    plt.grid(which='major', color='#D5D5D5', alpha=0.5)
    save_name = plt_title+'_'+notes+'a_'+draw_type+'_Scatter_MeanR2-'+str(round(mean_r2, 4))+'.png'
    if directory is None:
        save_name = Path('', save_name)
    else:
        if not os.path.exists(directory):
            os.mkdir(directory)
        save_name = Path('', directory, save_name)
    plt.savefig(save_name)
    plt.close()

    out = np.hstack((np.array(mean_list).reshape(len(mean_list), 1),
                     np.array(std_list).reshape(len(mean_list), 1)))
    out = np.hstack((np.array(true_y).reshape(len(mean_list), 1), out))
    out = np.hstack((np.linspace(0, len(mean_list) - 1, len(mean_list), dtype=int).reshape(len(mean_list), 1), out))
    out = np.vstack((np.array(['Index', 'True Values', 'Mean Pred Values',
                               'Mean Standard Deviation of Pred Values']).reshape(1, 4),
                     out))
    save_name = plt_title+'_'+notes+'a_'+draw_type+'_RawData_MeanR2-'+str(round(mean_r2, 4))+'.csv'
    if directory is None:
        save_name = Path('', save_name)
    else:
        save_name = Path('', directory, save_name)
    np.savetxt(save_name, out, fmt='%s', delimiter=',')

    me_plot_list = []
    for i in range(len(mean_list)):
        me_plot_list.append(mean_list[i] - true_y[i])
    fig = plt.figure(figsize=(12, 6), dpi=300)
    ax = fig.add_axes([0.08, 0.11, 0.95, 0.815])
    x_idx = np.linspace(0, len(me_plot_list) - 1, len(me_plot_list))
    sc = ax.scatter(x_idx, me_plot_list, alpha=1.0, c=std_list, cmap='viridis', marker='o')
    ax.set_xlabel('Sample ID', fontsize=17)
    ax.set_ylabel('Deviation of Mean Pred Values (2T)', fontsize=17)
    ax.plot([0, len(me_plot_list)], [0, 0], color='#B22222', linestyle=':', linewidth='2')
    ax.plot([0, len(me_plot_list)], [1, 1], color='#FFA500', linestyle=':', linewidth='2')
    ax.plot([0, len(me_plot_list)], [-1, -1], color='#FFA500', linestyle=':', linewidth='2')
    cb = plt.colorbar(sc)
    cb.set_label('Standard Deviation of Prediction Values', fontsize=17)
    plt.grid(which='major', color='#D5D5D5', alpha=0.5)
    plt.suptitle(plt_title+' Scatter of '+draw_type+' Deviation vs ID of ' + str(num_epoch) + ' Rounds', fontsize=21)
    save_name = plt_title+'_'+notes+'a_'+draw_type+'_Deviation_MeanR2-'+str(round(mean_r2, 4))+'.png'
    if directory is None:
        save_name = Path('', save_name)
    else:
        save_name = Path('', directory, save_name)
    plt.savefig(save_name)
    plt.close()


def PerformanceHist(p_list, plt_title, num_epoch, n_bins=30, draw_type='MSE', notes='05', directory=None):
    from scipy.stats import norm
    mu_p = np.mean(p_list)
    sigma_p = np.std(p_list)
    p_array = np.array(p_list).reshape(len(p_list), 1)
    p_sorted = np.sort(p_array, axis=0)
    fig = plt.figure(figsize=(8, 8), dpi=300)
    ax = fig.add_axes([0.11, 0.08, 0.85, 0.81])
    if draw_type == 'MSE':
        fc = '#4682B4'
        ec = '#505050'
        lc = '#483D8B'
    elif draw_type == 'MAE':
        fc = '#3CB371'
        ec = '#006400'
        lc = '#B2F200'
    else:
        fc = '#FF6347'
        ec = '#FF4500'
        lc = '#B22222'
    n, bins_p, patches = ax.hist(p_sorted, bins=n_bins, density=1,
                                 facecolor=fc, edgecolor=ec, alpha=0.75, linewidth=1.6)
    pn = norm.pdf(bins_p, mu_p, sigma_p)
    plt.plot(bins_p, pn, color=lc, linestyle=':', linewidth='2')
    plt.suptitle('Distribution of '+plt_title+' '+draw_type+' of ' + str(num_epoch) +
                 ' Rounds\nMean:' + str(round(mu_p, 4)) +
                 '    STD:' + str(round(sigma_p, 4)), fontsize=22)
    ax.set_ylabel('Counts', fontsize=17)
    ax.set_xlabel(draw_type, fontsize=17)
    save_name = plt_title+'_'+notes+'_'+draw_type+'_Distribution.png'
    if directory is None:
        save_name = Path('', save_name)
    else:
        if not os.path.exists(directory):
            os.mkdir(directory)
        save_name = Path('', directory, save_name)
    plt.savefig(save_name)


def FeatureImportanceHist(f_i, title, plt_title, num_draw=10, notes='06', directory=None):
    f_i_temp = f_i.reshape(f_i.shape[0], 1)
    title = title.reshape(title.shape[0], )
    f_i_temp[:, 0] = 100.0 * (f_i_temp[:, 0] / (max(f_i_temp[:, 0]) - min(f_i_temp[:, 0])))
    sorted_idx = np.argsort(-f_i_temp[:, 0])
    pos = np.arange(sorted_idx.shape[0]) + .5
    if len(pos) >= num_draw:
        fig = plt.figure(figsize=(11, 8), dpi=250)
        ax = fig.add_axes([0.11, 0.08, 0.85, 0.84])
        ax.barh(pos[:num_draw, ], f_i_temp[sorted_idx[:num_draw, ], 0].flatten().tolist(),
                align='center', color='#CD5C5C', edgecolor='#A52A2A', linewidth=1.6)
        plt.yticks(pos[:num_draw, ], title[sorted_idx[:num_draw, ]])
        ax.set_xlabel('Relative Importance', fontsize=17)
        plt.suptitle('Feature Importance (First 10) of '+plt_title, fontsize=20)
        save_name = plt_title+'_'+notes+'a_Feature_Importance.png'
        if directory is None:
            save_name = Path('', save_name)
        else:
            if not os.path.exists(directory):
                os.mkdir(directory)
            save_name = Path('', directory, save_name)
        plt.savefig(save_name)
    else:
        num_f = sorted_idx.shape[0]
        fig = plt.figure(figsize=(11, 8), dpi=250)
        ax = fig.add_axes([0.11, 0.08, 0.85, 0.84])
        ax.barh(pos[:num_f, ], f_i_temp[sorted_idx[:num_f, ], 0].flatten().tolist(),
                align='center', color='#CD5C5C', edgecolor='#A52A2A', linewidth=1.6)
        plt.yticks(pos[:num_f, ], title[sorted_idx[:num_f, ]])
        ax.set_xlabel('Relative Importance', fontsize=17)
        plt.suptitle('Feature Importance (First ' + str(int(num_f)) + ') of '+plt_title, fontsize=20)
        save_name = plt_title+'_'+notes+'a_Feature_Importance.png'
        if directory is None:
            save_name = Path('', save_name)
        else:
            if not os.path.exists(directory):
                os.mkdir(directory)
            save_name = Path('', directory, save_name)
        plt.savefig(save_name)
    feature_out = np.hstack((title.reshape(title.shape[0], 1), f_i_temp))
    save_name = plt_title+'_'+notes+'b_All_Feature_Importance.csv'
    if directory is None:
        save_name = Path('', save_name)
    else:
        save_name = Path('', directory, save_name)
    np.savetxt(save_name, feature_out[sorted_idx.flatten().tolist(), :], fmt='%s', delimiter=',')


def SHAPScatter(feat_value, heter_value, label_value, f_name, norm_f_i, plt_title,
                inter_1d=20, notes='', directory=None):
    from math import floor
    feat_value = feat_value.reshape(feat_value.shape[0], )
    heter_value = heter_value.reshape(heter_value.shape[0], )
    if f_name[-1] == ')':
        for j in range(len(f_name)):
            index = len(f_name) - j - 1
            if f_name[index] == '(':
                break
        f_name = f_name[:index - 1]
    if max(feat_value) > 0:
        ii = (max(feat_value) * 1.001 - min(feat_value)) / inter_1d
    else:
        ii = (max(feat_value) * 0.999 - min(feat_value)) / inter_1d
    fig = plt.figure(figsize=(8, 8), dpi=300)
    ax = fig.add_axes([0.11, 0.29, 0.70, 0.60])
    ax2 = fig.add_axes([0.11, 0.11, 0.70, 0.17])
    ax_bar = fig.add_axes([0.85, 0.11, 0.04, 0.78])
    x_idx = []
    x_inter = [min(feat_value)]
    x_ticks_blank = ['']
    x_ticks = [str(round(min(feat_value), 2))]
    y_mean_data = np.zeros((inter_1d, 1))
    y_mean_count = np.zeros((inter_1d, 1))
    for j in range(feat_value.shape[0]):
        y_mean_data[floor((feat_value[j, ] - min(feat_value)) / ii), 0] += heter_value[j, ]
        y_mean_count[floor((feat_value[j, ] - min(feat_value)) / ii), 0] += 1
    for j in range(inter_1d):
        x_idx.append(ii * (0.5 + j) + min(feat_value))
        x_inter.append(ii * j + ii + min(feat_value))
        x_ticks.append(str(round(ii * (j + 1) + min(feat_value), 2)))
        x_ticks_blank.append('')
        if y_mean_count[j, 0] != 0:
            y_mean_data[j, 0] /= y_mean_count[j, 0]
        else:
            y_mean_data[j, 0] = y_mean_data[j - 1, 0]
    x_data = feat_value.flatten().tolist()
    y_data = heter_value.flatten().tolist()
    y = label_value.flatten().tolist()
    sc = ax.scatter(x_data, y_data, c=y, cmap='viridis', marker='o', zorder=5)
    ax.plot(x_idx, y_mean_data, color='#EE82EE', linewidth=3, zorder=10, marker='o')
    ax.set_ylim(min(y_data) - 0.2 * (max(y_data) - min(y_data)), max(y_data) + 0.1 * (max(y_data) - min(y_data)))
    t = []
    for j in range(feat_value.shape[0]):
        t.append(min(y_data) - 0.1 * (max(y_data) - min(y_data)))
    ax.scatter(x_data, t, marker='|', alpha=0.1, color='#C0C0C0')
    plt.suptitle('SHAP Value vs Feature Value Plot of\n' + f_name + '  NormFI:' + str(round(norm_f_i, 2)),
                 fontsize=22)
    ax2.hist(x_data, inter_1d, density=1, facecolor='#3CB371', edgecolor='#006400', alpha=0.75, linewidth=1.6)
    ax2.set_xlabel(f_name, fontsize=17)
    ax.set_ylabel('SHAP Value of y', fontsize=17)
    ax2.set_ylabel('Count', fontsize=17)
    ax.set_xticks(x_inter)
    ax.set_xticklabels(x_ticks_blank)
    ax2.set_xticks(x_inter)
    ax2.set_xticklabels(x_ticks, rotation=45, fontsize=11)
    ax.grid(which='major', color='#D5D5D5', alpha=0.5, zorder=2)
    cb = plt.colorbar(sc, cax=ax_bar)
    cb.set_label('Label Value (Y)', fontsize=17)
    save_name = plt_title+'_'+notes+'SHAP-Scatter_' + f_name + '.png'
    if directory is None:
        save_name = Path('', save_name)
    else:
        if not os.path.exists(directory):
            os.mkdir(directory)
        save_name = Path('', directory, save_name)
    plt.savefig(save_name)
    plt.close()

    o = np.hstack((feat_value.reshape(feat_value, 1), heter_value.reshape(heter_value.shape[0], 1)))
    save_name = plt_title + '_' + notes + 'b_SHAP-Scatter_Data_' + f_name + '.csv'
    if directory is None:
        save_name = Path('', save_name)
    else:
        save_name = Path('', directory, save_name)
    np.savetxt(save_name, o, fmt='%s', delimiter=',')


def ALEPlot(feat_value, heter_value, f_name, plt_title, inter_1d=20, notes='', directory=None):
    feat_value = feat_value.reshape(feat_value.shape[0], )
    fig = plt.figure(figsize=(8, 8), dpi=300)
    ax = fig.add_axes([0.11, 0.29, 0.85, 0.64])
    ax2 = fig.add_axes([0.11, 0.11, 0.85, 0.17])
    x_idx = []
    x_inter = [min(feat_value)]
    x_ticks_blank = ['']
    x_ticks = [str(round(min(feat_value), 2))]
    ii = (max(feat_value) * 1.00001 - min(feat_value)) / inter_1d
    for i in range(inter_1d):
        x_idx.append(ii * (0.5 + i) + min(feat_value))
        x_inter.append(ii * i + ii + min(feat_value))
        x_ticks.append(str(round(ii * (i + 1) + min(feat_value), 2)))
        x_ticks_blank.append('')
    y_data = heter_value.flatten().tolist()
    ax.plot(x_idx, y_data, color='#483D8B', linestyle=':', linewidth=3, marker='o',
            markersize=12, zorder=10)
    ax.set_ylim(min(y_data) - 0.2 * (max(y_data) - min(y_data)),
                max(y_data) + 0.1 * (max(y_data) - min(y_data)))
    t = []
    for i in range(feat_value.shape[0]):
        t.append(min(y_data) - 0.1 * (max(y_data) - min(y_data)))
    ax.scatter(feat_value, t, marker='|', alpha=0.1, color='#C0C0C0')
    plt.suptitle('1D ALE Plot of ' + f_name, fontsize=23)
    ax2.hist(feat_value, inter_1d, density=1, facecolor='#3CB371', edgecolor='#006400',
             alpha=0.75, linewidth=1.6)
    ax2.set_xlabel(f_name, fontsize=17)
    ax.set_ylabel('ALE Value of y', fontsize=17)
    ax2.set_ylabel('Count', fontsize=17)
    ax.set_xticks(x_inter)
    ax.set_xticklabels(x_ticks_blank)
    ax2.set_xticks(x_inter)
    ax2.set_xticklabels(x_ticks, rotation=80, fontsize=11)
    ax.grid(which='major', color='#D5D5D5', alpha=0.5)
    save_name = plt_title+'_'+notes+'a_1D-ALE_Plot.png'
    if directory is None:
        save_name = Path('', save_name)
    else:
        if not os.path.exists(directory):
            os.mkdir(directory)
        save_name = Path('', directory, save_name)
    plt.savefig(save_name)
    plt.close()

    o = np.hstack((np.array(x_idx).reshape(len(x_idx), 1), heter_value.reshape(heter_value.shape[0], 1)))
    save_name = plt_title+'_'+notes+'b_1D-ALE_Data_'+f_name+'.csv'
    if directory is None:
        save_name = Path('', save_name)
    else:
        save_name = Path('', directory, save_name)
    np.savetxt(save_name, o, fmt='%s', delimiter=',')


def ReduceDimScatter(X_new, y, plt_title, notes='', directory=None):
    y = y.reshape(y.shape[0], )
    save_name = plt_title+'_'+notes+'_ReduceDim_X.csv'
    if directory is None:
        save_name = Path('', save_name)
    else:
        if not os.path.exists(directory):
            os.mkdir(directory)
        save_name = Path('', directory, save_name)
    np.savetxt(save_name, X_new, fmt='%s', delimiter=',')
    fig = plt.figure(figsize=(10, 8), dpi=300)
    ax = fig.add_axes([0.11, 0.08, 0.88, 0.815])
    sc = ax.scatter(X_new[:, 0], X_new[:, 1], alpha=0.75, c=y, cmap='viridis', marker='o', zorder=20)
    ax.set_xlabel('Dim-1', fontsize=17)
    ax.set_ylabel('Dim-2', fontsize=17)
    plt.suptitle('Scatter of Dimesion Reducing Results by '+plt_title+'\n', fontsize=21)
    cb = plt.colorbar(sc)
    cb.set_label('Label Value', fontsize=17)
    plt.grid(which='major', color='#D5D5D5', alpha=0.5, zorder=1)
    save_name = plt_title+'_'+notes+'_ReduceDim-Scatter.png'
    if directory is None:
        save_name = Path('', save_name)
    else:
        save_name = Path('', directory, save_name)
    plt.savefig(save_name)
    plt.close()
