import scrapy


class SatilikDaireSpider(scrapy.Spider):
    name = 'satilik_daire'
    allowed_domains = ['www.hepsiemlak.com']
    start_urls = ['https://www.hepsiemlak.com/istanbul-satilik']

    def parse(self, response):
        evler = response.xpath("//div[@class='listView']/ul/li")

        for ev in evler:
            ev_resim     = ev.xpath(".//a[@class='img-link']/figure/picture/img/@data-src").get()
            ev_tipi      = str(ev.xpath(".//div[@class='top']/div[@class='left']/span[2]/text()").get()).replace("\n","").strip()
            ev_baslik    = ev.xpath(".//div[@class='list-view-content']/div/a/@title").get()
            ev_fiyat     = str(ev.xpath(".//div[@class='top']/span[1]/text()").get()).replace("\n","").strip()
            ev_oda       = ev.xpath(".//div[@class='top']/div[@class='right']/span[1]/span/span/text()").get()
            ev_metrekare = str(ev.xpath(".//div[@class='top']/div[@class='right']/span[2]/span/span/span/text()").get()).replace("\n","").strip()
            ev_yasi      = ev.xpath(".//div[@class='top']/div[@class='right']/span[3]/span/text()").get()
            ev_kat       = str(ev.xpath("//div[@class='top']/div[@class='right']/span[4]/text()").get()).replace("\n","").strip()

            ev_ilce      = str(ev.xpath(".//div[@class='list-view-location']/span[1]/text()").get()).strip()
            ev_mahalle   = str(ev.xpath(".//div[@class='list-view-location']/span[2]/text()").get()).replace("\n","").strip()
            ev_adres     = ev_ilce + " " + ev_mahalle 

            yield{

                "Ev Resmi"      : ev_resim,
                "Emlak Tipi"    : ev_tipi,
                "İlan Basligi"  : ev_baslik,
                "Ev Fiyatı"     : ev_fiyat,
                "Oda Sayisi"    : ev_oda,
                "Ev MetreKare"  : ev_metrekare,
                "Bina Yasi"     : ev_yasi,
                "Bina Kati"     : ev_kat,
                "Adres"         : ev_adres,
            }

        
        sonraki_sayfa = response.xpath("//div[@class='he-pagination']/a[2]/@href").get()

        if sonraki_sayfa:
            link = response.urljoin(sonraki_sayfa)
            yield scrapy.Request(url=link, callback=self.parse)
