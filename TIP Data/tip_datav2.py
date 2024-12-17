#               TIP Data Software v2.0
# Update includes:
# Data types of columns corrected. Some digits data points were treated as string, converted them to integer 'LOGIN ID', 'BAG COUNT', 'TIP COUNT', 'HIT'
# Output as Excel instaed of CSV
# 

import os
import pandas as pd
import time
print('***----🎀  TIP Data Software v2.0  🎀----***')
print('***-----This program is created by ASF Equipment AIIAP Lahore-----***')
print('***----For any assistance or error in the program Please contact Us at 03000705208 ----***')
print('***----This is version 2.0 of TIP Data Software. Released on 20/11/2024 ----***')
print('Please place all your relevent TIP data files  in the folder  "tip data files"')
time.sleep(10)
qq = input('Have you followed above instruction? If Yes press "Y"......')

if qq == 'Y' or qq == 'y':
    destdir = './tip data files/'
    files = [f for f in os.listdir(destdir) if os.path.isfile(os.path.join(destdir, f)) and '.txt' in f]
    if len(files) < 1:
        print('No file found in the folder. Exiting the program now.')
        time.sleep(4)
    else:
        df = pd.DataFrame()
        for file in files:
            df1 = pd.read_csv(f'{destdir}{file}', delimiter='\t')
            df = pd.concat([df, df1], ignore_index=True)
        df = df[['NAME', 'LOGIN ID', 'BAG COUNT', 'TIP COUNT', 'HIT']]
        df = df[df['NAME'] != 'SERVICE']
        df = df[df['LOGIN ID']!='unknown user'].dropna()
        df = df.astype({
        'NAME': str,
        'LOGIN ID': int,
        'BAG COUNT': int,
        'TIP COUNT': int,
        'HIT': int
    })
        df = df.groupby(['LOGIN ID'], as_index=False).agg({
        'NAME': 'first',
        'BAG COUNT': 'sum',
        'TIP COUNT': 'sum',
        'HIT': 'sum'
    })
        df = df[['NAME', 'LOGIN ID', 'BAG COUNT', 'TIP COUNT', 'HIT']]
        df['RESULT'] = (df['HIT'] / df['TIP COUNT'] * 100).round(0)
        def grades(x):
            if x == 100:
                return 'A+'
            if x >= 90:
                return 'A'
            if x >= 80:
                return 'B'
            if x >= 70:
                return 'C'
            return 'D'
        df['GRADE'] = df['RESULT'].apply(grades)
        df3 = df.dropna(subset=['RESULT'])
        df3 = df3.sort_values(by=['RESULT'], axis=0, ascending=False)
        df3=df3[df3['BAG COUNT']!=0]
        df3.insert(0, 'SER NO', range(1, len(df3) + 1))
        df3.to_excel('Tip Data.xlsx',index=False)
        print('Programme completed successfully.')