# -*- coding: utf-8 -*-
import scrapy
from scrapy_folha.items import ScrapyFolhaItem

class SearchSpider(scrapy.Spider):
    name = 'search'
    allowed_domains = ['search.folha.uol.com.br', 
                        'www1.folha.uol.com.br']
    page_counter = 0
    max_pages = 8

    start_urls = [f'http://search.folha.uol.com.br/?q=esportes'] 
    # TODO: colocar kwarg no q para buscar por tema
    # TODO: tratar data
    # TODO: 

    def parse(self, response):
      
      self.page_counter += 1

      link = response.css(".c-headline__content")
      for item in link:
        yield from self.parse_article(item, response)

      next_page = response.css(".c-pagination__item+ .c-pagination__arrow a::attr(href)").get() #all()[:-2]
      if next_page is not None and self.page_counter < self.max_pages:
          yield response.follow(next_page, self.parse)
   

    def parse_article(self, content, response):

      title = content.css(".c-headline__title::text").get()
      text = content.css('.c-headline__standfirst::text').get()
      image = response.css(".c-headline__image::attr(src)").get()
      # category = content.css('.c-search__result_h3::text').get()
      created_at = content.css('.c-headline__dateline::text').get()
      link = content.css('.c-headline__content a::attr(href)').get()
      
      article = ScrapyFolhaItem(title=title, created_at=created_at, 
                                text=text, link=link, image=image)#, category=category)
      yield article
