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
    parser.add_argument("-d", "--datapath", required = True, dest = "path1", 
                        help = "absolute path to brat directory. Within it, "+
                        "we must have one folder per annotator. With all " +
                        "the annotated files directly in the folder")
    parser.add_argument("-v", "--variables", required = False, dest = "variables", 
                        default = 'filename,label',
                        help = "Comma separated names of columns of interest to compute IAA")    
    parser.add_argument("-l", "--labels", required = False, dest = "labels", 
                        default = 'MORFOLOGIA_NEOPLASIA',
                        help = "Comma separated names of relevant labels")    
    
    args = parser.parse_args()
    
    return args.path1, args.variables, args.labels


def parse_ann(datapath, relevant_labels, with_notes=False):
    '''
    DESCRIPTION: parse information in .ann files.
    
    Parameters
    ----------
    datapath: str. 
        Route to the folder where the files are. 
    relevant_labels: list
        List of annotation labels I am parsing
           
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
             
             info, filenames = parse_one_ann(info, filenames, root, filename,
                                             relevant_labels, ignore_related=True,
                                             with_notes=with_notes)

    # Save parsed .ann files
    if with_notes == True:
        df = pd.DataFrame(info, columns=['annotator', 'filename', 'mark',
                                         'label','offset', 'span', 'code'])
    else:
        df = pd.DataFrame(info, columns=['annotator', 'filename', 'mark',
                                         'label','offset', 'span'])
    
    #return df, filenames
    return df


def parse_one_ann(info, filenames, root, filename, relevant_labels,
                  ignore_related=False, with_notes=False):
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
    related_marks = []     
    if ignore_related == True:   
        # extract relations
        for line in f:
            if line[0] != 'R':
                continue
            related_marks.append(line.split('\t')[1].split(' ')[1].split(':')[1])
            related_marks.append(line.split('\t')[1].split(' ')[2].split(':')[1])
            
    mark2code = {}
    if with_notes == True:
        # extract notes
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
            print(os.path.join(root, filename))
            print(line)
            print(splitted)
        if len(splitted)>3:
            print('Line with more than 3 tabular splits:')
            print(os.path.join(root, filename))
            print(line)
            print(splitted)
        mark = splitted[0]
        if mark in related_marks:
            continue
        label_offset = splitted[1]
        label = label_offset.split(' ')[0]
        if label not in relevant_labels:
            continue
        offset = ' '.join(label_offset.split(' ')[1:])
        span = splitted[2].strip()
        
        if with_notes == False:
            info.append([annotator, filename, mark, label,
                         offset, span])
            continue
        
        if mark in mark2code.keys():
            code = mark2code[mark]
            info.append([annotator, filename, mark, label,
                         offset, span, code])
            
    return info, filenames


def get_subfolder_names(path):
    '''
    From https://stackoverflow.com/questions/800197/how-to-get-all-of-the-immediate-subdirectories-in-python
    '''
    
    return [f.path for f in os.scandir(path) if f.is_dir()]

    
def print_iaa_annotators(annotator_names, iaa_pairwise):
    '''
    Print IAA pairwise in a pretty way
    '''
    # Make sure iaa_pairwise and annotator_names have same order
    first_key = [k[0] for k, v in iaa_pairwise.items()]
    if first_key != sorted(first_key):
        print('Cannot display pretty pairwise information due to unknown '+
              'sorting error. We proceed to display it in non-pretty way')
        print(iaa_pairwise)
        return
    # Print
    c = 0
    print(*([''] + annotator_names), sep='\t', end='')
    first_ann_old = ''
    for k, v in iaa_pairwise.items():
        first_ann = k[0]
        if first_ann != first_ann_old:
            print('\n')
            print(first_ann, end='')
            first_ann_old = first_ann
            c = 0
        c = c + 1
        print('\t', end='')
        print(str(round(v, 3)), end='')
        
def output_annotation_tables(list_df, outpaths):
    '''
    DESCRIPTION: output pandas DataFrames with annotations to TSV file
    
    Parameters
    ----------
    list_df: list
        List with annotation Dataframes. One Dataframe per annotator
    outpaths: list
        List with output paths. One path per annotation
           
    Returns
    -------
    
    '''
    for df,path in zip(list_df, outpaths):
        df.to_csv(path, sep='\t', index=False)
        