from ScrapeBook import *

# Une classe de simulation d'une categorie.
# une catégorie est caractérisée par :
# - Une URL (page_url)
# - Une liste de livres (books)
# - Un Nom (name)
class Category:
    def __init__(self,categoryPageUrl):
        URL_CATALOG = URL_SITE + 'catalogue/'
        FOLDER_BASE = 'data/Category/'
        self.page_url = categoryPageUrl
        self.books = []        
        index = 1
        # commencer par la premiere page de chaque catégorie (index.html)
        currentPage = 'index.html'
        # recupérer le contenu brut de la page 
        htmlCategory = requests.get(self.page_url+currentPage)
        # "parser" le contenu recuperer. rendre plus comprehensible le contenu recuperer par python 
        soupCategory = BeautifulSoup(htmlCategory.content,'html.parser')
        # recuperer le nom de la catgorie, qui est le titre de niveau 1 de la classe "page-header action"
        self.name = soupCategory.find(class_='page-header action').h1.text   
        doIt= True
        
        while doIt:
            # recuperer les livres de la page en cours, on recuperant la valeur de l'attribut "href"  du titre niveau 3 de 
            # de la classe "col-xs-6 col-sm-4 col-md-3 col-lg-3" sous forme d'une liste
            booksPage = soupCategory.find_all("li","col-xs-6 col-sm-4 col-md-3 col-lg-3")
            for book in booksPage:
                # récuperer le lien de la page du livre = URL_CATALOG + la valeur de l'attribut  "href" de l'element HTML "<a>"
                # enlever les 9 premiers caractéres pour reconstituer l'url 
                aBook = Book(URL_CATALOG+book.h3.a["href"][9:])
                aBook.saveData(FOLDER_BASE)
                # ajouter le livre dans la liste
                self.books.append(aBook)
            index +=1
            currentPage = 'page-'+str(index)+'.html'
            # "next"  est en bas de chaque page, sauf la derniére            
            doIt = soupCategory.find('li', attrs={'class':'next'})
            htmlCategory = requests.get(self.page_url+currentPage)
            soupCategory = BeautifulSoup(htmlCategory.content,'html.parser')
        return 
    
def main():
    # on recupere les informations de la categorie, on créant un objet (category) de type (Category) 
    # avec comme paramétre d'entrée l'URL de la page de la categorie
    URL_CATEGORY = URL_SITE + 'catalogue/category/books/mystery_3/'   
    category = Category(URL_CATEGORY)
    return
   
if __name__== '__main__':
    main()


