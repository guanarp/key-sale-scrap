#importing packages
from selenium import webdriver #usar gecko
from selenium.webdriver.common.by import By #buscar por parametro
from selenium.webdriver.support.ui import WebDriverWait #permite esperar a la pag a que cargue
from selenium.webdriver.support import expected_conditions as EC #especificar que se busca de la pagina para determinar que ya cargo la pagina
from selenium.common.exceptions import TimeoutException #para manejar tiemouts

import pprint
import csv

browser = webdriver.Firefox()
wait = WebDriverWait(browser, 10)

def filtroEuros(titulo,precio,link,linkImg):
    index = 0
    print(titulo)
    for x in precio:
        if x.find(" EUR")!=-1:
            print("articulo borrado, en euros")
            print(titulo[index])
            print(index)
            del titulo[index],precio[index],link[index],linkImg[index]
            print(titulo)
        else:
            index+=1

def filtroRegion(titulo,precio,link,linkImg):
    index = 0
    for x in titulo:
        if x.find("GLOBAL")==-1:
            print("articulo borrado, no es global")
            print(titulo[index])
            print(index)
            del titulo[index],precio[index],link[index],linkImg[index]
        else:
            index+=1

def inicializador(contador):
    if contador ==1:
        get = browser.get("https://www.g2a.com/category/games-c189?drm[5]=1&banner=m1")
    elif contador >1:
        link = "https://www.g2a.com/category/games-c189?drm[5]=1&banner=m1" + "&page=" + str(contador) 
        get = browser.get(link)    

    # Wait 20 seconds for page to load
    timeout = 20

    #busca la img de background como ultima cosa a cargar, si no lo hace en 20 segs devuelve el error
    try:
        WebDriverWait(browser, timeout).until(EC.visibility_of_element_located((By.XPATH, "//img[@src='/en/assets/images/logo_g2a_white.svg']"))) 
    except TimeoutException:
        print("Timed out waiting for page to load")
        browser.quit()

    browser.execute_script("window.scrollTo(0, document.body.scrollHeight);") #esto lo que hace es hacer un scroll hasta el fondo una vez cargada toda la pag, para evitar perder informacion dinamicamente cargada, con un script de javasript                

def scrap(contador):

    # find_elements_by_xpath retorna un arreglo de objetos selenium.
    titulosElementos_steam = browser.find_elements_by_xpath("//h3[@class='Card__title']") #busca los titulos de los juegos, el xpath busca path, dice "busca la etiqueta h3 con el atributo class igual a card title"
    #busca la clase "card title" dentro de los h3
    titulos_steam = [str(i.text) for i in titulosElementos_steam] #saco los textos de los elementos en la lista

    #print("")
    #for x in range(len(titulos)):
    #    print(titulos[x])

    preciosElementos_steam = browser.find_elements_by_xpath("//span[@class='Card__price-cost price']") #lo mismo para precio
    precios_steam = [str(i.text) for i in preciosElementos_steam]


    linksElementos_steam = []
    links_steam = []
    for i in range(len(titulos_steam)):
        linksElementos_steam.append( browser.find_element_by_link_text(titulos_steam[i]) ) 
    for href in linksElementos_steam:
        links_steam.append( str(href.get_attribute("href")) )

    #print(links_steam) 

    linkImgElementos_steam = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, 'lazy-image__img'))) #espera a que se cargue
    linkImgElementos_steam = browser.find_elements_by_xpath("//img[@class='lazy-image__img']")
    linkImg_steam = []

    for src in linkImgElementos_steam: 
        if str(src.get_attribute("src")) != "None":
            linkImg_steam.append( str(src.get_attribute("src")) )
        else:
            linkImg_steam.append( str(src.get_attribute("data-src")) ) #para las imagenes que no carga por no estar en pantalla    

    filtroEuros(titulos_steam,precios_steam,links_steam,linkImg_steam)
    filtroRegion(titulos_steam,precios_steam,links_steam,linkImg_steam)

    #print(precios_steam)
    cotizacion_dolar = 6800 #a scrapear proximamente
    val = []
    preciosGs_steam = []
    for index in precios_steam:
        try:
            val.append( float(index.replace("USD","")) )
        except ValueError:
            continue    
    print(val)
    for j in val:
        preciosGs_steam.append (float(j) *1.3 * cotizacion_dolar)
    #print(preciosGs_steam)


    #print(len(titulos_steam))
    #print(len(precios_steam))

    for x in range(len(precios_steam)): #impresion titulo + precio
        print(titulos_steam[x] + " --- " + precios_steam[x])

def xlwriter(contador):
    scrap(contador)  
    try:
        if contador == 1:
            param = "wb"
        else:
            param = "a"  
        with open( "listaSteam.csv",param) as data_temp: #a de append , w de write, el newline="" (para python 3.x) hace que no haya filas de espacio entre los items, en python 2.x tengo que usar "wb"
            contador = 0
            nombrecolum = ["Titulo" , "Precio", "En Gs", "Link", "Img"]
            writer = csv.DictWriter(data_temp,nombrecolum)
            if contador == 0:
                writer.writeheader() #esto coloca header
                contador+=1
            #lo de arriba especifica el archivo con sus nombres de columnas
            for x in range(len(titulos_steam)):
                writer.writerow( {"Titulo":titulos_steam[x], "Precio": precios_steam[x],"En Gs":preciosGs_steam[x], "Link":links_steam[x], "Img": linkImg_steam[x], })
    except TypeError:
        if contador == 1:
            param = "w"
        else:
            param = "a"  
        with open( "listaSteam.csv",param,newline="") as data_temp: #a de append , w de write, el newline="" (para python 3.x) hace que no haya filas de espacio entre los items, en python 2.x tengo que usar "wb"
            contador = 0
            nombrecolum = ["Titulo" , "Precio", "En Gs", "Link", "Img"]
            writer = csv.DictWriter(data_temp,nombrecolum)
            if contador == 0:
                writer.writeheader() #esto coloca header
                contador+=1
            #lo de arriba especifica el archivo con sus nombres de columnas
            for x in range(len(titulos_steam)):
                writer.writerow( {"Titulo":titulos_steam[x], "Precio": precios_steam[x],"En Gs":preciosGs_steam[x], "Link":links_steam[x], "Img": linkImg_steam[x], })

