import os
from logging import setLoggerClass
import unittest
from selenium import webdriver
from time import sleep
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from csv import writer

order_by_default_option_CyberPuerta = []

search_products = []

order_by_options = ["Relevancia","Nombre Z-A","Nombre A-Z", "Mayor precio", "Menor precio", "Disponibilidad", "Más nuevos", "Mejor calificación"]

def get_search_items():
    search_product = input("¿🎃 Qué producto desea buscar 🎃? ")
    search_products.append(search_product)
    search_product = ""

    while search_product.lower() != 'n':
        os.system ("cls") 
        search_product = input("""  ¿🎃 Qué producto desea buscar 🎃? 
        Para dejar de buscar seleccione la opcion 'N':""")
        if(search_product != 'n'):
            search_products.append(search_product)
    #print(search_products)
    correct_type = False
    while correct_type == False:
        try:
            order_by_default = int(input("""¿En que orden le gustaria ordenar los productos?
                1. Relevancia
                2. Nombre Z-A
                3. Nombre A-Z
                4. Mayor precio
                5. Menor precio
                6. Disponibilidad
                7. Más nuevos
                8. Mejor calificación
            """))
            
            order_by_default_option_CyberPuerta.append(order_by_options[order_by_default-1])
            correct_type = True
            print("order", order_by_default_option_CyberPuerta)

        except:
            os.system ("cls") 
            continue


def create_dir(dir_name):
    path = os.getcwd()
    exist = os.path.exists(path+"/"+dir_name)
    if not exist:
        os.makedirs(path+"/"+dir_name)
    
    return str(path + "/" + dir_name)


def write_csv_file(dir_path, list_items, search_product):

    with open(dir_path+"/"+search_product+".csv",'w') as file:
        csv_file = writer(file, lineterminator='\n')
        header = ('Prodcuto','Precio','Link')
       
        csv_file.writerow(header)

        for i in range(len(list_items["item_name"])):
            name_contains = list_items["item_name"][i]
            name_contains.find
            
            row = (list_items["item_name"][i],list_items["item_price"][i],list_items["item_link"][i])

            try:
                csv_file.writerow(row)
            except:
                row = ("Error al escribir el nombre",list_items["item_price"][i],list_items["item_link"][i])
                csv_file.writerow(row)


class HomePageTests(unittest.TestCase):

    def setUp(self):
        get_search_items()
        driver = webdriver.Chrome("./chromedriver.exe")
        self.driver = driver
        driver.get('https://www.cyberpuerta.mx/')
        driver.maximize_window()

    def test_home_page(self):
        dirs_path = create_dir("Cyber Puerta")
        driver = self.driver
        print("Hola: ",order_by_default_option_CyberPuerta[0])
        for product in search_products:
            #input para buscar
            input_search = driver.find_element_by_xpath('//*[@id="cp-header-search"]/form/input[2]')
            input_search.clear()
            input_search.send_keys(product)

            #boton de busqueda
            button_search = driver.find_element_by_xpath('//*[contains(concat( " ", @class, " " ), concat( " ", "largeButton", " " ))]')
            button_search.click()
            sleep(3)

            #meter una promesa aqui
            
            try: 
                order_by = driver.find_element_by_class_name('emdropdownicon')
                order_by.click()

                order_by_keyword = driver.find_element_by_xpath('//*[@id="emselectbox_sort"]/div[@class = "emdropdownitems"]/div/div[contains(.,"'+order_by_default_option_CyberPuerta[0]+'")]')
                order_by_keyword.click()
                sleep(6)

                items = driver.find_elements_by_xpath('//*[@id="productList"]/li')

                if(len(items) == 0):
                    items = driver.find_elements_by_xpath('//*[@id="searchList"]/li')
                
                print("Items encontrados: ", len(items))

                list_item = {
                    "item_name":[],
                    "item_price":[],
                    "item_link":[]
                }

                for item in items:
                    stock_item = item.find_element_by_xpath(('.//div/form/div[@class = "emproduct_right"]/div[@class]/div[@class = "emproduct_right_price"]/div[@class = "clear"]/div[@class="emproduct_right_price_left"]/div[@class = "emstock"]/span')).text
                    if(stock_item != "Producto agotado"):
                        item_name = item.find_element_by_xpath('.//div/form/div[@class = "emproduct_right"]/a').text
                        item_url = item.find_element_by_xpath('.//div/form/div[@class = "emproduct_right"]/a').get_attribute('href')
                        item_price = item.find_element_by_xpath('.//div/form/div[@class = "emproduct_right"]/div[@class]/div[@class = "emproduct_right_price"]/div[@class = "clear"]/div[@class="emproduct_right_price_left"]/label').text

                        list_item["item_name"].append(item_name)
                        list_item["item_price"].append(item_price)
                        list_item["item_link"].append(item_url)

                write_csv_file(dirs_path, list_item, product)
            except:
                continue



    def tearDown(self):
        self.driver.close()

    
if __name__ == "__main__":
    unittest.main(verbosity = 2)