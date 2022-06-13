from os import path, listdir, remove
import pandas as pd
import string
from nltk.corpus import stopwords 
from nltk.tokenize import word_tokenize

def make_dataframe(preprocess=True, save_csv=True):
    """opens all files then make a Dataframe with all reviews"""
    
    files = listdir('data/')
    if '_all_reviews.csv' in files:
        files.remove('_all_reviews.csv')
    print(f'{len(files)} files founded')
    
    for i, file in enumerate(files):
        if i == 0:
            df = pd.read_csv(f'data/{file}', index_col=0)
            
        else:
            df_new = pd.read_csv(f'data/{file}', index_col=0)
            df = pd.concat([df, df_new])

    if preprocess:
        df['rating'] = df['rating'].apply(rating_to_int)
        df['preprocessed_title'] = df['title'].apply(preprocess_text)
        df['preprocessed_text'] = df['text'].apply(preprocess_text)

    df = df.reset_index(drop=True)

    if save_csv:
        file_path = 'data/_all_reviews.csv'
        if path.exists(file_path):
            remove(file_path)
        df.to_csv(file_path)

    print(f'Total of reviews : {df.shape[0] - 1}')

    return df


def rating_to_int(rating):
    """returns rating in int"""
    if rating in [5., 4., 3., 2., 1.]:
        return int(rating)
    else:
        print('error')
        return rating


def preprocess_text(text):
    """returns preprocessed text"""
    
    # lowercase
    text = text.lower()
    
    # number
    text = ''.join(word for word in text if not word.isdigit())
    
    # punctuation
    for punctuation in string.punctuation:
        text = text.replace(punctuation, '') 
    
    # stopwords
    stop_words = set(stopwords.words('french'))
    word_tokens = word_tokenize(text)
    text = [w for w in word_tokens if not w in stop_words]
    
    # tokenizing
    #stemmer = PorterStemmer()
    #stemmed = [stemmer.stem(word) for word in text]
    
    return text
