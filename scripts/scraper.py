import requests
from bs4 import BeautifulSoup
from os import path, listdir
import pandas as pd


def get_soup(url, html_file=False):
    """returns soup object of the given html page from url or file"""
    
    if html_file is False:
        
        splash = 'http://0.0.0.0:8050'

        r = requests.get(f'{splash}/render.html',
                    params={'url': url, 'wait': 2})

        soup = BeautifulSoup(r.text, 'html.parser')

        if soup.find('p', class_='a-last') is not None:
            if soup.find('p', class_='a-last').text == "Désolés, il faut que nous nous assurions que vous n'êtes pas un robot. Pour obtenir les meilleurs résultats, veuillez vous assurer que votre navigateur accepte les cookies.":
                raise ValueError('Amazon robot detection, try later')
            else:
                raise ValueError('unknown error')
    
    else:
        
        with open(url, 'r') as file:
            contents = file.read()
            soup = BeautifulSoup(contents, 'html.parser')

    return soup


def get_reviews(soup, wanted_lang='France'):
    """returns a list of dict about the review in the wanted language as
    {'product': , title': , 'rating': , 'text': } from a soup object"""

    all_reviews = soup.find_all('div', class_='review')

    lang_filtered_reviews = []

    for review in all_reviews:
        lang = review.find('span', class_='review-date').text.strip()
        if lang.find(wanted_lang) != -1:
            lang_filtered_reviews.append(review)

    product = soup.title.text.replace('Amazon.fr\xa0:Commentaires en ligne: ', '')
    
    reviews = []
    
    for review in lang_filtered_reviews:
    
        review_infos = {
            'product': product,
            'title': review.find('a', class_='review-title').text.strip(),
            'rating': float(review.find('i', class_='review-rating').text.strip()[:3].replace(',', '.')),
            'text': review.find('span', class_='review-text').text.strip()
        }
        
        reviews.append(review_infos)
        
    print(f'{len(reviews)} reviews scraped')

    return reviews


def reviews_to_csv(reviews):

    file_name = reviews[0]['product'] + '.csv'
    file_path = f'data/{file_name}'
    
    if path.exists(file_path):
        df = pd.read_csv(file_path, index_col=0)
        df_new = pd.DataFrame(reviews)
        df = pd.concat([df, df_new])
        df = df.reset_index(drop=True)
        print(f'{len(reviews)} reviews added to existing file')
    else:
        df = pd.DataFrame(reviews)
        print(f'New file created, {len(reviews)} reviews')

    len_before = df.shape[0]
    df = df.drop_duplicates()
    print(f'{len_before - df.shape[0]} duplicated rows deleted')

    df.to_csv(file_path)


def scrape_pages(url, start=1, end=5, autostop=True):

    reviews = []

    for page in range(start, end+1):

        print(f'Scraping page {page}')

        soup = get_soup(f'{url}&pageNumber={page}')

        page_reviews = get_reviews(soup)

        if autostop:
            if not page_reviews:
                print('No more reviews in selected language')
                break

        for review in page_reviews:
            reviews.append(review)

        if soup.find('li', class_='a-disabled a-last'):
            print('Last page, stop')
            break

        if page == end:
            print(f'All pages scraped, {len(reviews)} reviews')

    return reviews


def scrape_urls():
    """scrape urls from file then make one csv
    with reviews for each file"""

    urls_file = "urls_to_scrap.txt"

    print(f'Sourcing urls from {urls_file}')

    with open(urls_file, 'r') as file:
        urls = file.readlines()

    clean_urls = []

    for url in urls:
        url = url[:-1]
        if url:
            clean_urls.append(url)

    urls = clean_urls

    if not urls:
        print(f'{urls_file} is empty')
        exit()

    print(f'{len(urls)} url{"s" if len(urls) > 1 else ""} found')

    print('Start scraping :')

    for i, url in enumerate(urls):

        print(f'scraping url {i+1} : {url}')

        reviews = scrape_pages(url, 1, 20)
        if reviews:
            reviews_to_csv(reviews)
