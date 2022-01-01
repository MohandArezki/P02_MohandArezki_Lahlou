import requests, csv, os, sys
from bs4 import BeautifulSoup
from ScrapeOneBook import getData, saveToFile, getImage

URL_SITE = 'http://books.toscrape.com/'   
FOLDER_DATA = 'books/'

books = []
index = 1
not_yet= True

while not_yet:
    print('Récuperation des données ......Page: '+str(index))
    
    url_page = URL_SITE + 'catalogue/page-'+str(index)+'.html'
    html_brut = requests.get(url_page)
    if html_brut.ok:
        soup = BeautifulSoup(html_brut.content,'lxml')
        # next  est en bas de chaque page, sauf la derniére
        not_yet = soup.find('li', attrs={'class':'next'})

        # recuperer les livres de lapage en cours
        books_page = soup.findAll("li","col-xs-6 col-sm-4 col-md-3 col-lg-3")
        for book in books_page:
            # récuperer le lien de la page du livre
            books.append(getData(URL_SITE+'catalogue/'+book.h3.a["href"]))
    index +=1
 
print('Données recupérées.')

# Extraction des données des livres dans un fichier csv
print('Génération du fichier CSV ......')
saveToFile('books/','AllBooks.csv',books)

print('Fichier CSV généré.')

# Extraction l'image associée au livre
index = 1
for book in books:
    print('Récuperation des images .Image '+str(index)+'/'+str(len(books)))
    getImage('books/',book.get("category"),book.get("image_url"),book.get("title"))
    index +=1

print('Traitement terminé.')
