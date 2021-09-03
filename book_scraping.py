# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
import csv
import os
from tqdm import tqdm

# Fonction de récupération des infos d'un bouquin sous forme de dictionnaire
def get_book_infos(url):
    response = requests.get(url)
    if response.status_code == 200:
        # On reforme le lien sans les \..
        lien = response.url
        soup = BeautifulSoup(response.content, 'html.parser')
        search_img = soup.find('div', {"class": "item active"}).find('img')["src"]
        image_lien = requests.get(f"http://books.toscrape.com/{search_img}").url
        # Les infos du produit sont dans des balises tr
        trs = soup.findAll('tr')
        # Dictionnaire de récupération des infos
        dict_tr = {}
        for tr in trs:
            th = tr.find('th').text
            td = tr.find('td').text
            dict_tr[th] = td
    # On renvoit les infos du bouquin
    return {'product_page_url': lien,
            'universal_ product_code (upc)': dict_tr['UPC'],
            'title': soup.find('h1').text,
            'price_including_tax': dict_tr['Price (incl. tax)'],
            'price_excluding_tax': dict_tr['Price (excl. tax)'],
            'number_available': dict_tr['Availability'],
            'product_description': soup.findAll('meta')[2]["content"],
            'category': soup.findAll('li')[2].find('a').text,
            'review_rating': soup.findAll('p')[2]["class"][1],
            'image_url': image_lien}


def pass_category(url, nom):
    print(f"Passage de la catégorie {nom}...")
    # La liste des bouquins trouvés
    books = []
    while url != '':
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            # Les livres sont rangés dans les balises article
            articles = soup.findAll('article', {'class': 'product_pod'})
            for article in tqdm(articles):
                # On récupère le lien du bouquin
                lien = url + "/../" + article.find('h3').find('a')['href']
                # On lance la fonction sur le lien du bouquin
                dict_product = get_book_infos(lien)
                books.append(dict_product)
            # On regarde s'il y a une page de plus, et si c'est le cas on récupère le lien
            next_page = soup.find('li', {'class': 'next'})
            if not next_page:
                url = ''
            else:
                url = url + "/../" + soup.find('li', {'class': 'next'}).find('a')['href']
    write_category(nom, books)


def write_category(nom, books):
    print(f"Ecriture de la categorie {nom}...")
    # On enregistre dans un csv
    csv_path = os.path.abspath(os.path.dirname(__file__)) + r'\Resultats\\' + nom + '.csv'
    with open(csv_path, 'w', newline='', encoding='utf-8') as csvfile:
        # Le titre des colonnes
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
            # On écrit les infos du bouquin
            writer.writerow(book)


url = "http://books.toscrape.com"
# Création du répertoire "Resultats" où seront enregistrés les csv
os.makedirs(os.path.abspath(os.path.dirname(__file__)) + r'\Resultats', exist_ok=True)
response = requests.get(url)
if response.status_code == 200:
    soup = BeautifulSoup(response.content, 'html.parser')
    list_categorie = soup.find('ul', {'class': 'nav nav-list'}).find('ul').findAll('li')
    for li in list_categorie:
        lien = url + '/' + li.find('a')['href']
        nom = li.find('a').text.replace('\n', '').replace('  ', '')
        pass_category(lien, nom)
