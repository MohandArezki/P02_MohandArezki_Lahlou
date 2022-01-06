# -*- coding: utf-8 -*-
from ScrapeBook import *


def GetDataCategory(urlPage,folder):
    index = 1
    # commencer par la premiere page de chaque catégorie (index.html)
    currentPage = 'index.html'
    # recupérer le contenu brut de la page 
    htmlCategory = requests.get(urlPage+currentPage)
    # "parser" le contenu recuperer. rendre plus comprehensible le contenu recuperer par python 
    soupCategory = BeautifulSoup(htmlCategory.content,'html.parser')
    doIt= True
    while doIt:
        # recuperer les livres de la page en cours, on recuperant la valeur de l'attribut "href"  du titre niveau 3 de 
        # de la classe "col-xs-6 col-sm-4 col-md-3 col-lg-3" sous forme d'une liste
        booksPage = soupCategory.find_all("li","col-xs-6 col-sm-4 col-md-3 col-lg-3")
        for book in booksPage:
            # récuperer le lien de la page du livre = URL_SITE + 'catalogue/' + la valeur de l'attribut  "href" de l'element HTML "<a>"
            # enlever les 9 premiers caractéres pour reconstituer l'url 
            aBook = Book(URL_SITE + 'catalogue/'+book.h3.a["href"][9:])
            aBook.saveData(folder)
            index +=1
            currentPage = 'page-'+str(index)+'.html'
            # "next"  est en bas de chaque page, sauf la derniére            
            doIt = soupCategory.find('li', attrs={'class':'next'})
            htmlCategory = requests.get(urlPage+currentPage)
            soupCategory = BeautifulSoup(htmlCategory.content,'html.parser')
    return 
    
def main():
    baseFolder = 'data/Category/'
    # on recupere les informations de la categorie,
    urlCategory = URL_SITE + 'catalogue/category/books/mystery_3/'   
    GetDataCategory(urlCategory,baseFolder)
    return
   
if __name__== '__main__':
    main()


