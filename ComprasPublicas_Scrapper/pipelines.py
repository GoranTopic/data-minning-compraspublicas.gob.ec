# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import os


class CompraspublicasScrapperPipeline:
    dest_folder = 'Compras_Publicas'
    tab_types = { 
            '1' : 'Descripción', 
            '2' : 'Fechas', 
            '3' : 'productos', 
            '4' : 'Parámetros de Calificación', 
            '5' : 'Archivos', }

    #os.chdir(project.code)
    #cwd = os.getcwd()
    #os.mkdir(project.code)
    #os.chdir(project.code)
    

    def open_spider(self, spider):
        self.make_folder(self.dest_folder)

    def close_spider(self, spider):
        #self.file.close()
        pass

    def process_item(self, item, spider):
        # get the proects data passed
        body = item['body']
        project = item['project']
        tab_num = item['tab_num']
        # get code folder name
        code_folder = project["code"]
        # get tab folder name
        tab_folder = self.tab_types[f'{tab_num}']
        # make folders
        self.make_folder(
                os.path.join(self.dest_folder, code_folder))
        # get file path 
        self.make_folder(
                os.path.join(self.dest_folder, 
                    code_folder, tab_folder))
                # filename path
        filename = os.path.join(self.dest_folder, 
                code_folder,
                tab_folder,
                f"{tab_folder}.html")
        open(filename, "w").write(str(body, 'UTF-8'))
        return item

    def make_folder(self, folder):
        if not os.path.exists(folder):
            os.makedirs(folder)


