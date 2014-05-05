from scrapy.spider import Spider
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.selector import HtmlXPathSelector
from scrapy.selector import Selector
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from gommadiretto.items import GommadirettoItem
from scrapy.log import ScrapyFileLogObserver
from scrapy import log
from scrapy.contrib.loader.processor import TakeFirst, MapCompose, Join
from scrapy.contrib.loader import ItemLoader



class GmSpider(CrawlSpider):
	name = "gm"
	domain_name = "gommadiretto.it"
	#start_urls = ["http://www.gommadiretto.it/cgi-bin/rshop.pl?dsco=130&cart_id=9963841.130.4327&sowigan=So&Breite=205&Quer=55&Felge=16&Speed=&kategorie=6&Marke=&ranzahl=4&tyre_for=&x_tyre_for=&suchen=Trova%20pneumatici&rsmFahrzeugart=PKW&search_tool=standard&Ang_pro_Seite=5"]
	#start_urls = ["http://www.gommadiretto.it/cgi-bin/rshop.pl?m_s=3&Ang_pro_Seite=5&rsmFahrzeugart=PKW&s_p=Tutti&cart_id=9963841.130.4327&x_tyre_for=&search_tool=standard&dsco=130&tyre_for=&suchen=Trova+pneumatici&with_bootstrap_flag=1&ranzahl=4&sowigan=&Breite=145&Quer=70&Felge=12&Speed=&Load=&Marke=&kategorie=6&filter_preis_von=&filter_preis_bis=&homologation="]
	start_urls = ["http://www.gommadiretto.it/cgi-bin/rshop.pl?dsco=130&cart_id=9963841.130.4327&Breite=145&Quer=70&Felge=12&Speed=&Load=&kategorie=6&Marke=&ranzahl=4&tyre_for=&x_tyre_for=&m_s=3&Ang_pro_Seite=5&rsmFahrzeugart=PKW&filter_preis_bis=&filter_preis_von=&homologation=&search_tool=standard&Label=G-E-70-2&details=Ordern&typ=R-123525"]

	rules = (
		Rule(SgmlLinkExtractor(allow=('cgi-bin\/rshop.pl\?.*typ=[-0-9a-zA-Z]*$')),callback='parse_item'),
		#Rule(SgmlLinkExtractor(restrict_xpaths=('//a[@id="ajax_suchergebnisliste_goto_next"]',)))
	)

	def __init__(self,name=None,**kwargs):
		ScrapyFileLogObserver(open("spider.log",'w'), level=log.INFO).start()
		ScrapyFileLogObserver(open("spider_error.log",'w'),level=log.ERROR).start()
		super(GmSpider,self).__init__(name,**kwargs)


	def parse_item(self,response):
		response = response.replace(body=response.body.replace('<br />', '\n')) 
		sel = HtmlXPathSelector(response)
		
		l = ItemLoader(item=GommadirettoItem(),response=response)		

		item = GommadirettoItem()
		l.add_xpath('title','.//*[@id="detail-page"]/div[2]/div[2]/span/span[1]/h1/text()')
		l.add_xpath('small',".//*[@id='detail-page']/div[2]/div[2]/span/span[2]/text()")
		l.add_xpath('disponibility',".//*[@id='detail-page']/div[2]/div[3]/div[1]/div[2]/span/text()")
		sel.select(".//*[@id='detail-page']/div[2]/div[3]/div[2]/div[1]/text()").extract()

		if(sel.xpath(".//*[@id='detail-page']/div[2]/div[3]/div[2]/div[1]/text()").extract()[0] == 'Tipo di pneumatico'):
			l.add_xpath('ttype',".//*[@id='detail-page']/div[2]/div[3]/div[2]/div[2]/*/text()")
			l.add_xpath('iv',".//*[@id='detail-page']/div[2]/div[3]/div[3]/div[2]//text()")
			l.add_xpath('ue',".//*[@id='detail-page']/div[2]/div[3]/div[5]/div[2]/div[1]//text()");#.re("([A-Z]) *, *([A-Z]) *, *([A-Za-z0-9]*) ([a-z]*[^,])");
		else:
			l.add_value('ttype','undefined')
			l.add_xpath('iv',".//*[@id='detail-page']/div[2]/div[3]/div[2]/div[2]//text()")
			l.add_xpath('ue',".//*[@id='detail-page']/div[2]/div[3]/div[4]/div[2]/div[1]//text()");#.re("([A-Z]) *, *([A-Z]) *, *([A-Za-z0-9]*) ([a-z]*[^,])");#,re="([A-Z]) *, *([A-Z]) *, *([A-Za-z0-9]*) ([a-z]*[^,])")

		l.add_xpath('price',".//*[@id='detail-page']/div[3]/div[1]/div[1]/span/b/i[@itemprop=\"price\"]/text()")
 		l.add_xpath('size',".//*[@id='inhalt_site_content']/div/span[4]/span/a/text()")		
		#l.add_xpath('tlong',".//*[@id='reifendetails_tabs-0']/p//text()")
		l.add_xpath('tlong',".//*[@id='reifendetails_tabs-0']/p")
		l.add_xpath('name',".//*[@id='detail-page']/@data-item_id")

		link = sel.xpath(".//*[@id='detail-page']/div[1]/div/div/img/@src").extract()
		log.msg(link)

		l.add_value("image_urls",link)

		#l.add_value('link',response.url)
		
		return l.load_item()