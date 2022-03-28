import spacy
from newsapi.newsapi_client import NewsApiClient
import en_core_web_lg
import pandas as pd
from collections import Counter
from string import punctuation
from wordcloud import WordCloud
import matplotlib.pyplot as plt

nlp_eng = en_core_web_lg.load()
newsapi = NewsApiClient(api_key='b91021393937486591a58d360f322a61')

def getArticle(page):
    temp = newsapi.get_everything(q='coronavirus',language='en', from_param='2022-25-03',to='2022-27-03', sort_by='relevancy', page=page)
    return temp

articles = list(map(getArticle,range(1,6)))

dados = []

for i, article in enumerate(articles):
    for x in article['articles']:
        title = x['title']
        description = x['description']
        content = x['content']
        dados.append({'title':title, 'desc':description, 'content':content})

df = pd.DataFrame(dados)
df = df.dropna()
df.head()

results = []

def get_keywords_eng(text):
    result = []
    pos_tag = ['PROPN','VERB','NOUN']
    doc = nlp_eng(text.lower())
    for token in doc:
        if(token.text in nlp_eng.Defaults.stop_words or token.text in punctuation):
            continue
        if(token.pos_ in pos_tag):
            result.append(token.text)
    print(result)
    return result

for content in df.content.values:
    results.append([('#' + x[0]) for x in Counter(get_keywords_eng(content)).most_common(5)])

df['keyword'] = results

text = str(results)

wordcloud = WordCloud(max_font_size=50, max_words=100, background_color="white").generate(text)
plt.figure()
plt.imshow(wordcloud, interpolation="bilinear")
plt.axis("off")
plt.show()




        