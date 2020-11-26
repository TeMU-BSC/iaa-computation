#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 20 09:34:46 2020

@author: antonio
"""
import pandas as pd

def create_disagreement_tsv(path1, path2, outpath):
    df1 = pd.read_csv(path1, sep='\t', header=0)
    df1 = df1.drop(['mark'], axis=1)
    
    df2 = pd.read_csv(path2, sep='\t', header=0)
    df2 = df2.drop(['mark'], axis=1)
    
    aux = pd.merge(df1, df2, how='outer', on=['filename', 'label', 'offset', 'span'])
    aux[aux.isnull().any(axis=1)].sort_values(by=['filename','span']).\
        to_csv(outpath, sep='\t', header=True, index=False)
