version = 3.0


import os
import pandas as pd
import time
import shutil
input_dir = "Raw Data Files"
print(f'***----🎀  TIP Data Software v{version}  🎀----***')
print('***-----This program is created by ASF Equipment AIIAP Lahore-----***')
print('***----For any assistance or error in the program Please contact Us at 03000705208 ----***')
print(f'***----This is version {version} of TIP Data Software.  ----***')
print(
    """
--------------------------------------------------------------------------------------------------------------------------
            ***Version 3.0 Updates***                                                                                       
Update includes:
-> All files can be placed in one folder. Automatic separation of diffferent files based on data and date.
-> Process all files from any date range.

            ***Version 2.0 Updates***   
Update includes:
-> Data types of columns corrected. Some digits data points were treated as string, converted them to integer 
'LOGIN ID', 'BAG COUNT', 'TIP COUNT', 'HIT'
-> Output as Excel instaed of CSV
--------------------------------------------------------------------------------------------------------------------------
"""
)
print(f'Please place all your relevent TIP data files  in the folder  "{input_dir}"')
qq = input('Have you followed above instruction? If Yes press "Y"......')



def create_directory(directory_path):
  """Creates a directory at the specified path.
  Args:
    directory_path: The path to the directory to create.
  """

  try:
    os.makedirs(directory_path, exist_ok=True)
    print(f"Directory '{directory_path}' created successfully.")
  except OSError as error:
    print(f"Error creating directory: {error}")
all_data_files_folder = "All Data Files"
create_directory(all_data_files_folder)

# Scanning "input_dir" folder and getting all files paths in subdirs into files_list.
files_list=[]
def recursive_scandir(directory):
    for entry in os.scandir(directory):
        if entry.is_dir():
            recursive_scandir(entry.path)
        else:
            if '.txt' in entry.path:
                files_list.append(entry.path)  # Or perform other actions with the file

recursive_scandir(input_dir)
# Copying files form input_dir to "All Data Files" dir
for file in files_list:
    shutil.copy2(file, all_data_files_folder)

# In Smith Detection Machines all files ends with a specific number 1-4 according to data, like tip data files end with 3. We can classify files:
classification_dict={}
for file in files_list:
# def classification(file):
    file_name= file.split("\\")[-1].replace('.txt','')
    file_serial=file_name[-1]
    date=file_name[-7:-1]
    if file_serial not in classification_dict:
        classification_dict[file_serial]={}
    if date not in classification_dict[file_serial]:
        classification_dict[file_serial][date]=[]
    if date in classification_dict[file_serial]:
        classification_dict[file_serial][date].append(file_name)

if qq == 'Y' or qq == 'y':
    
    df = pd.DataFrame()

    for date in classification_dict['3']:
        for filess in classification_dict['3'][date]:
            df1 = pd.read_csv(f'{all_data_files_folder}//{filess}.txt', delimiter='\t')
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
        df3.to_excel(f'Tip Data {date[0:2]}-{date[2:]}.xlsx',index=False)
    print('Programme completed successfully.')