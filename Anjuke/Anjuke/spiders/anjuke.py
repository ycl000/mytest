# -*- coding: utf-8 -*-
import re
from pprint import pprint
import time
import scrapy



class AnjukeSpider(scrapy.Spider):
    name = 'anjuke'
    allowed_domains = ['leyoujia.com']
    start_urls = ['https://guangzhou.leyoujia.com/esf/']

    def parse(self, response):
        # print(response.text)
        # house_links = response.xpath('/html/body/div[3]/div[2]/div[1]/div[5]/ul/li')
        # next_url = response.xpath('/html/body/div[3]/div[2]/div[1]/div[5]/div/div[2]/a[10]/@href').extract()[0]
        #
        # if next_url:
        #     url = 'https://shenzhen.leyoujia.com' + next_url
        #     # yield scrapy.Request(
        #     #     url,
        #     #     callback=self.parse
        #     # )
        #     print(url)
        #某市各区的二手房数量
        house_region= response.xpath('/html/body/div[3]/div[1]/div[1]/div[3]/div[1]/a')

        for i in range(1,len(house_region)-1):#len(house_region)-1
            url = 'https://guangzhou.leyoujia.com/esf/a{}/'.format(i)
            yield scrapy.Request(
                url,
                callback=self.house_detail,

            )



            # next_url = 'https://shenzhen.leyoujia.com'
        # #全部二手房连接 #根据市 （深圳）获取全部
        # for i in range(1,len(house_links)-35):
        #     item = {}
        #     if (i==6):
        #         print("none6")
        #     else:
        #           #二手房信息连接
        #         d = response.xpath('/html/body/div[3]/div[2]/div[1]/div[5]/ul/li[{}]/div[2]/p[1]/a/@href'.format(i)).extract()
        #         # print(re.sub(r"[\[\]\']","",str(d)))
        #         l=re.sub(r"[\[\]\']","",str(d))
        #         # print('https://shenzhen.leyoujia.com'+l)
        #         #面积
        #         item['area'] = response.xpath('/html/body/div[3]/div[2]/div[1]/div[5]/ul/li[{}]/div[2]/p[2]/span[4]/text()'.format(i)).extract_first()

        #         #户型
        #         item['fangxing'] = response.xpath('/html/body/div[3]/div[2]/div[1]/div[5]/ul/li[{}]/div[2]/p[2]/span[1]/text()'.format(i)).extract_first().replace("\t","").replace("\r","").replace("\n","")
        #         #朝向
        #         item['orientation'] = response.xpath('/html/body/div[3]/div[2]/div[1]/div[5]/ul/li[{}]/div[2]/p[2]/span[2]/text()'.format(i)).extract_first()
        #         #几年建成
        #         item['time_year'] = response.xpath('/html/body/div[3]/div[2]/div[1]/div[5]/ul/li[{}]/div[2]/p[3]/span[3]/text()'.format(i)).extract_first()
        #         #楼层
        #         item['floor'] = response.xpath('/html/body/div[3]/div[2]/div[1]/div[5]/ul/li[{}]/div[2]/p[3]/span[2]/text()'.format(i)).extract_first()
        #         #小区地址
        #         item['village'] = response.xpath('/html/body/div[3]/div[2]/div[1]/div[5]/ul/li[{}]/div[2]/p[4]/span[1]/a/text()'.format(i)).extract_first()
        #         #地区
        #         item['region'] = response.xpath('/html/body/div[3]/div[2]/div[1]/div[5]/ul/li[{}]/div[2]/p[4]/span[2]/a[1]/text()'.format(i)).extract_first()
        #         #路段
        #         item['road_section'] = response.xpath('/html/body/div[3]/div[2]/div[1]/div[5]/ul/li[{}]/div[2]/p[4]/span[2]/a[2]/text()'.format(i)).extract_first()
        #         #描述
        #         item['describe'] = response.xpath('/html/body/div[3]/div[2]/div[1]/div[5]/ul/li[{}]/div[2]/p[1]/a/text()'.format(i)).extract_first()
        #         # pprint(item)
        #         #装修
        #         item['renovation'] = response.xpath('/html/body/div[3]/div[2]/div[1]/div[5]/ul/li[12]/div[2]/p[3]/span[1]/text()').extract_first()
        #         #房源标签
        #         tags = response.xpath('/html/body/div[3]/div[2]/div[1]/div[5]/ul/li[{}]/div[2]/p[5]/span'.format(i))
        #         t=""
        #         for tag in tags:
        #             t=t+tag.xpath('text()').extract_first()+'\t'
        #
        #
        #         item['housing_label'] = t
        #         # itm=response.xpath('/html/body/div[3]/div[2]/div[1]/div[5]/ul/li[1]/div[3]/p[2]/text()').extract_first()
        #         # print("iii",itm)
        #         item['house_count'] = response.xpath('/html/body/div[3]/div[2]/div[1]/div[3]/em/text()').extract_first()
        #         house_url = 'https://shenzhen.leyoujia.com'+l
        #         yield scrapy.Request(
        #             house_url,
        #             callback=self.parse_detail,
        #             meta={"item":item}
        #
        #         )
        #         time.sleep(1)


