########### Nous allons recuperer mes données d'un seul livre #########################
#   site to scrap
#   http://books.toscrape.com/
#
#   recuperer les données pour un seul livre
#
#   csv file structure
#
#   product_page_url
#   universal_ product_code (upc)
#   title
#   price_including_tax
#   price_excluding_tax
#   number_available
#   product_description
#   category
#   review_rating
#   image_url
#
######### les module à utilser ############
import requests
# Nous allons importé la bibliothéque Beautifullsoup
from bs4 import BeautifulSoup

######## Ou est ce que va se connecter  ? ############
url = 'http://books.toscrape.com/catalogue/tipping-the-velvet_999/index.html'
# Recuperer le contenu brut de la page
html_brut = requests.get(url)
# Pour savoir si un contenu a était renvoyé, on peut tester html_brut.ok  Ou html_brut.status_code = 200 
if html_brut.ok:
    # Parser le code source enregistré dans html_brut : Changer le format de HTML vers un format facilement comprehensible par Python
    html = BeautifulSoup(html_brut.content,'lxml')
    # dans le source HTML recuperé, le titre du livre est défini 
    # dans la classe [col-sm-6 product_main] et dans le tag [h1] (titre de niveau 1)
    title = html.find(class_='col-sm-6 product_main').h1.text 
    print(title)
    description = html.find(class_='sub-header').p.text
    print (description)

    # les reste des informations se trouve dans une table [table table-striped]
    # on recupere les differentes colonnes
    
     #rechercher image_url
    #table = soup.find('div',attrs ={'id':'product_description'})
    #product_description =
    # product_page_url = url
    # universal_product_code = UPC
    #title = 
    #price_including_tax = Price (incl. tax)
    #price_excluding_tax = Price (excl. tax)
    #number_available = Availability
    #product_description = product_description
    #category
    #review_rating = Number of reviews
    #image_url ="item active"