# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

# useful for handling different item types with a single interface
from scrapy.pipelines.files import FilesPipeline
from dotenv import dotenv_values
import mimetypes
import traceback
import os
import re

env = dotenv_values('.env')
urls = dotenv_values('.urls')
if env['DEST_FOLDER'] is not None:
    dest = os.path.join( env['DEST_FOLDER'], urls['DOMAIN'])
else: 
    dest = urls['DOMAIN']

tab_types = { 
        '1' : 'Descripción', 
        '2' : 'Fechas', 
        '3' : 'productos', 
        '4' : 'Parámetros de Calificación', 
        '5' : 'Historial de respuestas', 
        '6' : 'Archivos', }

class CompraspublicasScrapperPipeline:
    urls = urls 
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
        base_url = urls['PROCESOS_URL']
        url = base_url + self.project['ID']
        # craft file path
        filename = os.path.join(
                self.dest, 
                self.code_folder,
                f"{self.code_folder}.url")
        _file = open(filename, "w")
        _file.write(f"[InternetShortcut]\nURL={url}")

    def create_html_file(self, item):
        # filename path
        filename = os.path.join(self.dest, 
                self.code_folder,
                self.tab_folder,
                f"{self.tab_folder}.html")
        # create file 
        open(filename, "w").write(str(self.body, 'UTF-8'))
        

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
        self.body = item['response'].body
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


