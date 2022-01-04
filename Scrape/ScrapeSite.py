
from ScrapeCategory import *

class Site:
    def __init__(self):
        self.categories = []
        htmlSite = requests.get(URL_SITE)
        soupSite = BeautifulSoup(htmlSite.content,'html.parser')
        #les categories se trouve dans une liste "nav nav-list"
        categories = soupSite.find("ul","nav nav-list")
        #récuper tout les liens des catégories 
        #eviter de traiter la premiere page, on commence a partir de 2
        for url in categories.find_all('a',href=True)[2:]:
                # enlever la derniére partie de l'url
                urlCategory = URL_SITE+url["href"].rsplit("/", 1)[0]+'/'
                self.categories.append(Category(urlCategory))
        return
    
    def getData(self):
        data = []
         #on parcour les categories  
        for category in self.categories:
            #on recupere les données la categorie
            category.append(category.getData())
        return data

    def saveImages(self,folder):
          # on parcour la liste des categories
        for category in self.categories:
            # on recupere les images de la categorie
            category.saveImage(folder)
        return     
   
    def saveData(self,folder):
        #on parcour la liste des categories
        for category in self.categories:
            # on ajoute les données la categorie
            category.saveData(folder)
        return     
    

def main():
    FOLDER_BASE = 'data/Site/'
    site = Site()
    
    # exporter les données de la catéggorie dans un fichier csv
    site.saveData(FOLDER_BASE)

    #recuperer les images
    site.saveImages(FOLDER_BASE)
    return

if __name__== '__main__':
    main()


