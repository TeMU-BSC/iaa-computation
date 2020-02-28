#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 19 13:00:10 2020

@author: antonio
"""

from general_utils import parse_ann, argparser

def compute_iaa(df1, df2, relevant_colnames):
    df1_codes = df1[relevant_colnames].drop_duplicates(subset = relevant_colnames)
    df2_codes = df2[relevant_colnames].drop_duplicates(subset = relevant_colnames)
    df1_fc = set(df1_codes.apply('|'.join, axis=1).tolist())
    df2_fc = set(df2_codes.apply('|'.join, axis=1).tolist())
    
    return len(df1_fc.intersection(df2_fc)) / len(df1_fc.union(df2_fc))



if __name__ == '__main__':
    
    path_annot1, path_annot2, relevant_colnames = argparser()

    df1, filenames1 = parse_ann(path_annot1, '')
    df2, filenames2 = parse_ann(path_annot2, '')
    
    print('-----------------------------------------------------------------')
    print('IAA taking into account {}'.format(relevant_colnames))
    print('-----------------------------------------------------------------')
    print(round(compute_iaa(df1, df2, relevant_colnames),3))