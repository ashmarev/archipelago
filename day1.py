# Вводим переменные
number_of_pages = '100'
number_of_items = '100'
csv_file_name = 'nevnovru_' + str(int(number_of_pages) * int(number_of_items)) + str('.csv')

from google.colab import drive
drive.mount('/gdrive')
%cd /gdrive
%cd /gdrive/My Drive
%cd /gdrive/My Drive/wproject102
%cd /gdrive/My Drive/wproject102/archipelago

# importing the requests library 
import requests
import pandas as pd
import os

# так как добавляю записи в цикле
if os.path.isfile(str(csv_file_name)):
  os.remove(str(csv_file_name))

# headers
user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_2) AppleWebKit/600.3.18 (KHTML, like Gecko) Version/8.0.3 Safari/600.3.18'
headers = { 'User-Agent' : user_agent }  

# запрос из api в цикле
for number in range(1,int(number_of_pages) + 1): # number страниц по 100 записей
  URL = "https://nevnov.ru/posts/get?limit=" + str(number_of_items) + '&region=0&needParam=1&postExept=0&page=' + str(number)
  # sending get request and saving the response as response object 
  r = requests.get(url = URL, headers=headers)
  # extracting data in json format 
  json = r.json() 
  # counting array size
  print(str(URL) + str(" ") + str(len(json['posts']['data'])))
  df3 = pd.DataFrame.from_dict(json['posts']['data'])
  selected_columns = df3[["date_num", "time", "title", "content", "fulllink",]]
  df2csv = selected_columns.copy()
  df2csv = df2csv.rename(columns={'date_num':'date', 'content':'text', 'fulllink':'url'})
   #df2csv = df2csv.replace(to_replace ='<p>', value = '', regex = True)
  df2csv.to_csv(str(csv_file_name), mode='a', index=False, sep=";") #append

# Read file
csv2df = pd.read_csv(csv_file_name, sep=";")
csv2df
