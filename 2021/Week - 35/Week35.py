
#IMPORTS
from pandas import ExcelFile, read_excel, Series, merge
from numpy import where

#2021\Week - 35\Inputs\Pictures Input.xlsx
#READ DATA
with ExcelFile(r'.\2021\Week - 35\Inputs\Pictures Input.xlsx') as xl :
    frames  = read_excel(xl, sheet_name = 'Frames')
    pictures  = read_excel(xl, sheet_name = 'Pictures')


#PROCESS DATA
#Split the frame and picture sizes in to Length and Width (cm) 
frames['Size'] = frames.Size.str.replace('X', 'x')

# Split frame dimensions and convert to cm
frames['Size_'] = frames.Size.apply(lambda s: s.split('x')
                     if 'x' in s else [s, s])
frames['Size_'] = frames['Size_'].apply(lambda x: sorted([int(i.strip()[:-1])*2.54
                     if i.strip().endswith('"') else int(i.strip()[:2]) for i in x], reverse= True))
frames[['f_side_1', 'f_side_2']] = frames.Size_.apply(Series)
frames.drop('Size_', axis=1, inplace=True)

frames['Area'] = round (frames['f_side_1'] * frames['f_side_2'], 0).astype('Int64')

# Split picture dimensions into length and width
pictures['Size_'] = pictures.Size.apply(lambda s: s.split('x')
                     if 'x' in s else [s, s])
pictures['Size_'] = pictures['Size_'].apply(lambda x: sorted([ int(i.strip()[:2])
                      for i in x], reverse= True))
pictures[['Length', 'Width']] = pictures.Size_.apply(Series)
pictures['Area'] = (pictures.Length * pictures.Width).astype('Int64')  
pictures.drop('Size_', axis=1, inplace=True)               

#Merge pictures and the frames
df = merge(pictures, frames, how='cross', suffixes=('_pic', '_frame'))

#Filter frames that fit the pictures
# Frames can be rotated
df[['f_side_1', 'f_side_2']] = df[['f_side_1', 'f_side_2']].astype('int')
df = df.iloc[where(
                (df['f_side_1'] >= df['Length']) & (df['f_side_2'] >= df['Width']) |
                (df['f_side_1'] >= df['Width']) & (df['f_side_2'] >= df['Length'])
                )].copy()
# Extra space
df['Extra space'] = df['Area_frame'] - df['Area_pic']

# Rank pictures by Extra space column/ best fit (Mininum extra space)
ranks = df.groupby(['Picture', 'Size_pic'])['Extra space'].rank().rename('Rnk')
best_fit = ranks[ranks == 1.0].index

df = df.loc[best_fit]
df = df.iloc[:, [0,2,3,5]]
df.columns = ['Picture', 'Max Side', 'Min Side', 'Frame'] # rename cols


#OUTPUT
df.to_csv(r'.\2021\Week - 35\Output\week_35_output.csv', index = False)
print('end')


