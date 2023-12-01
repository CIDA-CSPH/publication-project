'''
Author: Shuai Zhu
Date: 11/20/2023
Description: merge publication files to one file

'''
import pandas as pd
import glob
import os

## set the working directory
working_directory = r'C:\Users\zhushu\OneDrive\Graduate File\CIDA RA\publication project'
os.chdir(working_directory)

## list files
pub_file_list = glob.glob('./DataRaw/Publications/*.xlsx')

## read publication data
def merge_to_one(file_list):
    df_concat = pd.DataFrame()
    for i in range(len(file_list)):
        author_name = file_list[i].split('\\')[-1].replace(' publications.xlsx','')
        df = pd.read_excel(file_list[i])
        df['CIDA_member'] = author_name
        df = df.iloc[:,[-1,0,1,2,3,4,5]]
        df_concat = pd.concat([df_concat,df],axis=0, ignore_index=True)
    return df_concat



merge_to_one(pub_file_list).to_excel(r'./DataRaw/CIDA members google publication.xlsx',index=False)

