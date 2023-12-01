from scholarly import scholarly
from scholarly import MaxTriesExceededException
import pandas as pd
import os
import requests
from tqdm import tqdm


working_directory = r'C:\Users\zhushu\OneDrive\Graduate File\CIDA RA\publication project'
os.chdir(working_directory)


def get_author_id(name):
    search_query = scholarly.search_author(name)
    first_author_result = next(search_query)
    return first_author_result['scholar_id']

def authorid_request(name):
    try:
        authorid = get_author_id(name)
        return authorid
    except Exception as e1:
        try:
            authorid = get_author_id(name+' anschutz')
            return authorid
        except Exception:
            return None


df = pd.read_excel(r'./DataProcessed/PERSONEL ROSTER for CIDA and B&I-NEC.xlsx')
df_tail = df[df['author_id'].isna()]
df_tail['name'] =  df_tail['First Name']+' ' + df_tail['Last Name']
author_id = df_tail['name'].apply(lambda x: authorid_request(x))

df_tail['author_id'] = author_id
df_tail.to_excel('temp.xlsx',index=False)