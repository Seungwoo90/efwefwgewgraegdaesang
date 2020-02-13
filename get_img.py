import pandas as pd
import os
import requests
import ast
from multiprocessing.dummy import Pool as ThreadPool
import time

def get_img(path_and_url):
    path, url = path_and_url[0], path_and_url[1]
    try:
        img_data = requests.get(url).content
    except Exception as e:
        with open('request_failed.txt', 'a') as file:
            file.write("Exception occurred: {} :::: {} 이미지 파일 request 오류".format(e, url))
        print("Exception occurred: {} :::: {} 이미지 파일 request 오류".format(e, url))
        
    with open(path, 'wb') as img:
            img.write(img_data)
            print(path + '  완료')  


df = pd.read_csv("13차 분유.csv")
df['images'] = df['images'].apply(ast.literal_eval) 


path_and_url = []

for i, row in df.iterrows():
    api_id = row['api_id']
    path = f"./picture/{api_id}"
    
    if not os.path.exists(path):
        os.mkdir(path)

    for i, url in enumerate(row['images']):
        path = f"./picture/{api_id}/{api_id}_{str(i)}.jpg"
        path_and_url.append((path, url))



pool = ThreadPool(4)

t1=time.time()
pool.map(get_img, path_and_url)

pool.close()
pool.join()

print(time.time()-t1)