#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 19 13:00:10 2020

@author: antonio
"""

from general_utils import parse_ann, argparser

def compute_iaa(df1, df2, relevant_colnames):
    '''
    Compute IAA

    Parameters
    ----------
    df1 : pandas dataframe
        Annotations of annotator 1
    df2 : pandas dataframe
        Annotations of annotator 1
    relevant_colnames : list
        List of relevant column names to compute IAA.

    Returns
    -------
    float
        IAA (pairwise agreement: intersection / union)

    '''
    df1_codes = df1[relevant_colnames].drop_duplicates(subset = relevant_colnames)
    df2_codes = df2[relevant_colnames].drop_duplicates(subset = relevant_colnames)
    df1_fc = set(df1_codes.apply('|'.join, axis=1).tolist())
    df2_fc = set(df2_codes.apply('|'.join, axis=1).tolist())
    
    return len(df1_fc.intersection(df2_fc)) / len(df1_fc.union(df2_fc))

def filter_pandas(df, column, values):
    return df[df[column].isin(values)]


if __name__ == '__main__':
    
    ##### Get inputs #####
    path_annot1, path_annot2, rel_variables, rel_labels = argparser()
    relevant_colnames = rel_variables.split(',')
    relevant_labels= rel_labels.split(',')

    ##### GET ANN INFORMATION #####
    df1, _ = parse_ann(path_annot1, '')
    df2, _ = parse_ann(path_annot2, '')
    
    ##### FILTER OUT LABELS NOT RELEVANT #####
    df1 = filter_pandas(df1, 'label', relevant_labels)
    df2 = filter_pandas(df2, 'label', relevant_labels)

    ##### COMPUTE IAA #####
    print('-----------------------------------------------------------------')
    print('IAA taking into account {}'.format(rel_variables))
    print('-----------------------------------------------------------------')
    print(round(compute_iaa(df1, df2, relevant_colnames),3))