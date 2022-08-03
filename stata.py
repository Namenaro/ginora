import numpy as np
import scipy.stats.distributions as dist
from scipy import stats
from math import sqrt

def get_p_value_for_two_samples(sample1, sample2):
    # чем ниже п-валью, тем больше вероятность, что выборки "разные"
    # т.е. чем ниже, тем лучше
    ttest, pval = stats.mannwhitneyu(sample1, sample2, use_continuity=False, alternative="two-sided")
    return pval

def get_p_value_for_paramentric_case(num_ones, sample_len, p_one):
    #https://mse.msu.ru/wp-content/uploads/2020/03/%D0%9B%D0%B5%D0%BA%D1%86%D0%B8%D1%8F-6-%D0%9F%D1%80%D0%BE%D0%B2%D0%B5%D1%80%D0%BA%D0%B0-%D0%B3%D0%B8%D0%BF%D0%BE%D1%82%D0%B5%D0%B7.pdf
    p=num_ones/sample_len #доля признака в выборке

    if p_one<0.0000001:
        p_one = 0.0000001
    if p_one == 1.0:
        p_one=0.999999

    q0 = 1 - p_one
    z=(p-p_one)/sqrt(p_one*q0/sample_len)  #z сходится по распределению к стандартной нормальной величине при sample_len → ∞.
    # рассчитываем  p-value
    pvalue = 2 * dist.norm.cdf(-np.abs(z))  # Multiplied by two indicates a two tailed testing.
    return pvalue

def get_p_value_for_one_sample(sample, p_one):
    sample_size1 = len(sample)
    num_successes1 = 0
    for res in sample:
        if res == True:
            num_successes1 += 1
    p_val = get_p_value_for_paramentric_case(num_successes1, sample_size1, p_one)
    return p_val

def test_one_sample():
    p_one = 0.07
    num_ones = 5
    sample_len = 10
    pval = get_p_value_for_paramentric_case(num_ones, sample_len, p_one)
    print(pval)


if __name__ == "__main__":
    test_one_sample()
