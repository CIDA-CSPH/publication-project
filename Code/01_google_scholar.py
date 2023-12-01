'''
Author: Shuai Zhu
Date: 11/14/2023
Description: Requesting the publications cited  from google scholar using scholarly package. 

'''





from scholarly import scholarly
from scholarly import MaxTriesExceededException
import pandas as pd
import os
import requests
from tqdm import tqdm


### read member name
working_directory = r'C:\Users\zhushu\OneDrive\Graduate File\CIDA RA\publication project'
os.chdir(working_directory)


def set_proxy(n):
    list_proxy_address = []
    with open('./Code/Webshare 100 proxies.txt') as file:
        line = file.readlines()
    for i in line:
        proxy = i.replace('\n','').split(':')
        proxy_address = 'http://'+ proxy[2]+':'+proxy[3]+'@'+proxy[0]+':'+proxy[1]
        list_proxy_address.append(proxy_address)

 
    os.environ['http_proxy'] = list_proxy_address[n]
    os.environ['HTTP_PROXY'] = list_proxy_address[n]
    os.environ['https_proxy'] = list_proxy_address[n]
    os.environ['HTTPS_PROXY'] = list_proxy_address[n]
    print('Changing ip to: ', list_proxy_address[n])
    print('Current ip is: ', requests.get('https://api.ipify.org').text)

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


def checkip():
    re = requests.get('http://checkip.dyndns.org/')
    return re.text

n = 5
count = 0
set_proxy(n)

def get_filled_pub(pub):
    global n
    try:
        filled_pub = scholarly.fill(pub)
    except MaxTriesExceededException:
        print('Max tries')
        set_proxy(n)
        n = n+1
        filled_pub = get_filled_pub(pub)
    return filled_pub



def get_publications(author):

    global n
    global count
    publications = [author['publications'][i] for i in range(len(author['publications']))]
    list_filled_pub = []

    for i in tqdm(range(len(publications))):
        filled_publication = get_filled_pub(publications[i])
        list_filled_pub.append(filled_publication)
        count = count+1
        if count >=100:
            n = n+1
            set_proxy(n)
            count =0


    author = [i['bib'].get('author') for i in list_filled_pub]
    article_title = [i['bib'].get('title') for i in list_filled_pub]
    pub_year = [i['bib'].get('pub_year') for i in list_filled_pub ]
    journal = [i['bib'].get('journal') for i in list_filled_pub ]
    num_citations = [i['num_citations'] for i in list_filled_pub]
    abstract = [i['bib'].get('abstract') for i in list_filled_pub]


    df = pd.DataFrame({
            "article_title" : article_title,
            "pub_year" : pub_year,
            "num_citations" : num_citations,
            'journal': journal,
            'author':author,
            'abstract':abstract
            })

    return df    


# def get_citedby(author_name,id):

#     author = scholarly.search_author_id(id)
#     author = scholarly.fill(author)
#     df_publictation = get_publications(author)
#     df_publictation.to_csv(r'./DataRaw/Publications/'+author_name+' publications.csv',index = False)
#     start_year = 2017
    
#     for i in tqdm(range(0,len(author['publications']))):
#         try:
#             if (int(author['publications'][i]['bib']['pub_year'])>=start_year) & (author['publications'][i]['num_citations']!=0):
#                 pub = scholarly.fill(author['publications'][i])
#                 citedby = pull_citeby_article(pub)
#                 citedby = {i['bib']['title']:i for i in citedby}
#                 citedby = { pub['bib']['title']:citedby }
#                 dict_citedby.update(citedby)
#                 with open(r'./DataRaw/Citedby/' + author_name+'.pickle', 'wb') as file:
#                     pickle.dump(dict_citedby, file, protocol=pickle.HIGHEST_PROTOCOL)
#         except Exception as e1:
#             print(e1)
#             continue

def _init_():

    global n
    df_member = pd.read_excel(r"./DataProcessed/PERSONEL ROSTER for CIDA and B&I-NEC.xlsx")
    df_member.drop_duplicates(subset = ['Last Name', 'First Name'],inplace = True)
    list_name =  df_member['First Name'] +' '+ df_member['Last Name'].str.split('-').str[0]
    # df_member['author_id'] = [authorid_request(i) for i in list_name]
    # df_member.to_csv("./DataProcessed/CIDA's Members.csv",index = False)


    for i in range(33,len(df_member)):

        if pd.isna(df_member['author_id'][i]):
            continue
        else:
            id = df_member['author_id'][i]
            name = list_name[i]
            print(name)
            author = scholarly.search_author_id(id)
            author = scholarly.fill(author)
            df_publictation = get_publications(author)
            df_publictation.to_excel(r'./DataRaw/Publications/'+name+' publications.xlsx',index = False)


_init_()


