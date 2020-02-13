from google.cloud import vision
import io
import glob
import os
import multiprocessing
import csv
import json
import pandas as pd

# 권한설정 export GOOGLE_APPLICATION_CREDENTIALS="/home/yoo/Desktop/DeepNatural AI-ab0f13ad71d2.json"
# 권한설정 export GOOGLE_APPLICATION_CREDENTIALS="/home/yoo/Desktop/cre.json"

def detect_text(path):
    
    client = vision.ImageAnnotatorClient()

    with io.open(path, 'rb') as image_file:
        content = image_file.read()


    try:
        image = vision.types.Image(content=content)
        response = client.text_detection(image=image)
        texts = response.text_annotations
        output = texts[0].description
    except Exception as e:
            with open('OCR_failed.txt', 'a') as file:
                file.write("Exception occurred: {} ::\n {} 이미지 파일\n\n".format(e, path))
            output = 'NO OCR OUTPUT'

    api_id = path.split('/')[2]
    image_num = path.split('_')[1].replace('.jpg', '')


    return api_id, image_num, output


if __name__ == "__main__":

    directories = os.listdir('./picture')
    
    image_paths = []


    
    
    #2063################################# 분할 실행 ###########
    dir1 = directories[:401]
    dir2 = directories[401:801]
    dir3 = directories[801:1201]
    dir4 = directories[1201:1601]
    dir5 = directories[1601:]
    ##########################################################
    
    for directory in dir5:
        images = glob.glob(f'./picture/{directory}/*.jpg')
        for image in images:
            image_paths.append(image)

    
    p = multiprocessing.Pool(4)
    
    results = {}

    with open('OCR_OUTPUT_5.txt', mode='a') as file:
        for api_id, image_num, output in p.imap_unordered(detect_text, image_paths):
            file.write(f"{api_id}:::::{image_num}\n\n{output}\n======================================\n")
            print(f"{api_id}:::::{image_num}\n\n{output}\n======================================\n")
            if api_id not in results:
                results[api_id] = {image_num : output}
            elif api_id in results:
                results[api_id][image_num] = output


    with open('OCR_OUTPUT_5.json', 'w') as file:
        json.dump(results, file, ensure_ascii=False)

    
    multirows = []

    for key,value in results.items():
        singlerow={}
        singlerow['api_key'] = key
        for number, ocroutput in value.items():
            singlerow[number] = ocroutput
        multirows.append(singlerow)


    df = pd.DataFrame(multirows)
    cols = list(df.columns)
    cols.sort()
    cols.insert(0, cols.pop())
    df = df[cols]
    df.to_csv('OCR_OUTPUT_5.csv', index=False)

    print(df.head())


