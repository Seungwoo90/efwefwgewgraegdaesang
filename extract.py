import json
import pandas as pd

df = pd.read_csv("export.csv")

df['작업 컨텍스트'] = df['작업 컨텍스트'].apply(lambda x : json.loads(x))
df['비고'] = df['비고'].apply(lambda x : json.loads(x))

df['images'] = df['작업 컨텍스트'].apply(lambda x : x['images'])
df['api_id'] = df['비고'].apply(lambda x : x['api_id'])


df = df[['api_id', 'images']]
df.to_csv('extracted.csv', index = False)




print(df.shape)