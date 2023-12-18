from pymed import PubMed
import os

from tqdm import tqdm
import pandas as pd
tqdm.pandas()
import datetime

working_directory = r'C:\Users\zhushu\OneDrive\Graduate File\CIDA RA\publication project'
os.chdir(working_directory)

def get_pubmed(name,email):

    now = datetime.datetime.now().strftime('%Y/%m/%d')
    myquery = '('+ name +'[Author]) AND (("2017/01/01"[Date - Publication] : "'+ now+'"[Date - Publication]))'
    pubmed = PubMed(tool="MyTool",email=email)
    results = pubmed.query(myquery, max_results=500)
    article_list =  []

    for article in results:
        a = article.toDict()
        article_list.append([a.get('title'), a.get('publication_date'), a.get('journal'), a.get('authors'), a.get('abstract')])

    columns_names = ['article_title', 'pub_year', 'journal', 'author', 'abstract' ]

    df_res = pd.DataFrame(article_list, columns=columns_names)
    df_res.to_excel(r'./DataRaw/PubMed/'+name+' PubMed.xlsx',index=False)
    return df_res

### 
df = pd.read_excel('./DataRaw/Team member list.xlsx',names=['name','email','title'])
for i in tqdm(range(len(df))):
    name = df.iloc[i,0]
    email = df.iloc[i,1]
    get_pubmed(name,email)
# get_pubmed('Alex Kaizer', 'alex.kaizer@cuanschutz.edu').to_excel(r'./DataRaw/PubMed/'+name+' PubMed.xlsx',index=False)