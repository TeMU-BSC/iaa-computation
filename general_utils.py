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
                        help = "absolute path to annotated brat files from annotator 1")
    parser.add_argument("-a2", "--path2", required = True, dest = "path2", 
                        help = "absolute path to annotated brat files from annotator 2")
    parser.add_argument("-v", "--variables", required = False, dest = "variables", 
                        default = ['filename', 'code'],
                        help = "absolute path to annotated brat files from annotator 2")    
    
    args = parser.parse_args()
    
    return args.path1, args.path2, args.variables


def parse_ann(datapath, output_path):
    '''
    DESCRIPTION: parse information in .ann files.
    
    Parameters
    ----------
    datapath: str. 
        Route to the folder where the files are. 
    output_path: str. 
        Path to output TSV where information will be stored.
           
    Returns
    -------
    df: pandas DataFrame 
        It has information from ann files. Columns: 'annotator', 'bunch',
        'filename', 'mark', 'label', 'offset1', 'offset2', 'span', 'code'
    filenames: list 
        list of filenames
    '''
    info = []
    ## Iterate over the files and parse them
    filenames = []
    for root, dirs, files in os.walk(datapath):
         for filename in files:
             if filename[-3:] == 'ann': # get only ann files
                 #print(os.path.join(root,filename))
                 
                 f = open(os.path.join(root,filename)).readlines()
                 filenames.append(filename)
                 # Get annotator and bunch
                 annotator = root.split('/')[-1]
                 
                 # Parse .ann file
                 mark2code = {}
                 for line in f:
                     if line[0] == '#':
                         line_split = line.split('\t')
                         mark2code[line_split[1].split(' ')[1]] = line_split[2].strip()
                         
                 for line in f:
                     if line[0] == 'T':
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

    # Save parsed .ann files
    df = pd.DataFrame(info, columns=['annotator', 'filename', 'mark', 'label',
                                     'offset', 'span', 'code'])
    #df.to_csv(output_path, sep='\t',index=False)
    
    return df, filenames