import pandas as pd
import numpy as np
from scipy import stats
import math
import matplotlib.pyplot as plt
import seaborn as sns


# Our data will be split into two samples based on a boolean condition, ie hill or no hill
def split_by_bool(dataframe, col):
    true_df = dataframe[dataframe[col]==True]
    false_df = dataframe[dataframe[col]==False]
    return true_df, false_df

# Take 198 (can be changed) samples of size 50 from each split dataframe
# 198 sample size to detect small effect size with power of 0.8 and alpha 0.05.
def get_means_of_sample(dataframe, feature, sample_size = 50, num_sims = 198, seed = 3):
    np.random.seed(seed)
    preds = []
    for i in range(num_sims):
        sample = dataframe.sample(n= sample_size, replace = True)
        mean = np.sum(sample[feature])/sample_size
        preds.append(mean)

    return preds

# Plots the distribution and histograms of the means of our 198 samples
def plot_means_of_sample(dataframe, feature, sample_size = 50, num_sims = 50, seed = 3):
    preds = get_means_of_sample(dataframe, feature, sample_size, num_sims, seed)
    fig = plt.figure(figsize = (10,7))
    sns.distplot(preds, norm_hist = True, bins=15)
    plt.title(f'Distribution of mean of {feature}')
    plt.xlabel(f'Mean {feature}')
    plt.ylabel('Density')
    plt.show()

    
# Cohen's d calculator for 2 sample t-test    
def coh_d(sample1, sample2):
    n_1 = len(sample1)
    n_2 = len(sample2)
    std_1 = np.std(sample1, ddof = 1)
    std_2 = np.std(sample2, ddof = 1)
    dof = n_1 + n_2 - 2
    num = np.mean(sample1) - np.mean(sample2)
    denom = np.sqrt(((n_1 - 1)*std_1**2 + (n_2 - 1)*std_2**2)/dof)
    return num/denom


# Alpha p-value comparison
def compare_pval_alpha(p_val, alpha = 0.05):
    status = ''
    if p_val > alpha:
        status = "Fail to reject"
    else:
        status = 'Reject'
    return status



# Hypothesis test super function
# Splits the data along a boolean condition 
# Samples each split dataframe and returns a sns dist plot
# Plots the distribution of the 2 splits along with their means
# Calculates relevant variances and the ratio of one variance to another to determine similarity
# Plots both densitys on one axis to see the effect size
# Performs ttest or welch t-test depending on the ratio of variances
# Prints summary of the results of the hypothesis test

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
    # Display the dataframes to see the data with which we are working.
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

    print(f'Based on the p value of {p_val} and our aplha of {round(alpha, 3)} we {status.lower()} the null hypothesis.')
          
    if assertion == 'can':
        print(f"with an effect size, cohen's d, of {round(d, 3)} and power of {power}.")
    else:
        print(".")