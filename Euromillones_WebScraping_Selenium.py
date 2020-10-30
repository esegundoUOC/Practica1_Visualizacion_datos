# -*- coding: utf-8 -*-
"""
Created on Sun Oct 25 08:05:45 2020

@author: Javier Plo
"""

""" Acciones previas"""

""" 1- Selenium Chrome:   download https://sites.google.com/a/chromium.org/chromedriver/downloads """

""" 2- pip install Beautifulsoup4 """
""" 3- pip install requests"""

import requests
from bs4 import BeautifulSoup
""" Para volcar listas en ficheros .csv importamos pandas"""
import pandas as pd
   
# Import the webdriver from selenium library 
from selenium import webdriver 
  
# Link the driver of the browser 
# D://Javier/Chromedriver/chromedriver.exe route included in path variable

# Code to don't open the browser

option = webdriver.ChromeOptions()
option.add_argument('headless')


driver = webdriver.Chrome(options=option) 
      
# Open the website  using url 

eurourl="https://www.euromillones.com.es/historico/euromillones-anos-anteriores.html"

driver.get(eurourl)


# Finding links with xpath 
Enlaces = driver.find_elements_by_xpath('//article/table/tbody/tr/td/a[contains(@href,"historico/")]')


listasorteos = []

words = ["*", "SEM.", "NÚMEROS", "Lluvia de Millones","FECHA","SORTEO","COMBINACION GANADORA","2010","2009","2008","2007","2006","2005","2004","ESTRELLAS"]               

for x in range(0,len(Enlaces)):

  
    
    page = requests.get(Enlaces[x].get_attribute('href'))
    soup = BeautifulSoup(page.content, features="lxml")
    yeartitle = soup.table.caption.text
    year = yeartitle[-4:]
    
    # Accedemos a la tabla de los sorteos
    tabla = soup.table.find('tbody')
    
    # Obtenemos todas las filas de la tabla. Cada fila corresponde a un sorteo.
    filas = tabla.find_all('tr')
     
    """for fila in filas:
         cols = fila.find_all('td')         
         children = cols.findChildren('br')
         print(children)
         fila.extract() """
        
                
  
    
    semana = 1
    
    for fila in filas:     
         # Ignoramos las filas que no nos interesan
        if fila.find('td') and (fila.find('td', attrs={'colspan':'9'}) == None) and any(word in fila.td.text for word in words) == False:
     
            sorteo = [year]
            
        
        
            # Algunas semanas tienen más de un sorteo a la semana
            if ((fila.find('td', attrs={'rowspan':'2'}) != None) or (int(year) < 2011) or (int(year) == 2011 and int(semana) < 19)) or (fila.find('td', attrs={'rowspan':'4'}) != None):
                
                    semana = fila.td.text
              
            else:            
                
                
                    sorteo.append(semana)                    
                  
        
                        
            
            # Eliminamos las columnas que contienen algún campo en blanco
            """for filaaborrar in fila.find_all('td') :
                if filaaborrar.findChild() == "":
                   print(filaaborrar)
                   filaaborrar.extract()"""
                    
            # Obtenemos todas las columnas de la fila
            cols = fila.find_all('td')
            
            """for elem in fila.find_element_by_xpath('td/br', ''):
                    elem.extract()"""
            
                            
            
            
            """flagdeleterow = 0
            index = 0
            colindex = 0
            
            for valcolumna in cols:
                index = index + 1
                if len(valcolumna.get_text(strip=True)) == 0:
                    colindex = index
                    flagdeleterow = 1
                    break
                    
            if flagdeleterow == 1:
                cols[colindex].extract()"""
                
                             
            for valorcolumna in cols:               
                numero = valorcolumna.text
                if numero != '\n':
                    sorteo.append(numero)
    
    
        
            # Algunos años no tienen campo "Semana" (aquellos que solo tienen un sorteo por semana)
            # Añadimos un valor igual al número de sorteo que corresponde al número de semana
            if len(sorteo) == 10:
                    sorteo.insert(1, sorteo[1])
                    
            # Algunos años no tienen campo "ElMillon"
            if len(sorteo) < 12:
                    sorteo.append('')
                
            # Guardamos los resultados de la fila a la lista 'data'
            listasorteos.append(sorteo)        
         
# Creamos el dataframe en el que guardaremos los datos    
df = pd.DataFrame(listasorteos, columns=["Anyo","Semana","Sorteo","Fecha","Numero1","Numero2","Numero3","Numero4","Numero5","Estrella1","Estrella2","ElMillon"])


print(df.head(10))    

   
# Guardamos los datos en un fichero csv
df.to_csv('Resultados_Euromillones.csv', index=False) 
    
                
    
    
    

    





       
       
    



  

