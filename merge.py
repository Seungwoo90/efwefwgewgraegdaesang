import json
import pandas as pd

def get_values(dic):
    values = []
    food_type_list = dic['food_type']
    
    for i in food_type_list:
        if i == "":
            values = None
        else:
            value = i['value']
            values.append(value)
            
    return values

def get_numbers(dic):
    numbers = []
    number_list = dic['item_report_number']
    
    for i in number_list:
        if i == "":
            numbers = None
        else:
            numbers.append(i)
    return numbers

def get_img_url(dic):
    return dic['images']


export_df = pd.read_csv("export.csv")


export_df['작업 컨텍스트'] = export_df['작업 컨텍스트'].apply(lambda x : json.loads(x))
export_df['작업수행 결과'] = export_df['작업수행 결과'].apply(lambda x : json.loads(x))
export_df['비고'] = export_df['비고'].apply(lambda x : json.loads(x))


export_df['values'] = export_df['작업수행 결과'].apply(get_values)
export_df['numbers'] = export_df['작업수행 결과'].apply(get_numbers)
export_df['images'] = export_df['작업 컨텍스트'].apply(get_img_url)
export_df['api_id'] = export_df['비고'].apply(lambda x : x['api_id'])

export_df = export_df[['작업 이름', 'api_id', 'values', 'numbers', 'images']]



output_df = pd.read_csv("OCR_output.csv")

output_df = output_df.rename(columns={'api_key': 'api_id'})


joined_df = export_df.merge(output_df, on = 'api_id', how='left')

joined_df.to_csv('merged_output.csv', index = False)

