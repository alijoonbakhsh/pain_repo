import scrapy
import json
import datetime as dt

class testspider(scrapy.Spider):
    name = "testspider"
    def start_requests(self):
        """baraie shro va request dadan be har url shoroee"""

        urls_list = [#urls_list = response.xpath('//a[@class="nearby-location weather-card"]/@href').extract()       ---------       the response for these urls
            '/web-api/three-day-redirect?key=210434&target=',
            '/web-api/three-day-redirect?key=206976&target=',
            '/web-api/three-day-redirect?key=208194&target=',
            '/web-api/three-day-redirect?key=210047&target=', 
            '/web-api/three-day-redirect?key=208929&target=', 
            '/web-api/three-day-redirect?key=207308&target=', 
            '/web-api/three-day-redirect?key=210841&target=', 
            '/web-api/three-day-redirect?key=210291&target=', 
            '/web-api/three-day-redirect?key=208612&target=', 
            '/web-api/three-day-redirect?key=210584&target=', 
            '/web-api/three-day-redirect?key=210185&target=', 
            '/web-api/three-day-redirect?key=208538&target=', 
            '/web-api/three-day-redirect?key=210816&target=', 
            '/web-api/three-day-redirect?key=210842&target=', 
            '/web-api/three-day-redirect?key=211367&target=', 
            '/web-api/three-day-redirect?key=209375&target=', 
            '/web-api/three-day-redirect?key=209439&target=', 
            '/web-api/three-day-redirect?key=208708&target=', 
            '/web-api/three-day-redirect?key=209737&target=', 
            '/web-api/three-day-redirect?key=208760&target=']
        urls = []
        for i in range(len(urls_list)):
            url_nahaii = 'https://www.accuweather.com/' + urls_list[i]
            urls.append(url_nahaii)

        for url in urls :
            yield scrapy.Request( url = url, callback = self.parse_first)

    
    def parse_first(self, response):
        """be safhe ye aval rafte va az anja vared safheye joziiat mishavad"""

        current_link_pages = response.xpath('/html/body/div/div[4]/div[1]/div[1]/a[1]/@href').extract()
        current_link_page = 'https://www.accuweather.com/' + current_link_pages[0]
        yield response.follow(current_link_page, callback=self.parse_currentweather)


    def parse_currentweather(self, response):
        """dar safhe ye joziiat eteleat ra daryaft mikonad va be safhe ye baadi ya rozzane miravad"""

        yield {
            'current_temp' : response.xpath('/html/body/div/div[4]/div[1]/div[1]/div[2]/div[2]/div[1]/div[1]/div/div/text()').extract()[0],
            'pusheshabr' : response.xpath('/html/body/div/div[4]/div[1]/div[1]/div[2]/div[3]/div[2]/div[2]/div[2]/text()').extract()[0],
            'saghf_abr' : response.xpath('/html/body/div/div[4]/div[1]/div[1]/div[2]/div[3]/div[2]/div[4]/div[2]/text()').extract()[0],
            'had_aksar_ashaee-mavara_banafhsh' : response.xpath('/html/body/div/div[4]/div[1]/div[1]/div[2]/div[3]/div[1]/div[1]/div[2]/text()').extract()[0],
            'rtoobat' : response.xpath('/html/body/div/div[4]/div[1]/div[1]/div[2]/div[3]/div[1]/div[4]/div[2]/text()').extract()[0],
            'ab_havaye_feely' : response.xpath('/html/body/div/div[4]/div[1]/div[1]/div[2]/div[2]/div[1]/div[2]/text()').extract()[0],
            'baad' : response.xpath('/html/body/div/div[4]/div[1]/div[1]/div[2]/div[3]/div[1]/div[2]/div[2]/text()').extract()[0],
            'feshar' : response.xpath('/html/body/div/div[4]/div[1]/div[1]/div[2]/div[3]/div[2]/div[1]/div[2]/text()').extract()[0]
        }
        
        link_pages_2 = response.css('body > div > div.two-column-page-content > div.page-column-1 > div.content-module > div.content-module.subnav-pagination > a:nth-child(3)::attr(href)').extract()
        link_page_2 = 'https://www.accuweather.com/' + link_pages_2[0]
        yield response.follow(link_page_2, callback=self.parse_eachday)


    def parse_eachday(self, response):
        """etelaat har rooz ra dar mored rooz va shab grefte va be safhe ye saaty miravad"""

        rooz = response.xpath('/html/body/div/div[4]/div[1]/div[1]/div[1]/div/text()').extract()[0].split(" ")
        year_born =  dt.date(1982,2,14)
        this_year = dt.date.today().year
        rooz_full_tarikh = str(this_year) + '.' + rooz[1] + '.' + rooz[2]
        rooz_date = dt.datetime.strptime(rooz_full_tarikh, "%Y.%B.%d")
        today_date = dt.date.today()
        days = (rooz_date.date()- today_date).days

        yield {
            'tarikh' : response.xpath('/html/body/div/div[4]/div[1]/div[1]/div[1]/div/text()').extract()[0],

            'rooz' : {
                'dama' : response.xpath('/html/body/div/div[4]/div[1]/div[1]/div[2]/div[1]/div[1]/text()').extract()[0],
                'had_aksar_ashaee-mavara_banafhsh' : response.xpath('/html/body/div/div[4]/div[1]/div[1]/div[2]/div[2]/div[2]/div[1]/p[1]/span/text()').extract()[0],
                'poosheshabr' : response.xpath('/html/body/div/div[4]/div[1]/div[1]/div[2]/div[2]/div[2]/div[2]/p[3]/span/text()').extract()[0],
                'ehtemalbaresh' : response.xpath('/html/body/div/div[4]/div[1]/div[1]/div[2]/div[2]/div[2]/div[1]/p[4]/span/text()').extract()[0],
                'mizanbaresh' : response.xpath('/html/body/div/div[4]/div[1]/div[1]/div[2]/div[2]/div[2]/div[2]/p[2]/span/text()').extract()[0],
                'baad' : response.xpath('/html/body/div/div[4]/div[1]/div[1]/div[2]/div[2]/div[2]/div[1]/p[2]/span/text()').extract()[0]
                },

            'shab' : {
                'dama' : response.xpath('/html/body/div/div[4]/div[1]/div[1]/div[3]/div[1]/div[1]/text()').extract()[0],
                'ehtemalbaresh' : response.xpath('/html/body/div/div[4]/div[1]/div[1]/div[3]/div[2]/div[2]/div[1]/p[3]/span/text()').extract()[0],
                'mizanbaresh' : response.xpath('/html/body/div/div[4]/div[1]/div[1]/div[3]/div[2]/div[2]/div[2]/p[2]/span/text()').extract()[0],
                'baad' : response.xpath('/html/body/div/div[4]/div[1]/div[1]/div[3]/div[2]/div[2]/div[1]/p[1]/span/text()').extract()[0]
                }
        }

        nextpages = response.css('body > div > div.two-column-page-content > div.page-column-1 > div.content-module > div.subnav-pagination > a:nth-child(3)::attr(href)').extract()  
        nextpage = 'https://www.accuweather.com/' + nextpages[0]
        hourly_data_pags = response.css('body > div > div.page-subnav > div > div.subnav-items > a:nth-child(2)::attr(href)').extract()
        hourly_page = 'https://www.accuweather.com/' + hourly_data_pags[0]
        if days <= 14:

                yield response.follow(nextpage, callback=self.parse_eachday)

        else :

            yield response.follow(hourly_page, callback=self.parse_hourly)


    def parse_hourly(self, response) :
        """etelaat har saat az alan ta shab ra migirad"""

        for j in range (24) :

            try :

                yield {
                    'hour' : response.xpath('//*[@id="hourlyCard{}"]/div[1]/div/div[1]/h2/span/text()'.format(j)).extract()[0],
                    'dama' : response.xpath('//*[@id="hourlyCard{}"]/div[1]/div/div[1]/div/text()'.format(j)).extract()[0],
                    'ab_o_hava' : response.xpath('//*[@id="hourlyCard{}"]/div[2]/div/div[1]/div[1]/div/text()'.format(j)).extract()[0],
                    'pooshesh_abr' : response.xpath('//*[@id="hourlyCard{}"]/div[2]/div/div[2]/div[2]/p[2]/text()'.format(j)).extract()[0],
                    'rotobat' : response.xpath('//*[@id="hourlyCard{}"]/div[2]/div/div[2]/div[1]/p[4]/span/text()'.format(j)).extract()[0],
                    'baad' : response.xpath('//*[@id="hourlyCard{}"]/div[2]/div/div[2]/div[1]/p[2]/span/text()'.format(j)).extract()[0],
                    'had_aksar_ashaee-mavara_banafhsh' : response.xpath('//*[@id="hourlyCard{}"]/div[2]/div/div[2]/div[1]/p[1]/span/text()'.format(j)).extract()[0],
                    'keyfiat_hava_text' : response.xpath('//*[@id="hourlyCard{}"]/div[2]/div/div[2]/div[1]/p[5]/span/span/text()'.format(j)).extract()[0]
                }

            except :


                pass