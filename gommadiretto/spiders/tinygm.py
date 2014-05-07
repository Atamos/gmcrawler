from scrapy.spider import Spider
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.selector import HtmlXPathSelector
from scrapy.selector import Selector
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from gommadiretto.items import DisponibilityItem
from scrapy.log import ScrapyFileLogObserver
from scrapy import log
from scrapy.contrib.loader.processor import TakeFirst, MapCompose, Join
from scrapy.contrib.loader import ItemLoader



class TinyGmSpider(CrawlSpider):
    name = "tinygm"
    domain_name = "gommadiretto.it"
    
    rules = (
         Rule(SgmlLinkExtractor(restrict_xpaths=('//a[@id="ajax_suchergebnisliste_goto_next"]'),canonicalize=False),callback="parse_items"),
    )

    def __init__(self,name=None,dim1=None,dim2=None,dim3=None,paging=5,**kwargs):
        ScrapyFileLogObserver(open("tinyspider.log",'w'), level=log.INFO).start()
        ScrapyFileLogObserver(open("tinyspider_error.log",'w'),level=log.ERROR).start()
        log.msg('begin arguments')
        log.msg(dim1)
        log.msg(dim2)
        log.msg(dim3)
        log.msg(paging)
        log.msg('end arguments')
        log.msg('STAR WITH : %s %s %s WITH PAGE %s' % (dim1,dim2,dim3,paging))
        super(TinyGmSpider,self).__init__(name,**kwargs)
        log.msg("http://www.gommadiretto.it/cgi-bin/rshop.pl?dsco=130&Breite=%s&Quer=%s&Felge=%s&Speed=&Load=&kategorie=&Marke=&ranzahl=4&tyre_for=&x_tyre_for=&m_s=3&suchen=Trova%%20pneumatici&rsmFahrzeugart=PKW&filter_preis_bis=&filter_preis_von=&homologation=&search_tool=standard&Ang_pro_Seite=%s" % (dim1,dim2,dim3,paging))
        self.start_urls = ["http://www.gommadiretto.it/cgi-bin/rshop.pl?dsco=130&Breite=%s&Quer=%s&Felge=%s&Speed=&Load=&kategorie=&Marke=&ranzahl=4&tyre_for=&x_tyre_for=&m_s=3&suchen=Trova%%20pneumatici&rsmFahrzeugart=PKW&filter_preis_bis=&filter_preis_von=&homologation=&search_tool=standard&Ang_pro_Seite=%s" % (dim1,dim2,dim3,paging)] 


    def parse_start_url(self, response):
        return self.parse_items(response)

    def parse_items(self,response):
        response = response.replace(body=response.body.replace('<br />', '\n')) 
        sel = HtmlXPathSelector(response)
        
        products = []
        items = sel.xpath("//div[@id='ajax_suchergebnisliste']/*[div]")

        for product in items:
            l = ItemLoader(item=DisponibilityItem(),selector=product)
            l.add_xpath('name','.//a[1]/@name')
            l.add_xpath('title','.//div/div/div[2]/div//text()')
            l.add_xpath('disponibility','.//div/div/div[5]/div[1]/text()')
            products.append(l.load_item());
        return products
