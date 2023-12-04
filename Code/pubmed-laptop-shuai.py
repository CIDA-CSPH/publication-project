from pymed import PubMed
import requests
import os
tqdm.pandas()
working_directory = r'C:\Users\zhushu\OneDrive\Graduate File\CIDA RA\publication project'
os.chdir(working_directory)

def get_abstract(title):

    myquery = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&retmode=json&retmax=20&sort=relevance&term='+requests.utils.quote(title)
    
    res = requests.get(url=myquery)
    res_json = res.json()
    try:
        id = res_json['esearchresult']['idlist'][0]
        pubmed = PubMed(tool="MyTool")
        results = pubmed.query(id, max_results=500)
    
        for article in results:
            article_id = article.pubmed_id
            title = article.title
            publication_date = article.publication_date
            abstract = article.abstract
            a = [article_id, title, article.publication_date, abstract]
            df = pd.DataFrame([a], columns = ['article_id', 'title','publication_date', 'abstract'])
            break
        return a
    except Exception as e1:
        print(e1)
        return None

def string_clean(series_string):
    dict_repalce = {".": "", "[": "","]":"" , "—":"-"}
    for word, initial in dict_repalce.items():
        series_string = series_string.str.replace(word.lower(), initial)
    return series_string.str.strip().str.lower().str.split(' ').str[0:3]

read_file = r'DataProcessed\Nichole Carlson.csv'
df_citedby = pd.read_csv(read_file)
b = df_citedby['citedby.title'].progress_apply(get_abstract)
index = b[b.notna()].index
df_abstract = pd.DataFrame(b[b.notna()].to_list(),columns = ['article_id', 'title','publication_date', 'abstract']).set_index(index)
df_merged = df_citedby.merge(df_abstract,how = 'left',left_index = True, right_index = True)
df_merged['same'] = (string_clean(df_merged['citedby.title'])== string_clean(df_merged['title']))
df_merged['citedby.abstract'] = df_merged.apply(lambda x:x['abstract'] if x['same']==True else x['citedby.abstract'] , axis = 1  )
df_merged.rename(columns = {'same':'full_abstract'},inplace = True)


os.remove(read_file)
df_merged.iloc[:,[0,1,2,3,4,-1]].to_excel(read_file.replace('csv','xlsx'),index = False)



from pymed import PubMed
# myquery = 'Christopher A Mancuso[Author]'
myquery = '(Christopher A Mancuso[Author]) AND (("2017/01/01"[Date - Publication] : "2023/09/01"[Date - Publication]))'
pubmed = PubMed(tool="MyTool",email="chirstopher.a.mancuso@cuanschutz.edu")
results = pubmed.query(myquery, max_results=500)
for article in results:
    print(article.toJSON())