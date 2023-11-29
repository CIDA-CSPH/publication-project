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
        
df_member = pd.read_excel(r'./DataRaw/PERSONEL ROSTER for CIDA and B&I-NEC.xlsx',skiprows=1)
df_member.drop_duplicates(subset=['Empl ID', 'Last Name','First Name'], inplace=True)
df_member['Last Name'] = df_member['Last Name'].str.split('-').str[0]

df_merged = df_member.merge(pd.read_excel(r"./DataProcessed/CIDA's Members.xlsx").loc[:,['Last Name', 'First Name','author_id']], how='left', on=['Last Name', 'First Name'])
# df_merged = df_merged.loc[:,['Empl ID','Last Name','First Name','author_id']]
df_merged.to_excel("./DataProcessed/PERSONEL ROSTER for CIDA and B&I-NEC.xlsx",index=False)
