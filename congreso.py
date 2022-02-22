from selenium.webdriver.support.ui import Select
from selenium import webdriver
from webdriver_manager.firefox import GeckoDriverManager
import requests
from bs4 import BeautifulSoup
import csv
import pandas as pd

link_congresista=""
link=""
nombre_congresistas=""
votacion_obtenida=""
periodo_funciones=""
periodo_inicio=""
periodo_fin=""
grupo_partido=""
bancada=""
representa=""
condicion=""
periodo_parlamentario=""


driver = webdriver.Firefox(executable_path=GeckoDriverManager().install())
driver.get('https://www.congreso.gob.pe/pleno/congresistas/')

for x in range(1,8):
    select_periodo_parlamentario = Select(driver.find_element_by_name('idRegistroPadre'))
    select_periodo_parlamentario.select_by_value(str(x)) #Pass value as string
    
    select_condicion = Select(driver.find_element_by_name('fld_13_Condicion'))
    select_condicion.select_by_index(0)
    
    page_source = driver.page_source
    soup = BeautifulSoup(page_source, "lxml")
    
    periodo_parlamentario = soup.find('select',attrs={"name":"idRegistroPadre"}).find('option',attrs={"value":str(x)}).text
    print("\n")
    print(periodo_parlamentario)
    
    for tr in soup.find_all("tr"):
        for td in tr.find_all("td"):
            if td.find('a',attrs={"class": "conginfo"}): 
                
                link_congresista=td.find('a')
                link='https://www.congreso.gob.pe/pleno/congresistas/'+link_congresista.get('href')
                        
                #Sopa de las paginas de los congresistas
                pagina_congresista = requests.get(link).text 
                sopa_congreso = BeautifulSoup(pagina_congresista, "lxml")
                        
                #Extracción de valores
                nombre_congresistas=sopa_congreso.find('p',attrs={"class": "nombres"}).find('span',attrs={"class": "value"}).text
                print("\nNombres:",nombre_congresistas)
                
                votacion_obtenida=sopa_congreso.find('p',attrs={"class": "votacion"}).find('span',attrs={"class": "value"}).text
                print("Votación Obtenida:",votacion_obtenida)
                
                periodo_funciones=sopa_congreso.find('p',attrs={"class": "periodo"})
                for tag in periodo_funciones.findAll('span', attrs={'class': 'periododatos'}):
                    if tag.find('span', attrs={'class':'field'}).text == "Inicio:":
                        new_tag = tag.find('span', attrs={'class': 'value'})
                        periodo_inicio=new_tag.text
                        print("Inicio:",periodo_inicio)
                    if tag.find('span', attrs={'class':'field'}).text == "Término:":
                        new_tag = tag.find('span', attrs={'class': 'value'})
                        periodo_fin=new_tag.text
                        print("Termino:",periodo_fin)
                
                grupo_partido=sopa_congreso.find('p',attrs={"class": "grupo"}).find('span',attrs={"class": "value"}).text
                print("Grupo o Partido Político:",grupo_partido)
                
                bancada=sopa_congreso.find('p',attrs={"class": "bancada"}).find('span',attrs={"class": "value"}).text
                print("Bancada:",bancada)
                
                representa=sopa_congreso.find('p',attrs={"class": "representa"}).find('span',attrs={"class": "value"}).text
                print("Representa a:",representa)
                
                condicion=sopa_congreso.find('p',attrs={"class": "condicion"}).find('span',attrs={"class": "value"}).text
                print("Condición:",condicion)
                
                print("Periodo Parlamentario:", periodo_parlamentario)
                
                with open('congresistas.csv', 'a', newline='') as csv_file:
                    writer = csv.writer(csv_file)
                    writer.writerow([nombre_congresistas,votacion_obtenida,periodo_inicio,periodo_fin,grupo_partido,bancada,representa,condicion,periodo_parlamentario])
                    
    print("\nPeriodo Completado")
print("Extraccion completa")

df = pd.read_csv("congresistas.csv", header=None, sep= ',',encoding='ISO-8859-1')
df.columns = ["nombre_congresistas","votacion_obtenida","inicio","termino","grupo_partido","bancada","representa","condicion","periodo_parlamentario"]
