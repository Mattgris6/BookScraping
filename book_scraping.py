# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
import csv
import os

#Fonction de récupération des infos d'un bouquin sous forme de dictionnaire
def recup_info(url):
    response = requests.get(url)
    if response.ok:
        lien = response.url#On reforme le lien sans les \..
        soup = BeautifulSoup(response.content, 'html.parser')
        image_lien = requests.get("http://books.toscrape.com/" + soup.find('div', {"class":"item active"}).find('img')["src"]).url
        trs = soup.findAll('tr') #Les infos du produit sont dans des balises tr
        dict_tr = {} #Dictionnaire de récupération des infos
        for tr in trs:
            th = tr.find('th').text
            td = tr.find('td').text
            dict_tr[th] = td
    #On renvoit les infos du bouquin
    return {'product_page_url':lien, 'universal_ product_code (upc)':dict_tr['UPC'], 'title':soup.find('h1').text, 'price_including_tax':dict_tr['Price (incl. tax)'], 'price_excluding_tax':dict_tr['Price (excl. tax)'], 'number_available':dict_tr['Availability'], 'product_description':soup.findAll('meta')[2]["content"], 'category':soup.findAll('li')[2].find('a').text, 'review_rating':soup.findAll('p')[2]["class"][1], 'image_url':image_lien}

def categorie(url, nom):
    liste_bouquin = [] #La liste des bouquins trouvés
    while url != '':
        response = requests.get(url)
        if response.ok:
            soup = BeautifulSoup(response.content, 'html.parser')
            liste_article = soup.findAll('article', {'class':'product_pod'})#Les livres sont rangés dans les balises article
            for article in liste_article:
                lien = url + "/../" + article.find('h3').find('a')['href']#On récupère le lien du bouquin
                dict_product = recup_info(lien)#On lance la fonction sur le lien du bouquin
                liste_bouquin.append(dict_product)
            try:
                url = url + "/../" + soup.find('li', {'class':'next'}).find('a')['href']#On regarde s'il y a une page de plus, et si c'est le cas on récupère le lien
            except:
                url = ''

    #On enregistre dans un csv
    with open(os.path.abspath(os.path.dirname(__file__)) + r'\Resultats\\' + nom + '.csv', 'w', newline='', encoding='utf-8') as csvfile:
        #Le titre des colonnes
        fieldnames = ['product_page_url', 'universal_ product_code (upc)', 'title', 'price_including_tax', 'price_excluding_tax', 'number_available', 'product_description', 'category', 'review_rating', 'image_url']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter=';')
        writer.writeheader()
        for bouquin in liste_bouquin:
            writer.writerow(bouquin)#On écrit les infos du bouquin


url = "http://books.toscrape.com"
os.makedirs(os.path.abspath(os.path.dirname(__file__)) + r'\Resultats', exist_ok=True)#Création du répertoire "Resultats" où seront enregistrés les csv
response = requests.get(url)
if response.ok:
    soup = BeautifulSoup(response.content, 'html.parser')
    liste_categorie = soup.find('ul', {'class':'nav nav-list'}).find('ul').findAll('li')
    for li in liste_categorie:
        lien = url + '/' + li.find('a')['href']
        nom = li.find('a').text.replace('\n', '').replace('  ', '')
        categorie(lien, nom)


