# Import libraries
import numpy as np
import pandas as pd
from scipy import stats



def ttest_from_df(df
                  , group_column
                  , metric_column
                 ):
    """
    This function performs a t test of 2 independent samples on a dataframe.
    :param df: clean pandas DataFrame
    :param group_column: The Column in the dataframe which contains the group information
    :param metric_column: The column containg the conversion metric needs to be 0 and 1
    :return: dictionary of all possible combinations in group_column and the p_value (rounded to 10 digits)
    """
    results_dict = {}
    loop_dict = {}
    
    for group in df[group_column].unique():
        
        loop_dict[group] = df[df[group_column] == group][metric_column]
    
    for A in loop_dict:
        for B in loop_dict:
            if A == B:
                continue
            
            if f"{B}:{A}" in results_dict:
                continue
            
            p_value = stats.ttest_ind(loop_dict[A], loop_dict[B])[1] # check scipy doc for other ttests
            
            if p_value < 0.01:
                result = "99% significant"
            elif p_value < 0.05:
                result = "95% significant"
            else:
                result = "not significant"    
            
            results_dict[f"{A}:{B}"] = (result, round(p_value, 10))

    return results_dict



def ttest_from_np_arrays(A
                         ,B
                        ):
    """
    This function performs a t test of 2 independent samples on a dataframe.
    :param A: first Array
    :param B: second Array
    :return: tuple of a statement of significance and the p_value (rounded to 10 digits)
    """
    p_value = stats.ttest_ind(A, B)[1] # check scipy doc for other ttests

    if p_value < 0.01:
        result = "99% significant"
    elif p_value < 0.05:
        result = "95% significant"
    else:
        result = "not significant"     
    
    return (result, round(p_value, 10))



def chi_square_test(df
                    , group_column
                    , metric_column
                   ):
    """
    This function performs a chi squared test on a dataframe.
    :param df: clean pandas DataFrame
    :param group_column: The Column in the dataframe which contains the group information
    :param metric_column: The column containg the conversion metric needs to be 0 and 1
    :return: dictionary with names of tested groups as key and a tuple with significance statement and p_value as values
    """
    
    results_dict = {}
    loop_dict = {}
    
    # split into one dataframe per entry in group column
    for group in df[group_column].unique():
        
        loop_dict[group] = df[df[group_column] == group][metric_column]
    
    # initialize an 2x2 Array with zeros 
    # each row is a treatment (Control, vs Test Group)
    # col 1 are successful and col 2 unsuccessful events
    T = np.zeros((2,2))
    
    for A in loop_dict:
        for B in loop_dict:
            if A == B:
                continue
            
            if f"{B}:{A}" in results_dict:
                continue

            # A
            T[0][0] = loop_dict[A].sum()
            T[0][1] = len(loop_dict[A]) - loop_dict[A].sum()
            
            # B
            T[1][0] = loop_dict[B].sum()
            T[1][1] = len(loop_dict[B]) - loop_dict[B].sum()
                
            # calculate the chi square parameters
            p_value = stats.chi2_contingency(T, correction = False)[1]                
                
            if p_value < 0.01:
                result = "99% significant"
            elif p_value < 0.05:
                result = "95% significant"
            else:
                result = "not significant"                  
            
            results_dict[f"{A}:{B}"] = (result, round(p_value, 10))
    
    return results_dict