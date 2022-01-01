########### Nous allons recuperer mes données d'un seul livre #########################
#   http://books.toscrape.com/
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
import requests,csv, os
from slugify import slugify 
# import de la bibliothéque Beautifullsoup
from bs4 import BeautifulSoup

URL_PAGE = 'http://books.toscrape.com/catalogue/tipping-the-velvet_999/index.html'
URL_SITE = 'http://books.toscrape.com/'   
FOLDER_DATA = 'book/'

    
def getData(url):
    # Recuperer le contenu brut de la page
    html_brut = requests.get(url)
    results ={}
    # Pour savoir si un contenu a était renvoyé, on peut tester html_brut.ok  Ou html_brut.status_code = 200 
    if html_brut.ok:
        
        # Parser le code source enregistré dans html_brut : Changer le format de HTML vers un format facilement comprehensible par Python
        soup = BeautifulSoup(html_brut.content,'lxml')

        # on recupére les données dans un dictionnaire
        results= {"product_page_url":"",
                  "image_url":"",
                  "category":"","title":"","product_description":"","universal_ product_code (upc)":"","price_excluding_tax":"",
                  "price_including_tax":"","number_available":"","review_rating":""}
        
        # URL de la page
        results['product_page_url'] = url
        # URL de l'image
        results["image_url"]= soup.findAll('img')[0].attrs['src']

        # Dans le source HTML recuperé, le titre du livre est défini 
        # on recupere les elements de la liste [breadcrumb]
        list = soup.find('ul', attrs={'class':'breadcrumb'})
    
        results['category'] = list.find_all('a')[2].string.lstrip() 

        # dans la classe [col-sm-6 product_main] et dans le tag [h1] 
        results['title'] = soup.find(class_='col-sm-6 product_main').h1.text.lstrip()
            
        # la description , c'est le 4ieme paragraphe [p]
        results['product_description'] = soup.select('p')[3].text.lstrip()
               
        # les reste des informations se trouve dans une table [table table-striped]
        table = soup.find('table', attrs={'class': 'table table-striped'})
        
        # 1iere tag td, UPC
        results['universal_ product_code (upc)'] = table.find_all('td')[0].string.lstrip()                 
        
        # 3iéme balise td, Price (excl. tax)
        results['price_excluding_tax'] = table.find_all('td')[2].string.lstrip() 
        
        # 4iéme balise td, Price (incl. tax)
        results['price_including_tax'] = table.find_all('td')[3].string.lstrip()  

        # 6iéme balise td, Availability
        results['number_available'] =  table.find_all('td')[5].string.strip('In stock () available')      
        
        # 7iéme balise td, Number of reviews     
        results['review_rating'] = table.find_all('td')[6].string.lstrip()
    return results

def saveToFile(folder,fileName,dict):
    
    # on crée le dossier s il n 'existe pas 
    os.makedirs(folder, exist_ok=True)
    fileName = folder+ fileName
    
    # créer le fichier dans le dossier csv
    with open(fileName, 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames = dict[0].keys())
        writer.writeheader()
        writer.writerows(dict)
    return

def getImage(folderData,category,urlImg,nameImg):
    
    # recuperer le chemin complet de l'image
    urlImg = requests.compat.urljoin(URL_SITE,urlImg)
    
    # generer le nom du dossier de sauvegarde des images  
    # generer le nom de l'image (le nom du produit comme nom d'image)
    folderData = folderData+'/img/'+slugify(category)+'/'  
    nameImg =folderData + slugify(nameImg)+".jpg"
    # on crée  le dossier et le sous dossier s'il n'existe pas
    os.makedirs(folderData, exist_ok=True)
    # si le fichier n existe pas, on le telecharge       
    if not os.path.isfile(nameImg):
        # telecharger l'image
        with open(nameImg, 'wb') as f:
            f.write(requests.get(urlImg).content)
    return

def main():
    book = []
    # Récuperation des données sur le livre
    book.append(getData(URL_PAGE))
   
    # Extraction des données du livre dans un fichier csv
    saveToFile('book/','book.csv',book)
    
    # Extraction l'image associée au livre
    getImage('book/',book[0].get("category"),book[0].get("image_url"),book[0].get("title"))
    return

if __name__== '__main__':
    main()