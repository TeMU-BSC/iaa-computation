#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 19 13:00:10 2020

@author: antonio
"""

from collections import Counter

def computations(list_df, relevant_colnames, annotator_names, by_label=False):
    '''
    Compute IAA

    Parameters
    ----------
    list_df : list
        Contains one pandas dataframe per annotator.
    relevant_colnames : list
        List of relevant column names to compute IAA.
    by_label: boolean
        Whether to do the comparison label by label

    Returns
    -------
    iaa_all_vs_all: float
        IAA (pairwise agreement: intersection / union)
    iaa_pairwise: dict
        Contains IAA annotator by annotator
        Keys: annotators compared
        Values; float IAA (pairwise agreement: intersection / union)
    iaa_by_label: dict
        Contains IAA by label. 
        Keys: label
        Values: tuple (iaa_all_vs_all, iaa_pairwise)

    '''
    # Get labels
    labels = []
    for df in list_df:
        labels = labels + df.label.to_list()
    count_labels = Counter(labels)
    labels = set(count_labels.keys())
    
    
    # Extract info from dataframe
    codes,_ = get_codes(list_df, relevant_colnames, labels)
        
    # Compute IAA
    iaa_all_vs_all, iaa_pairwise = compute_iaa(codes, annotator_names)
            
    if by_label == False:
        return iaa_all_vs_all, iaa_pairwise
    
    # In case we want to compute IAA per each label
    iaa_by_label = {}
    for label in labels:
        # Extract info from dataframe
        codes, _ = get_codes(list_df, relevant_colnames, [label])
        # Compute IAA
        iaa_all_vs_all_l, iaa_pairwise_l = compute_iaa(codes, annotator_names)
        
        iaa_by_label[label] = (iaa_all_vs_all_l, iaa_pairwise_l)
    return iaa_all_vs_all, iaa_pairwise, iaa_by_label, count_labels

def get_codes(list_df, relevant_colnames,rel_labels):
    '''
    Extract "codes" from dataframe.
    
    Parameters
    ----------
    list_df : list
        Contains one pandas dataframe per annotator.
    relevant_colnames : list
        List of relevant column names to compute IAA.
    rel_labels : list
        List of relevant values of the "label" column of dataframe.

    Returns
    -------
    codes : list
        Contains sets of codes for each dataframe.
    annotator_names : list
        Contains names of annotators.

    '''
    codes = []
    annotator_names = []
    for df in list_df:
        if df.shape[0] == 0:
            codes.append(set())
            annotator_names.append('empty')
            continue
        codes.append(set(df[relevant_colnames].
                         drop(df[df['label'].isin(rel_labels)==False].index).
                         drop_duplicates(subset = relevant_colnames).
                         agg('|'.join, axis=1).to_list()))
        annotator_names.append(df.annotator.drop_duplicates().to_list()[0])
    
    return codes, annotator_names

def compute_iaa(codes, annotator_names):
    '''
    Compute IAA given the codes and annotator names

    Parameters
    ----------
    codes : list
        Contains sets of codes for each dataframe.
    annotator_names : list
        Contains names of annotators.

    Returns
    -------
    iaa_all_vs_all: float
        IAA (pairwise agreement: intersection / union)
    iaa_pairwise: dict
        Contains IAA annotator by annotator
        Keys: annotators compared
        Values; float IAA (pairwise agreement: intersection / union)

    '''
    
    if len(set.union(*codes)) == 0:
        all_vs_all = 0
    else:
        all_vs_all = len(set.intersection(*codes)) / len(set.union(*codes))
    
    pairwise = {}
    for annotator1, annotations1 in zip(annotator_names, codes):
        for annotator2, annotations2 in zip(annotator_names, codes):
            comparison = (annotator1,annotator2)
            if len(annotations1.union(annotations2)) == 0:
                pairwise[comparison] = 0
                continue
            pairwise[comparison] = (len(annotations1.intersection(annotations2))/
                                    len(annotations1.union(annotations2)))
    
    return all_vs_all, pairwise

