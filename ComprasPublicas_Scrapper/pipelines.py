# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

# useful for handling different item types with a single interface
from scrapy.pipelines.files import FilesPipeline
from ComprasPublicas_Scrapper import params
import mimetypes
import traceback
import os
import re

if params.dest_folder is not None:
    dest = os.path.join( params.dest_folder, params.domain )
else: 
    dest = params.domain

tab_types = { 
        '1' : 'Descripción', 
        '2' : 'Fechas', 
        '3' : 'productos', 
        '4' : 'Parámetros de Calificación', 
        '5' : 'Historial de respuestas', 
        '6' : 'Archivos', }

class CompraspublicasScrapperPipeline:
    tab_types = tab_types
    dest = dest

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
        base_url = params.procesos_url
        url = base_url + self.project['ID']
        # craft file path
        filename = os.path.join(
                self.dest, 
                self.code_folder,
                f"{self.code_folder}.url")
        with open(filename, "w") as file:
            file.write(f"[InternetShortcut]\nURL={url}")

    def create_html_file(self, item):
        # filename path
        if(self.isResume):
            filename = os.path.join(self.dest, 
                    self.code_folder,
                    self.tab_folder,
                    'resumen_contractual')
        else:
            filename = os.path.join(self.dest, 
                    self.code_folder,
                    self.tab_folder,
                    f"{self.tab_folder}.html")
        # create file 
        with open(filename, "w") as file:
            file.write(str(self.body, 'UTF-8'))
        

    def create_folders(self):
        # get code folder name
        self.code_folder = self.project["code"]
        # get tab folder name
        if(self.isResume):
            self.tab_folder = 'resumen_contractual'
        else:
            self.tab_folder = self.tab_types[f'{self.tab_num}']
        # make folders
        self.make_folder(
                os.path.join(self.dest, self.code_folder))
        # get file path 
        self.make_folder(
                os.path.join(self.dest, self.code_folder, self.tab_folder))

    def process_item(self, item, spider):
        # get the project data passed
        self.body = item['response'].body
        self.project = item['project']
        self.isResume = item['isResume']
        self.tab_num = item['tab_num']

        # make folders
        self.create_folders()
        # make url file
        self.create_url_file(item)
        # make html file
        self.create_html_file(item)
        # return file
        return item

class CompraspublicasFilePipeline(FilesPipeline):
    # if download folde is not specified, make folder with the domain's name
    tab_types = tab_types
    dest = dest

    _content_disposition_regex = [
        re.compile(';\s*[fF][iI][lL][eE][nN][aA][mM][eE]\*=[^;]+(\.[^;]+)'),
        re.compile(';\s*[fF][iI][lL][eE][nN][aA][mM][eE]=[^;]+(\.[^;]+)'),
    ]

    def file_path(self, request, response=None, info=None, item=None):
        try: 
            code_folder = item['project']['code']
            tab_folder = self.tab_types[f"{item['tab_num']}"]
            for meta in item['files_meta']:
                if(request.url == meta['url']):
                    title = meta['title']
            # ge the filename
            media_ext=''
            filename = os.path.join( code_folder, tab_folder, f"{title}") 
            if response is not None:
                if 'Content-Type' in response.headers:
                    media_ext_guess = mimetypes.guess_extension(
                            str(response.headers.get('Content-Type'), 'UTF-8'))
                if not media_ext_guess and 'Content-Disposition' in response.headers:
                    for regex in self._content_disposition_regex:
                        media_ext_guess = regex.findall(
                                str(response.headers.get('Content-Disposition'),'UTF-8'))
                        if media_ext_guess:
                            media_ext_guess = media_ext_guess[0]
                            break
                media_ext = media_ext_guess or os.path.splitext(url)[1]
        except Exception as e:
            print(f"\nsomething went wrong when downloading file:\n{request}\n{e}\n")
            traceback.print_exc()
        return "{}{}".format(filename, media_ext)


