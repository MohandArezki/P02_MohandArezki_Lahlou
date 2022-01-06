# -*- coding: utf-8 -*-
from ScrapeCategory import *

def main():
    baseFolder = 'data/Site/'
    htmlSite = requests.get(URL_SITE)
    soupSite = BeautifulSoup(htmlSite.content,'html.parser')
    # les categories se trouve dans une liste "nav nav-list"
    categories = soupSite.find("ul","nav nav-list")
    # récuper tout les liens des catégories 
    # eviter de traiter la premiere page, on commence a partir de 2
    for url in categories.find_all('a',href=True)[2:]:
        # enlever la derniére partie de l'url
        urlCategory = URL_SITE+url["href"].rsplit("/", 1)[0]+'/'
        GetDataCategory(urlCategory,baseFolder)
    return

if __name__== '__main__':
    main()


