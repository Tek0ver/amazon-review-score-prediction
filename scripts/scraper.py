import requests, csv
from bs4 import BeautifulSoup
from os import path


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

        print('Soup made from url')
    
    else:
        
        with open(url, 'r') as file:
            contents = file.read()
            soup = BeautifulSoup(contents, 'html.parser')
        
        print('Soup made from file')

    return soup


def get_reviews(soup, wanted_lang='France'):
    """returns a list of reviews in the wanted language from a soup object"""
    
    reviews = soup.find_all('div', class_='review')
    
    lang_filtered_reviews = []
    
    for review in reviews:
        lang = review.find('span', class_='review-date').text.strip()
        if lang.find(wanted_lang) != -1:
            lang_filtered_reviews.append(review)
    
    return lang_filtered_reviews


def get_reviews_infos(soup, wanted_lang='France'):
    """returns a list of dict about the review in the wanted language as
    {'product': , title': , 'rating': , 'text': } from a soup object"""
    
    print('Scraping reviews...')

    product = soup.title.text.replace('Amazon.fr\xa0:Commentaires en ligne: ', '')
    
    reviews_infos = []
    
    for review in get_reviews(soup, wanted_lang):
    
        review_infos = {
            'product': product,
            'title': review.find('a', class_='review-title').text.strip(),
            'rating': float(review.find('i', class_='review-rating').text.strip()[:3].replace(',', '.')),
            'text': review.find('span', class_='review-text').text.strip()
        }
        
        reviews_infos.append(review_infos)
        
    print(f'{len(reviews_infos)} reviews scraped')

    return reviews_infos


def reviews_to_csv(reviews):

    file_name = reviews[0]['product'].replace(' ', '_') + '.csv'
    
    if path.exists(f'data/{file_name}'):
        write_header = False
        print('Rows added to existing file')
    else:
        write_header = True
        print('New file created')
        
    with open(f'data/{file_name}', 'a') as csvfile:
        fieldnames = reviews[0].keys()
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        if write_header:
            writer.writeheader()
        
        for review in reviews:
            writer.writerow(review)
