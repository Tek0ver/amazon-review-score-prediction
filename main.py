from sys import argv
import scripts.scraper as scraper
import scripts.data_preparation as data_preparation


def print_menu():
    print("""How to use :
Type in the console "python main.py <option>"
<option> :
1 : Scrape urls from urls_to_scrap.txt to data/*.csv
2 : Combine all reviews preprocessed in data/_all_reviews.csv""")


if __name__ == "__main__":

    if len(argv) != 2:
        print_menu()
    elif argv[1] == '1':
        scraper.scrape_urls()
    elif argv[1] == '2':
        data_preparation.make_dataframe()
    else:
        print_menu()
