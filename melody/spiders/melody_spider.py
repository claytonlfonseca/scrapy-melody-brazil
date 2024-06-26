#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import scrapy
from scrapy.crawler import CrawlerProcess

def main():
    #Exporta o relatório em XLSx chamando o Spider
    process = CrawlerProcess()

    #Chama a classe Melody que contem o Spider
    process.crawl(Melody)
    process.start()

class Melody(scrapy.Spider):
    name = 'melody'
 
    def __init__(self):
        self.start_url = "https://www.melodybrazil.com/"

    #Realiza requisição a partir da variável START_URL
    def start_requests(self):
        yield scrapy.Request(self.start_url)
    
    #Faz o parse da página html requisitada
    def parse(self, response, **kwargs):  
        tags = response.xpath('//div[@class="post-info"]')

        for tag in tags:
            url_cd = tag.xpath('.//h2[@class="post-title"]/a/@href').get()
            name = tag.xpath('./h2[@class="post-title"]/a[@href]/text()').get()
            date_pub = tag.xpath('.//time[@class="post-datepublished"]/text()').get()
            pub_by = tag.xpath('.//span[@class="post-author"]/a/text()').get()
            url_down = tag.xpath('.//a[@class="read-more"]/@href').get()  

            #Evita conteúdo no TOP 10 (não duplicidade)
            if not url_down:
                break
            yield {
                'url_cd': url_cd,
                'name': name,
                'date_pub': date_pub,
                'pub_by': pub_by,
                'url_down': url_down
            }   
            #Data e hora do último CD de cada página para montar próxima URL
            next = tag.xpath('.//time[@class="post-datepublished"]').get()      
        
        #Montando URL para próxima requisição.
        try:
            date_pg = next.split('datetime="')[1][0:10]
            time_pg = next.split('datetime="')[1][11:19]
        except:
            print("Erro ao requisitar próxima paǵina!")
            quit()

        #Realiza a requisição e chama o método Response novamente
        yield scrapy.Request("https://www.melodybrazil.com/search?updated-max="+(date_pg)+"T"+(time_pg)+"-03:00", dont_filter = True, callback=self.parse)
        print("---------------------------------------------------------------")

