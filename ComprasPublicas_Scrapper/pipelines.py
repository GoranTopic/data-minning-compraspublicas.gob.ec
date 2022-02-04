# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

# useful for handling different item types with a single interface
from scrapy.pipelines.files import FilesPipeline
from itemadapter import ItemAdapter
from dotenv import dotenv_values
import os

class CompraspublicasScrapperPipeline():
    env = dotenv_values('.env')

    if env['DEST_FOLDER'] is not None:
        dest = os.path.join( env['DEST_FOLDER'], env['DOMAIN'])
    else: 
        dest = env['DOMAIN']

    tab_types = { 
            '1' : 'Descripción', 
            '2' : 'Fechas', 
            '3' : 'productos', 
            '4' : 'Parámetros de Calificación', 
            '5' : 'Historial de respuestas', 
            '6' : 'Archivos', }

    def open_spider(self, spider):
        self.make_folder(self.dest)

    def close_spider(self, spider):
        #self.file.close()
        pass

    def make_folder(self, folder):
        if not os.path.exists(folder):
            os.makedirs(folder)

    def create_url_file(self, item):
        # get url
        base_url ='https://www.compraspublicas.gob.ec/ProcesoContratacion/compras/PC/informacionProcesoContratacion2.cpe?idSoliCompra='
        url = base_url + self.project['ID']
        # craft file path
        filename = os.path.join(
                self.dest, 
                self.code_folder,
                f"{self.code_folder}.url")
        _file = open(filename, "w")
        _file.write(f"[InternetShortcut]\nURL={url}")
    

    def create_html_file(self, item):
        body = item['body']
        # make folder
        self.make_folder(
                os.path.join(
                    self.dest, 
                    self.code_folder, 
                    self.tab_folder))
        # filename path
        filename = os.path.join(self.dest, 
                self.code_folder,
                self.tab_folder,
                f"{self.tab_folder}.html")
        # create file 
        open(filename, "w").write(str(body, 'UTF-8'))

    def create_folders(self):
        # get code folder name
        self.code_folder = self.project["code"]
        # get tab folder name
        self.tab_folder = self.tab_types[f'{self.tab_num}']
        # make folders
        self.make_folder(
                os.path.join(self.dest, self.code_folder))
        # get file path 
        self.make_folder(
                os.path.join(self.dest, self.code_folder, self.tab_folder))

    def process_item(self, item, spider):
        # get the proects data passed
        self.body = item['body']
        self.project = item['project']
        self.tab_num = item['tab_num']
        # make folders
        self.create_folders()
        # make url file
        self.create_url_file(item)
        # make html file
        self.create_html_file(item)
        # return file
        return item


class FilesPipeline(FilesPipeline):
    tab_types = { 
            '1' : 'Descripción', 
            '2' : 'Fechas', 
            '3' : 'productos', 
            '4' : 'Parámetros de Calificación', 
            '5' : 'Historial de respuestas', 
            '6' : 'Archivos', }


        #self.file.close()
        pass

    def make_folder(self, folder):
        if not os.path.exists(folder):
            os.makedirs(folder)

    def create_url_file(self, item):
        # get url
        base_url ='https://www.compraspublicas.gob.ec/ProcesoContratacion/compras/PC/informacionProcesoContratacion2.cpe?idSoliCompra='
        url = base_url + self.project['ID']
        # craft file path
        filename = os.path.join(
                self.dest, 
                self.code_folder,
                f"{self.code_folder}.url")
        _file = open(filename, "w")
        _file.write(f"[InternetShortcut]\nURL={url}")
    

    def create_html_file(self, item):
        body = item['body']
        # make folder
        self.make_folder(
                os.path.join(
                    self.dest, 
                    self.code_folder, 
                    self.tab_folder))
        # filename path
        filename = os.path.join(self.dest, 
                self.code_folder,
                self.tab_folder,
                f"{self.tab_folder}.html")
        # create file 
        open(filename, "w").write(str(body, 'UTF-8'))

    def create_folders(self):
        # get code folder name
        self.code_folder = self.project["code"]
        # get tab folder name
        self.tab_folder = self.tab_types[f'{self.tab_num}']
        # make folders
        self.make_folder(
                os.path.join(self.dest, self.code_folder))
        # get file path 
        self.make_folder(
                os.path.join(self.dest, self.code_folder, self.tab_folder))

    def process_item(self, item, spider):
        # get the proects data passed
        self.body = item['body']
        self.project = item['project']
        self.tab_num = item['tab_num']
        # make folders
        self.create_folders()
        # make url file
        self.create_url_file(item)
        # make html file
        self.create_html_file(item)
        # return file
        return item



