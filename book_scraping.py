# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
import csv
import os
from tqdm import tqdm

def get_book_infos(url):
    """Get book's info from an url and return a dictionnary"""
    response = requests.get(url)
    if response.status_code == 200:
        # We get the link without the \..
        link = response.url
        soup = BeautifulSoup(response.content, 'html.parser')
        search_img = soup.find('div', {"class": "item active"}).find('img')["src"]
        image_link = requests.get(f"http://books.toscrape.com/{search_img}").url
        # Product info are in balise tr
        trs = soup.findAll('tr')
        # Stocking the info in a dictionnary
        dict_tr = {}
        for tr in trs:
            th = tr.find('th').text
            td = tr.find('td').text
            dict_tr[th] = td
    # All the informations of the book that we need
    return {'product_page_url': link,
            'universal_ product_code (upc)': dict_tr['UPC'],
            'title': soup.find('h1').text,
            'price_including_tax': dict_tr['Price (incl. tax)'],
            'price_excluding_tax': dict_tr['Price (excl. tax)'],
            'number_available': dict_tr['Availability'],
            'product_description': soup.findAll('meta')[2]["content"],
            'category': soup.findAll('li')[2].find('a').text,
            'review_rating': soup.findAll('p')[2]["class"][1],
            'image_url': image_link}


def pass_category(url, name):
    """Get all books of one category and then send it to the writer function"""
    print(f"Passage de la catégorie {name}...")
    # Initialize list of books
    books = []
    while url != '':
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            # Books are notify with article balise
            articles = soup.findAll('article', {'class': 'product_pod'})
            for article in tqdm(articles):
                # Get the book's link
                link = url + "/../" + article.find('h3').find('a')['href']
                # Run the function to get book's info
                dict_product = get_book_infos(link)
                books.append(dict_product)
            # Searching for a next page
            next_page = soup.find('li', {'class': 'next'})
            if not next_page:
                url = ''
            else:
                url = url + "/../" + soup.find('li', {'class': 'next'}).find('a')['href']
    write_category(name, books)


def write_category(name, books):
    """Write the informations of books of one category in one csv file"""
    print(f"Ecriture de la categorie {name}...")
    # Save in one csv file
    csv_path = os.path.abspath(os.path.dirname(__file__)) + r'\Results\\' + name + '.csv'
    with open(csv_path, 'w', newline='', encoding='utf-8') as csvfile:
        # Headers name
        fieldnames = ['product_page_url',
                      'universal_ product_code (upc)',
                      'title', 'price_including_tax',
                      'price_excluding_tax',
                      'number_available',
                      'product_description',
                      'category',
                      'review_rating',
                      'image_url']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter=';')
        writer.writeheader()
        for book in books:
            # Writing the book's infos
            writer.writerow(book)


url = "http://books.toscrape.com"
# Create a folder "Results" where we'll save the csv
os.makedirs(os.path.abspath(os.path.dirname(__file__)) + r'\Results', exist_ok=True)
response = requests.get(url)
if response.status_code == 200:
    soup = BeautifulSoup(response.content, 'html.parser')
    list_category = soup.find('ul', {'class': 'nav nav-list'}).find('ul').findAll('li')
    for li in list_category:
        link = url + '/' + li.find('a')['href']
        name = li.find('a').text.replace('\n', '').replace('  ', '')
        pass_category(link, name)
