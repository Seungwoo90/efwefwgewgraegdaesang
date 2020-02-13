import pandas as pd
import ast

# 간단한 후처리 후 진행 # 수입품 찾기

def delete_hyphen(ocr_result):
    output = ocr_result.replace('-', '')
    return output

def delete_space(ocr_result):
    output = ocr_result.replace(' ','')
    output = output.replace('\n','')
    return output

# joined.csv columns : ['작업 이름', 'values', 'numbers', 1_ocr, 1_url ....]

df = pd.read_csv("merged_output.csv")
df = df.fillna('')

ocr_cols = len(df.columns) - 5

is_it_valid_number = []

for i, row in df.iterrows():
    
    numbers_valid = 0
    # 일치하지 않는 경우 0

    if row['numbers'] == '':
        # user input이 없는 경우
        # 수입품인지 판단

        numbers_matching = []

        number_matching = 0

        for i in range(ocr_cols):
            # ocr outpt column들 돌면서
            ocr_col = str(i)

            if row[ocr_col] != '':
                # ocr output이 있는 경우
                row[ocr_col] = delete_hyphen(row[ocr_col])
                row[ocr_col] = delete_space(row[ocr_col])

                if '품목' in row[ocr_col]:
                    number_matching += 9999
                    break

                if '수입' in row[ocr_col]:
                    number_matching += 1

        numbers_matching.append(number_matching)

        if sum(numbers_matching) >= 9999:
            # 품목이라는 단어를 찾음 (invalid)
            is_it_valid_number.append(numbers_valid)
        elif 0 in numbers_matching:
            # 수입이라는 단어를 못 찾음 (invalid)
            is_it_valid_number.append(numbers_valid)
        elif 0 not in numbers_matching:
            # 품목이라는 못 찾고, 수입이라는 단어를 찾음 (valid)
            numbers_valid = 1
            is_it_valid_number.append(numbers_valid)
        


    elif row['numbers'] != '':
        # user input이 있는 경우
        numbers = ast.literal_eval(row['numbers'])
        images = ast.literal_eval(row['images'])
        numbers_matching = []
    
        for number in numbers:
            #사용자가 입력한 번호(들) 

            number_matching = 0

            for i in range(ocr_cols):
                # ocr outpt column들 돌면서
                ocr_col = str(i)
                
                if row[ocr_col] != '':
                    # ocr output이 있는 경우
                    row[ocr_col] = delete_hyphen(row[ocr_col])
                    row[ocr_col] = delete_space(row[ocr_col])

                    if number in row[ocr_col] and '품목보고번호' in row[ocr_col]:

                        with open('matched_numbers.txt', 'a') as file:
                            file.write('작업 이름 : ' + str(row['작업 이름']) +'\n'
                            + 'USER INPUT : ' + str(row['numbers']) + '\n'
                            + 'SEARCHING NUMBER : ' + number + '\n'
                            + 'img url : ' + images[i] + '\n'
                            + 'OCR OUTPUT : \n' + row[ocr_col] + '\n'
                            + '=============================================\n\n\n')

                        number_matching += 1

            numbers_matching.append(number_matching)

        if 0 not in numbers_matching:
            # '품목보고번호' 단어와 사용자가 입력한 번호(들)를 모두 찾은 경우
            numbers_valid = 1
            is_it_valid_number.append(numbers_valid)
        elif 0 in numbers_matching:
            # '품목보고번호' 단어와 사용자가 입력한 번호(들) 중 하나라도 찾지 못한 경우
            is_it_valid_number.append(numbers_valid)


df['is_it_valid_number'] = is_it_valid_number



is_it_valid_value = []

for i, row in df.iterrows():
    
    values_valid = 0


    if row['values'] == '':
        # user input이 없는 경우 (invalid)
        is_it_valid_value.append(values_valid)

    elif row['values'] != '':
        # user input이 있는 경우
        values = ast.literal_eval(row['values'])
        images = ast.literal_eval(row['images'])
        numbers_matching = []
    
        for value in values:
            #사용자가 입력한 식품유형(들) 

            number_matching = 0

            for i in range(ocr_cols):
                # ocr outpt column들 돌면서
                ocr_col = str(i)

                if row[ocr_col] != '':
                    # ocr output이 있는 경우
                    row[ocr_col] = delete_hyphen(row[ocr_col])
                    row[ocr_col] = delete_space(row[ocr_col])

                    if value in row[ocr_col] and '유형' in row[ocr_col]:

                        with open('matched_vales.txt', 'a') as file:
                            file.write('작업 이름 : ' + str(row['작업 이름']) +'\n'
                            + 'USER INPUT : ' + str(row['values']) + '\n'
                            + 'SEARCHING VALUE : ' + value + '\n'
                            + 'img url : ' + images[i] + '\n'
                            + 'OCR OUTPUT : \n' + row[ocr_col] + '\n'
                            + '=============================================\n\n\n')

                        number_matching += 1

            numbers_matching.append(number_matching)

        if 0 not in numbers_matching:
            # '유형' 단어와 사용자가 입력한 식품유형(들)을 모두 찾은 경우
            values_valid = 1
            is_it_valid_value.append(values_valid)
        elif 0 in numbers_matching:
            # '유형' 단어와 사용자가 입력한 식품유형(들) 중 하나라도 찾지 못한 경우
            is_it_valid_value.append(values_valid)


df['is_it_valid_value'] = is_it_valid_value

df = df[['작업 이름', 'values', 'numbers', 'is_it_valid_value', 'is_it_valid_number']]

df.to_csv('compared.csv', index = False)

