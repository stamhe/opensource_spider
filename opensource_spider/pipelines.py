# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


import requests
import os

class OpensourceSpiderPipeline(object):
    def __init__(self):
        #self.root_dir = '/windows/disk/work/linux/software/opensource'
        self.root_dir = '/windows/epan/opensource'
        pass
    def process_item(self, item, spider):
        if spider.name == 'nginx_spider':
            file_path = self.root_dir + "/nginx/" + os.path.dirname(item['orginname'])
        elif spider.name == 'lvs_spider':
            file_path = self.root_dir + "/lvs/" + os.path.dirname(item['orginname'])
        elif spider.name == 'vim_spider':
            file_path = self.root_dir + "/vim/" + os.path.dirname(item['orginname'])
        elif spider.name == 'sphinx_spider':
            file_path = self.root_dir + "/sphinx/" + os.path.dirname(item['orginname'])
        elif spider.name == 'isc_spider':
            file_path = self.root_dir + "/isc/" + os.path.dirname(item['orginname'])
        elif spider.name == 'kernel_spider':
            file_path = self.root_dir + "/kernel/" + os.path.dirname(item['orginname'])
        elif spider.name == 'git_spider':
            file_path = self.root_dir + "/git/" + os.path.dirname(item['orginname'])
        elif spider.name == 'apache_spider':
            file_path = self.root_dir + "/apache/" + os.path.dirname(item['orginname'])
        elif spider.name == 'python_spider':
            file_path = self.root_dir + "/python/" + os.path.dirname(item['orginname'])
        elif spider.name == 'curl_spider':
            file_path = self.root_dir + "/curl/" + os.path.dirname(item['orginname'])
        elif spider.name == 'ffmpeg_spider':
            file_path = self.root_dir + "/ffmpeg/" + os.path.dirname(item['orginname'])
        elif spider.name == 'gnu_spider':
            file_path = self.root_dir + "/gnu/" + os.path.dirname(item['orginname'])
        else:
            file_path = self.root_dir + "/source/" + os.path.dirname(item['orginname'])

        if os.path.exists(file_path) == False:
            try:
                #os.mkdir(file_path)
                os.makedirs(file_path)
            except OSError as exc:
                if exc.errno == errno.EEXIST and os.path.isdir(file_path):
                    pass
                else:
                    raise
        
        new_filename = file_path + "/" + os.path.basename(item['orginname'])


        r = requests.get(item['downurl'], stream = True)
        if r.status_code != 200:
            print "%s DONOT exists in server!!!"%(item['orginname'])
            return item

        filesize = int(r.headers['Content-Length'])
        # 文件存在且大小与要下载的大小一致，则不再重复下载了
        if os.path.isfile(new_filename) == True and (filesize == os.path.getsize(new_filename)):
            print "%s exists...no need to download again"%(item['orginname'])
            return item


        print "%s start to download now..."%(item['orginname'])
        f = open(new_filename, 'wb')
        ck_size=40960
        ck_count=0
        for chunk in r.iter_content(chunk_size = ck_size):
            if chunk:
                f.write(chunk)
                ck_count = ck_count + 1
                print "%s writing data...filesize = %d pos = %d"%(item['orginname'], filesize, ck_size * ck_count)

        f.close()
        if os.path.getsize(new_filename) == filesize:
            print "%s download success.................."%(item['orginname'])

        return item

    def open_spider(self, spider):
        pass

    def close_spider(self, spider):
        pass
