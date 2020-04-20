#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 20 10:56:20 2020

@author: antonio
Compute IAA from several annotators (all vs all and detailed) and for different
labels (all together and per label)
"""
from general_utils import parse_ann, argparser, get_subfolder_names
from compute_iaa import computations

if __name__ == '__main__':
    
    ##### Get inputs #####
    datapath, rel_variables,_ = argparser()
    relevant_colnames = rel_variables.split(',')
    #relevant_labels= rel_labels.split(',')

    ##### GET ANN INFORMATION #####
    annotator_paths = get_subfolder_names(datapath)
    annotator_names = list(map(lambda x: x.split('/')[-1], annotator_paths))

    list_df = []
    for annotator in annotator_paths:
        list_df.append(parse_ann(annotator))
    
    ##### COMPUTE IAA #####
    (iaa_all_vs_all, iaa_pairwise,
     iaa_by_label) = computations(list_df, relevant_colnames,
                                  annotator_names, by_label=True)
    
    ###### PRINT ######
    print('_________________________________________________________________')
    print('\nIAA taking into account {}'.format(rel_variables))
    print('_________________________________________________________________')
    print('\n\n')
    print('-----------------------------------------------------------------')
    print('1. IAA all vs all')
    print('-----------------------------------------------------------------')
    print(round(iaa_all_vs_all,3))
    print('\n\n')
    print('-----------------------------------------------------------------')
    print('IAA different annotators:')
    print('-----------------------------------------------------------------')
    # TODO: print_iaa_annotators(annotator_paths, iaa_pairwise)
       
        
    print('\n\n')
    print('-----------------------------------------------------------------')
    print('IAA per label:')
    print('-----------------------------------------------------------------')
    for k, v in iaa_by_label.items():
        print(k +': '+ str(round(v[0], 3)))
        