#根据地区（福田区）来获取
    def house_detail(self,response):
        house_links = response.xpath('/html/body/div[3]/div[3]/div[1]/div[5]/ul/li')
        print("house_detail")
        print(len(house_links))

        # print("next:", next_url)
        # /html/body/div[3]/div[3]/div[1]/div[5]/div/div[2]/a[12]/text()

        # 全部二手房连接
        for i in range(1, len(house_links)): #len(house_links) - 20
            item = {}
            if (i == 6):
                print("none6")
            else:
                item['country'] = "广州"
                d = response.xpath(
                    '/html/body/div[3]/div[3]/div[1]/div[5]/ul/li[{}]/div[2]/p[1]/a/@href'.format(i)).extract()

                # print(re.sub(r"[\[\]\']","",str(d)))
                l = re.sub(r"[\[\]\']", "", str(d))
                # print('https://shenzhen.leyoujia.com'+l)
                #总价
                price = response.xpath('/html/body/div[3]/div[3]/div[1]/div[5]/ul/li[{}]/div[3]/p[1]/span/text()'.format(i)).extract_first()
                danwei = response.xpath('/html/body/div[3]/div[3]/div[1]/div[5]/ul/li[{}]/div[3]/p[1]/text()'.format(i)).extract_first()
                item['price'] = str(price)+str(danwei)
                #单价
                item['danjia'] = response.xpath('/html/body/div[3]/div[3]/div[1]/div[5]/ul/li[{}]/div[3]/p[2]/text()'.format(i)).extract_first()

                # 面积
                item['area'] = response.xpath(
                    '/html/body/div[3]/div[3]/div[1]/div[5]/ul/li[{}]/div[2]/p[2]/span[4]/text()'.format(
                        i)).extract_first()

                # 户型
                item['fangxing'] = response.xpath(
                    '/html/body/div[3]/div[3]/div[1]/div[5]/ul/li[{}]/div[2]/p[2]/span[1]/text()'.format(
                        i)).extract_first().replace("\t", "").replace("\r", "").replace("\n", "")
                # 朝向
                item['orientation'] = response.xpath(
                    '/html/body/div[3]/div[3]/div[1]/div[5]/ul/li[{}]/div[2]/p[2]/span[2]/text()'.format(
                        i)).extract_first()
                # 几年建成
                item['time_year'] = response.xpath(
                    '/html/body/div[3]/div[3]/div[1]/div[5]/ul/li[{}]/div[2]/p[3]/span[3]/text()'.format(
                        i)).extract_first()
                # 楼层
                item['floor'] = response.xpath(
                    '/html/body/div[3]/div[3]/div[1]/div[5]/ul/li[{}]/div[2]/p[3]/span[2]/text()'.format(
                        i)).extract_first()
                # 小区地址
                item['village'] = response.xpath(
                    '/html/body/div[3]/div[3]/div[1]/div[5]/ul/li[{}]/div[2]/p[4]/span[1]/a/text()'.format(
                        i)).extract_first()
                # 地区
                item['region'] = response.xpath(
                    '/html/body/div[3]/div[3]/div[1]/div[5]/ul/li[{}]/div[2]/p[4]/span[2]/a[1]/text()'.format(
                        i)).extract_first()
                # 路段
                item['road_section'] = response.xpath(
                    '/html/body/div[3]/div[3]/div[1]/div[5]/ul/li[{}]/div[2]/p[4]/span[2]/a[2]/text()'.format(
                        i)).extract_first()
                # 描述
                item['describe'] = response.xpath(
                    '/html/body/div[3]/div[3]/div[1]/div[5]/ul/li[{}]/div[2]/p[1]/a/text()'.format(i)).extract_first()
                # pprint(item)
                # 装修
                item['renovation'] = response.xpath(
                    '/html/body/div[3]/div[3]/div[1]/div[5]/ul/li[12]/div[2]/p[3]/span[1]/text()').extract_first()
                # 房源标签
                tags = response.xpath('/html/body/div[3]/div[3]/div[1]/div[5]/ul/li[{}]/div[2]/p[5]/span'.format(i))
                t = ""
                for tag in tags:
                    t = t + tag.xpath('text()').extract_first() + '\t'

                item['house_label'] = t
                # itm=response.xpath('/html/body/div[3]/div[2]/div[1]/div[5]/ul/li[1]/div[3]/p[2]/text()').extract_first()
                # print("iii",itm)
                item['house_count'] = response.xpath('/html/body/div[3]/div[3]/div[1]/div[3]/em/text()').extract_first()
                house_url = 'https://guangzhou.leyoujia.com' + l
                yield scrapy.Request(
                    house_url,
                    callback=self.parse_detail,
                    meta={"item": item}

                )
                time.sleep(1)
                # pprint(item)
                # 下一页
        next_url = response.xpath('//a[text()="下一页 "]/@href').extract_first()
        if next_url:
            url = 'https://guangzhou.leyoujia.com' + next_url
            yield scrapy.Request(
                url,
                callback=self.house_detail
            )
            print(url)






            #其他信息
    def other(self,response):
        print('other')
        item = response.meta['item']
        url = response.xpath('/html/body/div[2]/div[2]/div[3]/div[1]/div[1]/div[2]/ul/li[10]/span[2]/text()').extract_first()
        #房屋性质
        item['purpose']=url.strip()
        # print(url.strip())
        #小区用户
        # item['people'] = response.xpath('/html/body/div[2]/div[2]/div[3]/div[1]/div[1]/div[2]/ul/li[5]/span[2]/text()').extract_first()
        #开发商 Developers
        item['developers'] = response.xpath('/html/body/div[2]/div[2]/div[3]/div[1]/div[1]/div[2]/ul/li[6]/span[2]/text()').extract_first()
        yield item
    def parse_detail(self,response):
        print("parse_detail")
        time.sleep(2)
        print(response.url)
        item = response.meta['item']
        #perple
        item['people'] = response.xpath('//*[@id="xqzl"]/div[3]/ul/li[3]/span[2]/text()').extract_first()
        url = response.xpath('//*[@id="xqzl"]/div[4]/a/@href').extract_first()
        if url:
            detail_url = "https://guangzhou.leyoujia.com/"+url
            # print(url)
            yield scrapy.Request(
                detail_url,
                callback=self.other,
                meta={"item": item}
            )
        else:
            item['purpose'] = None
            # item['people'] = None
            item['developers'] = None
            yield item

        # print(response.url)
        # # print(response.text)
        # content = re.findall(r'price: ".*',response.text)
        # # print(content)
        # price = re.sub(r'[price:",\r"]',"",content[0])
        # # print(price)
        # item['price'] = price
        # #单价
        # item['danjia'] = response.xpath('//*[@id="fjzs"]/div[2]/div[1]/span[2]/em[1]/text()').extract_first()+"元/㎡"
        # #y用途
        # item['purpose']=response.xpath('/html/body/div[6]/div[2]/div[4]/div[2]/div/p[3]/span[1]/text()').extract_first()
        #
        # #房源亮点
        # item['housing_lights'] = response.xpath('/html/body/div[6]/div[2]/div[7]/div[3]/div/text()').extract_first()
        # #绿化率
        # item['green'] = response.xpath('//*[@id="xqzl"]/div[3]/ul/li[7]/span[2]/text()').extract_first()
        # #Nature产品性质
        # item['nature'] = response.xpath('/html/body/div[6]/div[2]/div[4]/div[2]/div/p[4]/span[1]').extract_first()
        #
        # pa=response.xpath('//div[@class="cont"]/p')
        # for i in pa:
        #     # print(i)
        #     print("pa:",i.xpath('./text()').extract_first())
        #房源标签
        # tag1= response.xpath('/html/body/div[6]/div[2]/div[7]/div[2]/div/a/text()').extract_first()
        # tag2=response.xpath('/html/body/div[6]/div[2]/div[7]/div[2]/div/span[1]/text()').extract_first()

        # # resp2 = re.search(r'(?<="price":")(?P<price>.+?)(?=\")', response.text)
        # print(resp2)

        # print(item['price'])


        # item["danwei"] = response.xpath('/html/body/div[4]/div[2]/div[2]/div[1]/span/text()').extract_first()


