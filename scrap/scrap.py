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
######### les modules à utilser ############
import requests
# import de la bibliothéque Beautifullsoup
from bs4 import BeautifulSoup
import csv

def page_data(url):
    # Recuperer le contenu brut de la page
    html_brut = requests.get(url)
    # Pour savoir si un contenu a était renvoyé, on peut tester html_brut.ok  Ou html_brut.status_code = 200 
    if html_brut.ok:
        
        # Parser le code source enregistré dans html_brut : Changer le format de HTML vers un format facilement comprehensible par Python
        html = BeautifulSoup(html_brut.content,'lxml')

        # on recupére les données dans un dictionnaire
        results= {"product page url":"",
                  "Category":"","Titre":"","Product Description":"","UPC":[],"Product Type":"","Price (excl. tax)":"",
                  "Price (incl. tax)":"","Tax":"","Availability":"","Number of reviews":""}
        
        # URL de la page
        results['product page url'] = url

        # Dans le source HTML recuperé, le titre du livre est défini 
        # on recupere les elements de la liste [breadcrumb]
        list = html.find('ul', attrs={'class':'breadcrumb'})
    
        results['Category'] = list.find_all('a')[2].string 

        # dans la classe [col-sm-6 product_main] et dans le tag [h1] (titre de niveau 1)
        results['Titre'] = html.find(class_='col-sm-6 product_main').h1.text
            
        # Dans le source HTML recuperé, le titre du livre est défini 
        # dans la classe [col-sm-6 product_main] et dans le tag [h1] (titre de niveau 1)
        results['Product Description'] = html.find('p',class_='sub-header')

        # les reste des informations se trouve dans une table [table table-striped]
        table = html.find('table', attrs={'class': 'table table-striped'})
        
        # 1iere balise td, UPC
        results['UPC'] = table.find_all('td')[0].string                
        
        # 2iéme balise td, Product Type
        results['Product Type'] = table.find_all('td')[1].string       
        
        # 3iéme balise td, Price (excl. tax)
        results['Price (excl. tax)'] = table.find_all('td')[2].string 
        
        # 4iéme balise td, Price (incl. tax)
        results['Price (incl. tax)'] = table.find_all('td')[3].string  

        # 5iéme balise td, Tax
        results['Tax'] = table.find_all('td')[4].string                
        
        # 6iéme balise td, Availability
        results['Availability'] = table.find_all('td')[5].string       
        
        # 7iéme balise td, Number of reviews     
        results['Number of reviews'] = table.find_all('td')[6].string   
            
        return results

#appel de la fonction
url_page = 'http://books.toscrape.com/catalogue/tipping-the-velvet_999/index.html'
book = page_data(url_page)
book_info = book.items

# generer le fichier csv
filename = ("Book.csv")
f = open(filename, "w")
 
csv_headers = ["product page url","Category","Titre","Product Description","UPC", \
           "Product Type","Price (excl. tax)","Price (incl. tax)","Tax", \
           "Availability","Number of reviews\n"]
f.write(csv_headers)
writer = csv.writer(f)
for key, value in book.items():
    writer.writerow([value])


f.close()

https://appdividend.com/2019/11/14/how-to-write-python-dictionary-to-csv-example/