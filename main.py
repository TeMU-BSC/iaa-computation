#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 20 10:56:20 2020

@author: antonio
Compute IAA from several annotators (all vs all and detailed) and for different
labels (all together and per label)
"""
from general_utils import parse_ann, argparser
from compute_iaa import filter_pandas, compute_iaa

if __name__ == '__main__':
    
    ##### Get inputs #####
    path_annot1, path_annot2, rel_variables, rel_labels = argparser()
    relevant_colnames = rel_variables.split(',')
    relevant_labels= rel_labels.split(',')

    ##### GET ANN INFORMATION #####
    df1, _ = parse_ann(path_annot1)
    df2, _ = parse_ann(path_annot2)
    
    ##### FILTER OUT LABELS NOT RELEVANT #####
    df1 = filter_pandas(df1, 'label', relevant_labels)
    df2 = filter_pandas(df2, 'label', relevant_labels)

    ##### COMPUTE IAA #####
    print('-----------------------------------------------------------------')
    print('IAA taking into account {}'.format(rel_variables))
    print('-----------------------------------------------------------------')
    print(round(compute_iaa(df1, df2, relevant_colnames),3))