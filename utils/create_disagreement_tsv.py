#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 20 09:34:46 2020

@author: antonio
"""
import pandas as pd

def create_disagreement_tsv(paths_list, outpath):
    df1 = pd.read_csv(paths_list[0], sep='\t', header=0)
    df1 = df1.drop(['mark'], axis=1)
    
    df2 = pd.read_csv(paths_list[1], sep='\t', header=0)
    df2 = df2.drop(['mark'], axis=1)
    
    aux = pd.merge(df1, df2, how='outer', on=['filename', 'label', 'offset', 'span'])
    aux[['offset1', 'offset2']] = aux.offset.str.split(" ",expand=True,).astype(int)
    
    if len(paths_list)==2:
        aux[aux.isnull().any(axis=1)].sort_values(by=['filename','offset1']).\
            drop(['offset1', 'offset2'], axis=1).\
            to_csv(outpath, sep='\t', header=True, index=False)
    elif len(paths_list)==3:
        df3 = pd.read_csv(paths_list[2], sep='\t', header=0)
        df3 = df3.drop(['mark'], axis=1)
        
        aux2 = pd.merge(aux, df3, how='outer', on=['filename', 'label', 'offset', 'span'])
        aux2[aux2.isnull().any(axis=1)].sort_values(by=['filename','span']).\
            to_csv(outpath, sep='\t', header=True, index=False)
    else:
        Exception("We only accept 2 or 3 TSVs")