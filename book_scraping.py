# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
import csv

#On récupère le lien de la page du livre
url = "http://books.toscrape.com/catalogue/its-only-the-himalayas_981/index.html"
response = requests.get(url)
if response.ok:
    #On enregistre dans un csv
    with open(r'C:\Users\MatthieuGRISON\OneDrive - AptiSkills\Documents\CoursOCR\ParcoursPython\Projet2\names.csv', 'w', newline='', encoding='utf-8') as csvfile:
        #Le titre des colonnes
        fieldnames = ['product_page_url', 'universal_ product_code (upc)', 'title', 'price_including_tax', 'price_excluding_tax', 'number_available', 'product_description', 'category', 'review_rating', 'image_url']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter=';')
        writer.writeheader()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        trs = soup.findAll('tr') #Les infos du produit sont dans des balises tr
        dict_product = {} #Dictionnaire de récupération des infos
        for tr in trs:
            th = tr.find('th').text
            td = tr.find('td').text
            dict_product[th] = td
        #On remplit le csv avec les infos du bouquin
        writer.writerow({'product_page_url':url, 'universal_ product_code (upc)':dict_product['UPC'], 'title':soup.find('h1').text, 'price_including_tax':dict_product['Price (incl. tax)'], 'price_excluding_tax':dict_product['Price (excl. tax)'], 'number_available':dict_product['Availability'], 'product_description':soup.findAll('meta')[2]["content"], 'category':soup.findAll('li')[2].find('a').text, 'review_rating':soup.findAll('p')[2]["class"][1], 'image_url':"http://books.toscrape.com/" + soup.find('div', {"class":"item active"}).find('img')["src"]})
            

    