from koya_utilities import get_stats, value_counts_pct, get_general_changes
from koya_python_airtable import airtable_download, convert_to_dataframe, upload_pandas_dataframe

import pandas as pd
import boto3
import datetime
import sys
import re
from io import StringIO
import itertools

def test_columns(client_cols,koya_cols,test_level='client_match',verbose=False):
    '''
    client_cols: the columns in the client dataset
    
    koya_cols: the columns in the koya dataset
    
    test_level: 'inner' means that all the columns have to be common
                'client' means that all the columns on the client side need to be present on the koya table
                'outer' means that it can be columns in client that are not in koya
                
    verbose: if it should print values
    '''
    
    only_client=set(client_cols) - set(koya_cols)
    if verbose:    
        print('columns only in client:\n')
        for p in only_client:
            print(p)
        
    only_koya = set(koya_cols) - set(client_cols)
    if verbose:
        print('\ncolumns only in koya:\n')
        for p in only_koya:
            print(p)
        
    common = set(client_cols).intersection(koya_cols)
    if verbose:
        print('\ncolumns in common:\n')
        for p in common:
            print(p)
        
    if test_level=='inner':
        assert len(only_client) == len(only_koya) == 0

    elif test_level=='client_match':
        if len(only_client) != 0:
            raise ValueError(f'the follow columns are only present in client: {only_client}')
        
        
    return 0

def test_unique_key(data,key):
    
    if data[key].duplicated().sum()!=0:
        raise ValueError(f'there are duplicated values in the key: {key}')
        
    if data[key].isnull().sum()!=0:
        raise ValueError(f'there are null values in the key: {key}')
        
    return 0

def test_not_null_pct(data
                  ,columns=['SKU','Product Name','Canoa - Sub-Category','Product Description']
                  ,threshold=1):
    
    '''
    data: the pandas dataframe
    
    columns: the columns to test
    
    threshold: the value for the threshold that should be meet in order to not raise an error. Values from 0 to 1, with 1 meaning 100%
    '''
    
    stats=get_stats(data)
    aux=stats[stats['col'].isin(columns)]
    aux=aux[aux['not_null_pct']<threshold]

    if len(aux)>0:
        values_dict = aux[['col','not_null_pct']].set_index('col').to_dict()['not_null_pct']
        raise ValueError(f"columns that don't meet the threshold of {threshold}: {values_dict}")
        
    return 0
    
def test_main(profile_name = 'koya-mendes'
         ,client_project_name = 'koya-canoa'
         ,source = 'hem'
         ,context='aws'
         ,use_latest=True
         ,date=None
         ,table="NEW TAB"
         ,api_key='env'
         ,base_id='appy4rqg1s2CVflRF'
         ,test_level='client_match'
         ,tests=['columns','key','not_null_pct']
         ,key='SKU'
         ,cols_not_null = ['SKU','Product Name','Canoa - Sub-Category','Product Description']
         ,threshold = 1
         ,verbose=False):
    
    # koya = load_data(profile_name,client_project_name,source,context,use_latest,date)
    
    # if 'columns' in tests:
    #     client = load_template(table,api_key,base_id)
    #     result_cols = compare_columns(client.columns,koya.columns,test_level=test_level,verbose=verbose)
        
    # if 'key' in tests:
    #     result_key = test_unique_key(koya,key)
        
    # if 'not_null_pct' in tests:
    #     test_not_null_pct(koya,columns=cols_not_null,threshold=threshold)
    
    # return result

    return None