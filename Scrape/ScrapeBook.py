
import requests,csv, os
from slugify import slugify 
from bs4 import BeautifulSoup

URL_SITE = 'http://books.toscrape.com/'

# Une classe de simulation d'un livre.
# Un livre est caractérisé par :
# product_page_url  
# image_url 
# category   
# title 
# product_description
# universal_product_code
# price_excluding_tax
# price_including_tax
# number_available
# review_rating
# Toutes ces données sont enregistré dans un dictionnaire (data)
class Book:
    def __init__(self,bookPageUrl):
        self.data ={}
        self.data ={'product_page_url':bookPageUrl}
        # Recuperer le contenu brut de la page
        html_brut = requests.get(self.data['product_page_url'])
        # Pour savoir si un contenu a était renvoyé, on peut tester html_brut.ok  Ou html_brut.status_code = 200 
        # Parser le code source enregistré dans html_brut : Changer le format de HTML vers un format facilement comprehensible par Python
        bookSoup = BeautifulSoup(html_brut.content,'html.parser')
        # recupérer les données dans un dictionnaire
        # URL de l'image
        self.data['image_url']= requests.compat.urljoin(URL_SITE, bookSoup.findAll('img')[0].attrs['src'])
        # recuperer les elements de la liste [breadcrumb]
        list = bookSoup.find('ul', attrs={'class':'breadcrumb'})
        self.data['category'] = list.find_all('a')[2].string 
        # dans la classe [col-sm-6 product_main] et dans le tag [h1] 
        self.data['title'] = bookSoup.find(class_='col-sm-6 product_main').h1.text
        # la description , c'est le 4ieme paragraphe [p]
        self.data['product_description'] = bookSoup.select('p')[3].text
        # les reste des informations se trouve dans une table [table table-striped]
        table = bookSoup.find('table', attrs={'class': 'table table-striped'})
        # 1iere tag td, UPC
        self.data['universal_product_code'] = table.find_all('td')[0].string                
        # 3iéme balise td, Price (excl. tax)
        self.data['price_excluding_tax'] = table.find_all('td')[2].string 
        # 4iéme balise td, Price (incl. tax)
        self.data['price_including_tax'] = table.find_all('td')[3].string  
        # 6iéme balise td, Availability
        self.data['number_available'] = table.find_all('td')[5].string       
        # 7iéme balise td, Number of reviews     
        self.data['review_rating'] = table.find_all('td')[6].string
        return
    
    # methode pour recuperer les images du livre Et        
    # exporter les données d'un livre dans un csv
    def saveData(self,folder):
        print('Récuperation des données. Catégorie : ('+self.data['category']+')/Livre :'+self.data['title'])
        #generation de la structure dossier + dossier pour les Images
        folder = folder+slugify(self.data['category'])+'/'
        os.makedirs(folder, exist_ok=True)
        # generer un nom de dossier pour les images valide a partir du nom de la categorie
        # generer un nom valide pour le fichier image (le nom du produit comme nom d'image) 
        #Créer un objet  (f) pour le fichier image
        with open(folder+slugify(self.data['title'])+".jpg", 'wb') as f:
            # telecharger l'image
            f.write(requests.get(self.data['image_url']).content)
        # Créer un objet  (f) pour le fichier csv       
        csvFile=folder+'/file.csv'
        if not os.path.isfile(csvFile): 
            with open(csvFile, 'w',encoding='utf8') as f:
                # Passer l'objet (f) à la fonction Dictwriter()pour récuperer un objet DictWriter (writer)
                # les nom des champs sont les clés du dictionnaire sel.data
                # créer l'entete
                writer = csv.DictWriter(f, fieldnames=self.data.keys(),quoting=csv.QUOTE_ALL)
                writer.writeheader()
        with open(csvFile, 'a',encoding='utf8') as f:
            # Passer l'objet (f) à la fonction Dictwriter()pour récuperer un objet DictWriter (writer)
            # les nom des champs sont les clés du dictionnaire sel.data
            # writer = csv.DictWriter(f, fieldnames = self.data.keys())
            writer = csv.DictWriter(f, fieldnames=self.data.keys(),quoting=csv.QUOTE_ALL)
            # Passer  le dictionnaire self.data  comme paramétre de la fonction  writerow()
            writer.writerow(self.data)
        return
        
def main():
    baseFolder = 'data/book/'
    # recuperer les informations du livre, on créant un objet (book) de type (Book) 
    # avec comme paramétre d'entrée l'URL de la page du livre
    urlBook = URL_SITE+'/catalogue/tipping-the-velvet_999/index.html'
    book=Book(urlBook)
    # exporter les données du livre vers un fichier csv
    book.saveData(baseFolder)
    return 
      
if __name__== '__main__':
    main()
