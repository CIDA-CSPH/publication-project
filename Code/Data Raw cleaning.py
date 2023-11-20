import pandas as pd
import json
import pickle
import glob
import os


working_directory = r'C:\Users\zhushu\OneDrive\Graduate File\CIDA RA\publication project'
os.chdir(working_directory)
from_file_path = glob.glob(os.path.abspath(r'./DataRaw/Citedby/')+'\\*.pickle' )


def dict_to_df(article_name, citedby):
    list_citedby = [citedby[list(citedby.keys())[i]]['bib'] for i in range(len(citedby))]
    [list_citedby[i].pop('venue', None) for i in range(len(list_citedby))]
    df = pd.DataFrame.from_dict(list_citedby)
    df['article_name'] = article_name
    df = df.iloc[:,[4,0,1,2,3]]
    return df

for i in from_file_path:
    member_name = i.split('\\')[-1].replace('.pickle','')
    to_file_path = r'./DataProcessed/' + member_name+'.csv'
    with open(i,'rb') as file:
        data = pickle.load(file)

    cols_name = ['article_name', 'citedby.title', 'citedby.author', 'citedby.pub_year', 'citedby.abstract']
    pd.DataFrame(columns=cols_name).to_csv(to_file_path,header=True,index=False)



    for i in range(len(data)):
        article_name = list(data.keys())[i]
        df = dict_to_df(article_name, data[article_name])
        df.to_csv(to_file_path, header=False, index=False, mode='a')
        
