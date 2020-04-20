#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 28 12:29:08 2020

@author: antonio
"""
import argparse
import os
import pandas as pd

def argparser():
    '''
    DESCRIPTION: Parse command line arguments
    '''
    
    parser = argparse.ArgumentParser(description='process user given parameters')
    parser.add_argument("-a1", "--path1", required = True, dest = "path1", 
                        help = "absolute path to brat directory. Within it, "+
                        "we must have one folder per annotator. With all " +
                        "the annotated files directly in the folder")
    parser.add_argument("-v", "--variables", required = False, dest = "variables", 
                        default = 'filename,code',
                        help = "Comma separated names of columns of interest to compute IAA")    
    parser.add_argument("-l", "--labels", required = False, dest = "labels", 
                        default = 'MORFOLOGIA_NEOPLASIA',
                        help = "Comma separated names of relevant labels")    
    
    args = parser.parse_args()
    
    return args.path1, args.variables, args.labels


def parse_ann(datapath):
    '''
    DESCRIPTION: parse information in .ann files.
    
    Parameters
    ----------
    datapath: str. 
        Route to the folder where the files are. 
           
    Returns
    -------
    df: pandas DataFrame 
        It has information from ann files. Columns: 'annotator', 'filename',
        'mark', 'label', 'offset', span', 'code'
    filenames: list 
        list of filenames
    '''
    info = []
    ## Iterate over the files and parse them
    filenames = []
    for root, dirs, files in os.walk(datapath):
         for filename in files:
             if filename[-3:] != 'ann':
                 continue # get only ann files
             #print(os.path.join(root,filename))
             info, filenames = parse_one_ann(info, filenames, root, filename)

    # Save parsed .ann files
    df = pd.DataFrame(info, columns=['annotator', 'filename', 'mark', 'label',
                                     'offset', 'span', 'code'])
    
    return df, filenames

def parse_one_ann(info, filenames, root, filename):
    '''
    DESCRIPTION: parse information in one .ann file.
    
    Parameters
    ----------
           
    Returns
    -------
    
    '''
    f = open(os.path.join(root,filename)).readlines()
    filenames.append(filename)
    # Get annotator and bunch
    annotator = root.split('/')[-1]
    
    # Parse .ann file
    mark2code = {}
    for line in f:
        if line[0] != '#':
            continue
        line_split = line.split('\t')
        mark2code[line_split[1].split(' ')[1]] = line_split[2].strip()
            
    for line in f:
        if line[0] != 'T':
            continue
        splitted = line.split('\t')
        if len(splitted)<3:
            print('Line with less than 3 tabular splits:')
            print(root + filename)
            print(line)
            print(splitted)
        if len(splitted)>3:
            print('Line with more than 3 tabular splits:')
            print(root + filename)
            print(line)
            print(splitted)
        mark = splitted[0]
        label_offset = splitted[1]
        label = label_offset.split(' ')[0]
        offset = ' '.join(label_offset.split(' ')[1:])
        span = splitted[2].strip()
        if mark in mark2code.keys():
            code = mark2code[mark]
            info.append([annotator, filename, mark, label,
                         offset, span, code])
            
    return info, filenames
    