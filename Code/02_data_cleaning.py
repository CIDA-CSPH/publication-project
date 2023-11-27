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
pub_file_list = glob.glob('./DataRaw/Publications/*.csv')

## read publication data
columns = ['CIDA member','article_title', 'pub_year', 'num_citations', 'journal', 'author', 'abstract',]
def merge_to_one(file_list,columns_name,to_file):
    pd.DataFrame(columns=columns_name).to_csv(to_file, index= False)
    for i in range(len(file_list)):
        try:
            author_name = file_list[i].split('\\')[-1].replace(' publications.csv','')
            df = pd.read_csv(file_list[i], encoding='utf8')
            df['CIDA member'] = author_name
            df = df.iloc[:,[-1,0,1,2,3,4,5]]
            df.to_csv(to_file, mode='a', index= False, header=False)
        except:
            continue


merge_to_one(pub_file_list,columns, './DataRaw/CIDA members publication.csv')

