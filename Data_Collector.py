import pandas as pd
from Lda_func import lda_func
import matplotlib.pyplot as plt
from BOW_maker import bow_dict_lists, bow_dict_strings, bow_dict_dicts
from word_counter import w_counter
import networkx as nx
import matplotlib.pyplot as plt

from Stop_w import stop_word

test_string = '''fail test what knowledge IoT fail test compromise knowledge context compromise fail test knowledge it IT AI fail test IoT IoT'''
stop_words = ['web', 'intelligence', 'based', '/', ',', 'data', 'international', 'conference', 'paper', 'using', 'information', 'ï', 'ò', 'δ', '≥']

#reading the data set and croping out the part we are intrested in (2013-2020)
file_name = 'WI-Data.xlsx'
sheet_names = ("Sheet1", "Lab 1 - Web Intelligence Public")
xl_file = pd.ExcelFile(file_name)
df_1 = pd.read_excel(xl_file, sheet_names[0])
df_2 = pd.read_excel(xl_file, sheet_names[1])
columns_names = [i for i in df_2.columns]
year_filter = (df_2['Year'] > 2012)
data_13_20 = df_2.loc[year_filter]

#country affiliations
dis_affil = {}
country_affil = {}
affil = data_13_20['Affiliations']
for k, af_list in enumerate(affil):
    if type(af_list) == str:
        af_list = af_list.split(';')
        country_affil[k] = []
        dis_affil[k] = []
        for af in af_list:
            #country is on last index, discipline is on first
            af = af.split(',')
            country = af[-1]
            discipline = af[0]
            country_affil[k].append(country)
            dis_affil[k].append(discipline)
    else:
        pass
print(country_affil)
countries = {}
for k, v in country_affil.items():
    #removing duplicates of countries
    coutry_set = set()
    for j in v:
        coutry_set.add(j)
    countries[k] = list(coutry_set)
visualisation_table = {}
for k,v in countries.items():
    conutry_to_country = []
    visualisation_table[k] = []
    if len(v) > 1:
        i = 0
        for c in v:
            for _ in range(len(v)):
                if c != v[i]:
                    #creating table idx, country, country
                    conutry_to_country.append(c)
                    conutry_to_country.append(v[i])
                    conutry_to_country = sorted(list(conutry_to_country))
                    if conutry_to_country not in visualisation_table[k]:
                        visualisation_table[k].append(conutry_to_country.copy())
                i += 1
                conutry_to_country.clear()
            else:
                i = 0
vt_copy = visualisation_table.copy()
for k,v in vt_copy.items():
    if len(v) == 0:
        del visualisation_table[k]
network_table = {}
i = 0
for k,v in visualisation_table.items():
    for c_to_c in v:
        network_table[i] = c_to_c
        i+=1
for k,v in network_table.items():
    network_table[k] = sorted(v)
network_df = pd.DataFrame(network_table)
network_df = network_df.transpose()
network_df.columns = ['c1', 'c2']
plt.figure(figsize=(12, 12))
g = nx.from_pandas_edgelist(network_df, source='c1', target='c2')
nx.draw_networkx(g)
plt.show()


#abstract
abstract_words = data_13_20['Abstract']
abs_dict = {}
for i, words in enumerate(abstract_words):
    if type(words) == str:
        words = words.replace(';', '')
        words = stop_word(words, stop_words)
        abs_dict[i] = words
    else:
        pass

#keywords
a_keywords_dict = {}
ak_words = data_13_20['Author Keywords']
for k, words in enumerate(ak_words):
    if type(words) == str:
        words = words.replace(';', '')
        words = stop_word(words, stop_words)
        a_keywords_dict[k] = words
    else:
        pass

id_keywords_dict = {}
idk_words = data_13_20['Index Keywords']
for k, words in enumerate(idk_words):
    if type(words) == str:
        words = words.replace(';', '')
        words = stop_word(words, stop_words)
        id_keywords_dict[k] = words
    else:
        pass

#Titles
titles_dict = {}
for k, v in enumerate(data_13_20['Title']):
    v = v.lower()
    v = stop_word(v, stop_words)
    titles_dict[k] = v

#word cloud
with open('titles.txt', 'w+') as t:
    t.write(bow_dict_strings(titles_dict))
with open('abstract.txt', 'w+') as t:
    t.write(bow_dict_strings(abs_dict))
with open('author_keywords.txt', 'w+') as t:
    t.write(bow_dict_strings(a_keywords_dict))
with open('index_keywords.txt', 'w+') as t:
    t.write(bow_dict_strings(id_keywords_dict))
with open('countries.txt', 'w+') as t:
    t.write(bow_dict_lists(country_affil))


lda_func(bow_dict_strings(titles_dict), 'Titles')
lda_func(bow_dict_strings(a_keywords_dict), 'Author Keywords')
lda_func(bow_dict_strings(id_keywords_dict), 'ID Keywords')
lda_func(bow_dict_strings(abs_dict), 'Abstract')
lda_func((bow_dict_strings(abs_dict) + bow_dict_strings(titles_dict)), 'Titles + Abstract')