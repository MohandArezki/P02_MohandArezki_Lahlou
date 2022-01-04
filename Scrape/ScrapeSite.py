
from ScrapeCategory import *

class Site:
    def __init__(self):
        self.categories = []
        htmlSite = requests.get(URL_SITE)
        soupSite = BeautifulSoup(htmlSite.content,'html.parser')
        # les categories se trouve dans une liste "nav nav-list"
        categories = soupSite.find("ul","nav nav-list")
        # récuper tout les liens des catégories 
        # eviter de traiter la premiere page, on commence a partir de 2
        for url in categories.find_all('a',href=True)[2:]:
                # enlever la derniére partie de l'url
                urlCategory = URL_SITE+url["href"].rsplit("/", 1)[0]+'/'
                self.categories.append(Category(urlCategory))
        return
  
    # methode pour recuperer les données des livres        
    def getData(self):
        data = []
        # on parcour les categories  
        for category in self.categories:
            # recuperer les données la categorie
            category.append(category.getData())
        return data
    
    # methode pour recuperer les images des livres        
    def saveImages(self,folder):
          # parcourir la liste des categories
        for category in self.categories:
            # recuperer les images de la categorie
            category.saveImage(folder)
        return     

    # methode pour exporter les données des livres dans un csv
    def saveData(self,folder):
        # parcourir la liste des categories
        for category in self.categories:
            # ajouter les données la categorie
            category.saveData(folder)
        return     
 
def main():
    FOLDER_BASE = 'data/Site/'
    site = Site()
    # exporter les données de la catéggorie dans un fichier csv
    site.saveData(FOLDER_BASE)
    # recuperer les images
    site.saveImages(FOLDER_BASE)
    return

if __name__== '__main__':
    main()


