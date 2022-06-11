from os import path, listdir
import pandas as pd


def make_dataframe():
    """opens all files then make a Dataframe with all reviews"""
    
    files = listdir('data/')
    print(f'{len(files)} files founded')
    
    for i, file in enumerate(files):
        if i == 0:
            df = pd.read_csv(f'data/{file}', index_col=0)
            
        else:
            df_new = pd.read_csv(f'data/{file}', index_col=0)
            df = pd.concat([df, df_new])
    
    print(f'Total of reviews : {df.shape[0]}')

    return df

