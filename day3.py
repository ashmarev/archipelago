# Переменные
csv_file_name = 'nevnovru_10.csv'

from google.colab import drive
drive.mount('/gdrive')
%cd /gdrive
%cd /gdrive/My Drive
%cd /gdrive/My Drive/wproject102
%cd /gdrive/My Drive/wproject102/archipelago

!pip install pymorphy2[fast]
!pip install -U pymorphy2-dicts-ru
import pymorphy2
import re
import pandas as pd

morph = pymorphy2.MorphAnalyzer()
regex = re.compile("[А-Яа-яA-Za-z-]+")

def lemmatize(text, morph=morph):
  try:
    return [morph.parse(text)[0].normal_form for text in regex.findall(text.lower())]
  except:
    return "something_wrong"

df = pd.read_csv(csv_file_name, sep=";")
df['split_text'] = df.text.apply(lambda x: lemmatize(x))# указываем столбец, который лемматизируем
import json
with open('word_scores_l500_k25_n_min.json') as json_file: 
    word_scores_500 = json.load(json_file)
with open('word_scores_l5000_k25_n_min.json') as json_file: 
    word_scores_5000 = json.load(json_file)
with open('word_scores_l50000_k25_n_min.json') as json_file: 
    word_scores_50000 = json.load(json_file)

def determine_tone_500(word_list):
  try:
    score = [word_scores_500[word] for word in word_list if word in word_scores_500]
    return sum(score) / len(score)
  except:
    return "22"

def determine_tone_5000(word_list):
  try:
    score = [word_scores_5000[word] for word in word_list if word in word_scores_5000]
    return sum(score) / len(score)
  except:
    return "22"

def determine_tone_50000(word_list):
  try:
    score = [word_scores_50000[word] for word in word_list if word in word_scores_50000]
    return sum(score) / len(score)
  except:
    return "22"

df['tone_500'] = df['split_text'].apply(lambda x: determine_tone_500(x))
df['tone_5000'] = df['split_text'].apply(lambda x: determine_tone_5000(x))
df['tone_50000'] = df['split_text'].apply(lambda x: determine_tone_50000(x))
selected_columns = df[["date", "time", "title", "url", "tone_500", "tone_5000", "tone_50000","split_text"]]
df = selected_columns.copy()
df.to_csv('tone_of_' + csv_file_name, sep=";", index=False)# убираем лишний индекс
df2 = pd.read_csv('tone_of_' + csv_file_name, sep=";")
df2
