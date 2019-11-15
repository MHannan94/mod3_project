"""
This module is for your final hypothesis tests.
Each hypothesis test should tie to a specific analysis question.

Each test should print out the results in a legible sentence
return either "Reject the null hypothesis" or "Fail to reject the null hypothesis" depending on the specified alpha
"""

import pandas as pd
import numpy as np
from scipy import stats
import math
import matplotlib.pyplot as plt
import seaborn as sns


def split_by_bool(dataframe, col):
    true_df = dataframe[dataframe[col]==True]
    false_df = dataframe[dataframe[col]==False]
    return true_df, false_df

def get_means_of_sample(dataframe, feature, sample_size = 50, num_sims = 50, seed = 3):
    np.random.seed(seed)
    preds = []
    for i in range(num_sims):
        sample = dataframe.sample(n= sample_size, replace = True)
        mean = np.sum(sample[feature])/sample_size
        preds.append(mean)

    return preds

def plot_means_of_sample(dataframe, feature, sample_size = 50, num_sims = 50, seed = 3):
    preds = get_means_of_sample(dataframe, feature, sample_size, num_sims, seed)
    fig = plt.figure(figsize = (10,7))
    sns.distplot(preds, norm_hist = True, bins=15)
    plt.title(f'Distribution of mean of {feature}')
    plt.xlabel(f'Mean {feature}')
    plt.ylabel('Density')
    plt.show()

def coh_d(sample1, sample2):
    n_1 = len(sample1)
    n_2 = len(sample2)
    std_1 = np.std(sample1, ddof = 1)
    std_2 = np.std(sample2, ddof = 1)
    dof = n_1 + n_2 - 2
    num = np.mean(sample1) - np.mean(sample2)
    denom = np.sqrt(((n_1 - 1)*std_1**2 + (n_2 - 1)*std_2**2)/dof)
    return num/denom



# def create_sample_dists(cleaned_data, y_var=None, categories=[]):
#     """
#     Each hypothesis test will require you to create a sample distribution from your data
#     Best make a repeatable function

#     :param cleaned_data:
#     :param y_var: The numeric variable you are comparing
#     :param categories: the categories whose means you are comparing
#     :return: a list of sample distributions to be used in subsequent t-tests

#     """
#     htest_dfs = []

#     # Main chunk of code using t-tests or z-tests
#     return htest_dfs

def compare_pval_alpha(p_val, alpha = 0.05):
    status = ''
    if p_val > alpha:
        status = "Fail to reject"
    else:
        status = 'Reject'
    return status


def hypothesis_test(cleaned_data, split_col, test_col, alpha = 0.05, num_sim = 198):
    """
    Describe the purpose of your hypothesis test in the docstring
    These functions should be able to test different levels of alpha for the hypothesis test.
    If a value of alpha is entered that is outside of the acceptable range, an error should be raised.

    :param alpha: the critical value of choice
    :param cleaned_data:
    :return:
    """
    np.random.seed(3)
    if alpha <= 0 or alpha >= 1:
        return 'Error. Alpha value must be between 0 and 1.'
    if type(test_col) != str or type(split_col) != str:
        return 'Error. Input column names as strings'
    # Get data for tests
    true_df, false_df = split_by_bool(cleaned_data, split_col)
    
    display(true_df.head())
    print('\n')
    display(false_df.head())
    plot_means_of_sample(true_df, test_col)
    plot_means_of_sample(false_df, test_col)

    ###
    # Main chunk of code using t-tests or z-tests, effect size, power, etc
    ###
    sample1 = get_means_of_sample(true_df, test_col, num_sims = num_sim)
    sample2 = get_means_of_sample(false_df, test_col, num_sims = num_sim)
    
    fig = plt.figure(figsize = (10,7))
    sns.distplot(sample1, hist=False, norm_hist=True, label= '{}'.format(split_col).title(), color='red')
    sns.distplot(sample2, hist=False, norm_hist=True, label='Not {}'.format(split_col).title(), color='skyblue')
    plt.axvline(x = np.mean(sample1), color='red')
    plt.axvline(x = np.mean(sample2), color='skyblue')
    plt.xlabel('Mean of {}'.format(test_col))
    plt.ylabel('Density')
    plt.title('Comparison of distributions')
    plt.legend();
    
    
    v1 = np.var(sample1)
    v2 = np.var(sample2)

    print('{} var = {}'.format(split_col,round(v1, 3)) + '\nNon-{} var = {}'.format(split_col, round(v2, 3)))
    
    ratio = v1/v2
    
    if ratio < 0.75 or ratio > 1.25:
        print("The ratio {} is not close enough to 1 to use a t-test, so we use Welch's t-test".format(round(ratio, 3)))
        results = stats.ttest_ind(sample1, sample2, equal_var= False)
        t_val = results[0]
        p_val = results[1]
    else:
        print("The ratio {} is close enough to 1 to use a t-test".format(round(ratio, 3)))
        results = stats.ttest_ind(sample1, sample2)
        t_val = results[0]
        p_val = results[1]
        
    d = coh_d(sample1, sample2)
    
    power = 0.8
    # starter code for return statement and printed results
    status = compare_pval_alpha(p_val, alpha)
    assertion = ''
    if status == 'Fail to reject':
        assertion = 'cannot'
    else:
        assertion = "can"
        # calculations for effect size, power, etc here as well

    print(f'Based on the p value of {p_val} and our aplha of {round(alpha, 3)} we {status.lower()} the null hypothesis.')
          
    if assertion == 'can':
        print(f"with an effect size, cohen's d, of {round(d, 3)} and power of {power}.")
    else:
        print(".")


# def hypothesis_test_two():
#     pass

# def hypothesis_test_three():
#     pass

# def hypothesis_test_four():
#     pass
