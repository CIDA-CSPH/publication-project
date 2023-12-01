from pymed import PubMed
import os
import tqdm
import pandas as pd
tqdm.pandas()
import datetime

working_directory = r'C:\Users\zhushu\OneDrive\Graduate File\CIDA RA\publication project'
os.chdir(working_directory)
name = 'Christopher A Mancuso'
now = datetime.datetime.now().strftime('%Y/%m/%d')
myquery = '('+ name +'[Author]) AND (("2017/01/01"[Date - Publication] : "'+ now+'"[Date - Publication]))'
pubmed = PubMed(tool="MyTool",email="chirstopher.a.mancuso@cuanschutz.edu")
results = pubmed.query(myquery, max_results=500)
article_list =  []

for article in results:
    a = article.toDict()
    article_list.append([a.get('title'), a.get('publication_date'), a.get('journal'), a.get('authors'), a.get('abstract')])

columns_names = ['article_title', 'pub_year', 'journal', 'author', 'abstract' ]

pd.DataFrame(article_list, columns=columns_names).to_excel(r'./DataRaw/PubMed/'+name+' PubMed.xlsx',index=False)