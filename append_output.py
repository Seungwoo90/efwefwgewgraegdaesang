import pandas as pd
import json

OCR1_df = pd.read_csv("OCR_OUTPUT_1.csv")
OCR2_df = pd.read_csv("OCR_OUTPUT_2.csv")
OCR3_df = pd.read_csv("OCR_OUTPUT_3.csv")
OCR4_df = pd.read_csv("OCR_OUTPUT_4.csv")
OCR5_df = pd.read_csv("OCR_OUTPUT_5.csv")



OCR1_df = OCR1_df.append(OCR2_df)
OCR1_df = OCR1_df.append(OCR3_df)
OCR1_df = OCR1_df.append(OCR4_df)
OCR1_df = OCR1_df.append(OCR5_df)



OCR1_df.to_csv('OCR_output.csv', index = False)



with open('OCR_OUTPUT_1.json') as f:
  ocr1 = json.load(f)

with open('OCR_OUTPUT_2.json') as f:
  ocr2 = json.load(f)

with open('OCR_OUTPUT_3.json') as f:
  ocr3 = json.load(f)

with open('OCR_OUTPUT_4.json') as f:
  ocr4 = json.load(f)

with open('OCR_OUTPUT_5.json') as f:
  ocr5 = json.load(f)


  

   
# appending the data 

ocr1.update(ocr2)
ocr1.update(ocr3)
ocr1.update(ocr4)
ocr1.update(ocr5)

  
# the result is a JSON string: 
ocr_json = json.dumps(ocr1, ensure_ascii=False)  

with open('OCR_output.json', 'w') as file:
    file.write(ocr_json)