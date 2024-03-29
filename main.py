#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 20 10:56:20 2020

@author: antonio
Compute IAA from several annotators (all vs all and detailed) and for different
labels (all together and per label)
"""
from utils.general_utils import parse_ann, argparser, get_subfolder_names, print_iaa_annotators, output_annotation_tables
from utils.create_disagreement_tsv import create_disagreement_tsv
from compute_iaa import computations
import os

if __name__ == '__main__':
    
    ##### Get inputs #####
    datapath, rel_variables, rel_labels = argparser()
    relevant_colnames = rel_variables.split(',')
    relevant_labels= rel_labels.split(',')

    ##### GET ANN INFORMATION #####
    annotator_paths = sorted(get_subfolder_names(datapath))
    annotator_names = list(map(lambda x: x.split('/')[-1], annotator_paths))

    list_df = []
    for annotator in annotator_paths:
        if 'code' in relevant_colnames:
            list_df.append(parse_ann(annotator, relevant_labels, with_notes=True))
        else:
            list_df.append(parse_ann(annotator, relevant_labels))
    output_annotation_tables(list_df, list(map(lambda x: os.path.join(datapath, x + '.tsv'),
                                               annotator_names)))
    create_disagreement_tsv(list(map(lambda x: os.path.join(datapath, x + '.tsv'),annotator_names)), os.path.join(datapath, 'disagreement.tsv'))
    ##### COMPUTE IAA #####
    (iaa_all_vs_all, iaa_pairwise,
     iaa_by_label, count_labels) = computations(list_df, relevant_colnames,
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
    print_iaa_annotators(annotator_names, iaa_pairwise)
       
        
    print('\n\n')
    print('-----------------------------------------------------------------')
    print('IAA per label:')
    print('-----------------------------------------------------------------')
    for k, v in sorted(iaa_by_label.items()):
        print(k +': '+ str(round(v[0], 3)) + '\t('+ str(count_labels[k]) + ')')
        
    if 'COMPATIBLE_COVID' in iaa_by_label.keys():
        print('\n-----------------------------------------------------------------')
        print('COMPATIBLE_COVID')
        print_iaa_annotators(annotator_names, iaa_by_label['COMPATIBLE_COVID'][1])
    
    if 'NO_COMPATIBLE_COVID' in iaa_by_label.keys():
        print('\n-----------------------------------------------------------------')
        print('NO_COMPATIBLE_COVID')
        print_iaa_annotators(annotator_names, iaa_by_label['NO_COMPATIBLE_COVID'][1])
        
    if 'NO_SE_DESCARTA_COVID' in iaa_by_label.keys():
        print('\n-----------------------------------------------------------------')
        print('NO_SE_DESCARTA_COVID')
        print_iaa_annotators(annotator_names, iaa_by_label['NO_SE_DESCARTA_COVID'][1])
        
    if 'NORMAL' in iaa_by_label.keys():
        print('\n-----------------------------------------------------------------')
        print('NORMAL')
        print_iaa_annotators(annotator_names, iaa_by_label['NORMAL'][1])
    
    
    print('\n')
