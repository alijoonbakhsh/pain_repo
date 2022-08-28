import scrapy
import json
import datetime as dt
import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="alijoonbakhsh",
  password="13861386",
  database="crawler")


class testspider(scrapy.Spider):

    name = "testspider"

    def start_requests(self):
        """this function requests to "start_urls" and go to parse_first function"""

        start_urls = ['https://www.accuweather.com/en/ir/iran-weather']

        yield scrapy.Request(url = start_urls[0], callback=self.parse_first)
    
    def parse_first(self, response):
        """this function gets the urls of each city for their first page and go to this page"""
        urls_list = response.xpath('//a[@class="nearby-location weather-card"]/@href').extract()
        for i in range(len(urls_list)):
            url_nahaii = 'https://www.accuweather.com/' + urls_list[i]
            yield response.follow(url_nahaii, callback=self.parse_first_page)


    
    def parse_first_page(self, response):
        """this function gets the link of the page of current information with more details than first page and go to this page"""

        current_link_pages = response.xpath('/html/body/div/div[4]/div[1]/div[1]/a[1]/@href').extract()
        current_link_page = 'https://www.accuweather.com/' + current_link_pages[0]
        yield response.follow(current_link_page, callback=self.parse_currentweather)


    def parse_currentweather(self, response):
        """this function gets the information of current weather page and go to tomorrow page"""

        DOWNLOAD_DELAY = 1.25

        shahr = response.css('body > div > div.nfl-header > div.header-outer > div > a.header-city-link > h1::text').get()
        current_temp = response.xpath('/html/body/div/div[4]/div[1]/div[1]/div[2]/div[2]/div[1]/div[1]/div/div/text()').extract()[0]
        pusheshabr = response.xpath('/html/body/div/div[4]/div[1]/div[1]/div[2]/div[3]/div[2]/div[2]/div[2]/text()').extract()[0]
        saghf_abr = response.xpath('/html/body/div/div[4]/div[1]/div[1]/div[2]/div[3]/div[2]/div[4]/div[2]/text()').extract()[0]
        had_aksar_ashaee_mavara_banafhsh = response.xpath('/html/body/div/div[4]/div[1]/div[1]/div[2]/div[3]/div[1]/div[1]/div[2]/text()').extract()[0]
        rtoobat = response.xpath('/html/body/div/div[4]/div[1]/div[1]/div[2]/div[3]/div[1]/div[4]/div[2]/text()').extract()[0]
        ab_havaye_feely = response.xpath('/html/body/div/div[4]/div[1]/div[1]/div[2]/div[2]/div[1]/div[2]/text()').extract()[0]
        baad = response.xpath('/html/body/div/div[4]/div[1]/div[1]/div[2]/div[3]/div[1]/div[2]/div[2]/text()').extract()[0]
        feshar = response.xpath('/html/body/div/div[4]/div[1]/div[1]/div[2]/div[3]/div[2]/div[1]/div[2]/text()').extract()[0]

        sql = "INSERT INTO currentweather (id, current_temp, pusheshabr, saghf_abr, had_aksar_ashaee_mavara_banafhsh, rtoobat, ab_havaye_feely, baad, feshar) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
        val = (shahr, current_temp, pusheshabr, saghf_abr, had_aksar_ashaee_mavara_banafhsh, rtoobat, ab_havaye_feely, baad, feshar)
        mycursor = mydb.cursor()
        mycursor.execute(sql, val)

        mydb.commit()
        
        link_pages_2 = response.css('body > div > div.two-column-page-content > div.page-column-1 > div.content-module > div.content-module.subnav-pagination > a:nth-child(3)::attr(href)').extract()
        link_page_2 = 'https://www.accuweather.com/' + link_pages_2[0]
        yield response.follow(link_page_2, callback=self.parse_eachday)


    def parse_eachday(self, response):
        """this function gets the information of each day then go to hourly page"""
        DOWNLOAD_DELAY = 1.45

        rooz = response.xpath('/html/body/div/div[4]/div[1]/div[1]/div[1]/div/text()').extract()[0].split(" ")
        this_year = dt.date.today().year
        rooz_full_tarikh = str(this_year) + '.' + rooz[1] + '.' + rooz[2]
        rooz_date = dt.datetime.strptime(rooz_full_tarikh, "%Y.%B.%d")
        today_date = dt.date.today()
        days = (rooz_date.date()- today_date).days

        shahr = response.css('body > div > div.nfl-header > div.header-outer > div > a.header-city-link > h1::text').get()
        shahr_rooz = shahr + " " + str(days)

        tarikh = response.xpath('/html/body/div/div[4]/div[1]/div[1]/div[1]/div/text()').extract()[0]

        dama_rooz = response.xpath('/html/body/div/div[4]/div[1]/div[1]/div[2]/div[1]/div[1]/text()').extract()[0]
        had_aksar_ashaee_mavara_banafhsh = response.xpath('/html/body/div/div[4]/div[1]/div[1]/div[2]/div[2]/div[2]/div[1]/p[1]/span/text()').extract()[0]
        poosheshabr_rooz = response.xpath('/html/body/div/div[4]/div[1]/div[1]/div[2]/div[2]/div[2]/div[2]/p[3]/span/text()').extract()[0]
        ehtemalbaresh_rooz = response.xpath('/html/body/div/div[4]/div[1]/div[1]/div[2]/div[2]/div[2]/div[1]/p[4]/span/text()').extract()[0]
        mizanbaresh_rooz = response.xpath('/html/body/div/div[4]/div[1]/div[1]/div[2]/div[2]/div[2]/div[2]/p[2]/span/text()').extract()[0]
        baad_rooz = response.xpath('/html/body/div/div[4]/div[1]/div[1]/div[2]/div[2]/div[2]/div[1]/p[2]/span/text()').extract()[0]

    
        dama_shab = response.xpath('/html/body/div/div[4]/div[1]/div[1]/div[3]/div[1]/div[1]/text()').extract()[0]
        ehtemalbaresh_shab = response.xpath('/html/body/div/div[4]/div[1]/div[1]/div[3]/div[2]/div[2]/div[1]/p[3]/span/text()').extract()[0]
        mizanbaresh_shab = response.xpath('/html/body/div/div[4]/div[1]/div[1]/div[3]/div[2]/div[2]/div[2]/p[2]/span/text()').extract()[0]
        baad_shab = response.xpath('/html/body/div/div[4]/div[1]/div[1]/div[3]/div[2]/div[2]/div[1]/p[1]/span/text()').extract()[0]

        sql = "INSERT INTO daily (id, tarikh, dama_rooz, had_aksar_ashaee_mavara_banafhsh, poosheshabr_rooz, ehtemalbaresh_rooz, mizanbaresh_rooz, baad_rooz, dama_shab, ehtemalbaresh_shab, mizanbaresh_shab, baad_shab) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        val = (shahr_rooz, tarikh, dama_rooz, had_aksar_ashaee_mavara_banafhsh, poosheshabr_rooz, ehtemalbaresh_rooz, mizanbaresh_rooz, baad_rooz, dama_shab, ehtemalbaresh_shab, mizanbaresh_shab, baad_shab)
        mycursor = mydb.cursor()
        mycursor.execute(sql, val)
        mydb.commit()
        nextpages = response.css('body > div > div.two-column-page-content > div.page-column-1 > div.content-module > div.subnav-pagination > a:nth-child(3)::attr(href)').extract()  
        nextpage = 'https://www.accuweather.com/' + nextpages[0]
        hourly_data_pags = response.css('body > div > div.page-subnav > div > div.subnav-items > a:nth-child(2)::attr(href)').extract()
        hourly_page = 'https://www.accuweather.com/' + hourly_data_pags[0]

        if days >= 14:

            yield response.follow(hourly_page, callback=self.parse_hourly)
            

        else :

            yield response.follow(nextpage, callback=self.parse_eachday)


    def parse_hourly(self, response) :
        """this function gets the information of each hour from now until night"""

        DOWNLOAD_DELAY = 1.35
        all_data =  response.xpath('//span[@class="value"]/text()').extract()
        saatha = int((len(all_data)+3)/9)
        day_h = saatha-3

        for i in range(saatha):
                
            saat = int(response.xpath('//*[@id="hourlyCard{}"]/div[1]/div/div[1]/h2/span/text()'.format(i)).extract()[0].split(" ")[0])
            shahr = response.css('body > div > div.nfl-header > div.header-outer > div > a.header-city-link > h1::text').get()
            shahr_saat = shahr + " " + str(saat)

            if saat < 8 and saat > 6 :

                
                hour = response.xpath('//*[@id="hourlyCard{}"]/div[1]/div/div[1]/h2/span/text()'.format(i)).extract()[0]
                temp = response.xpath('//*[@id="hourlyCard{}"]/div[1]/div/div[1]/div/text()'.format(i)).extract()[0]
                weather = response.xpath('//*[@id="hourlyCard{}"]/div[2]/div/div[1]/div[1]/div/text()'.format(i)).extract()[0]
                cloud_cover = all_data[(i*9)+6]
                humidity = all_data[(i*9)+3]
                wind = all_data[(i*9)+1]
                    
            else :
                    
                
                hour = response.xpath('//*[@id="hourlyCard{}"]/div[1]/div/div[1]/h2/span/text()'.format(i)).extract()[0]
                temp = response.xpath('//*[@id="hourlyCard{}"]/div[1]/div/div[1]/div/text()'.format(i)).extract()[0]
                weather = response.xpath('//*[@id="hourlyCard{}"]/div[2]/div/div[1]/div[1]/div/text()'.format(i)).extract()[0]
                cloud_cover = all_data[(i*8)+day_h+5]
                humidity = all_data[(i*8)+day_h+2]
                wind = all_data[(i*8)+day_h]


            sql = "INSERT INTO hourly (id, hour, temp, weather, cloud_cover, humidity, wind) VALUES (%s, %s, %s, %s, %s, %s, %s)"
            val = (shahr_saat, hour, temp, weather, cloud_cover, humidity, wind)
            mycursor = mydb.cursor()
            mycursor.execute(sql, val)
            mydb.commit()