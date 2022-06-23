import scrapy
from ..items import ScrapItem
from scrapy.http import FormRequest
from scrapy.mail import MailSender
from .. import settings
from scrapy.crawler import CrawlerProcess
import smtplib
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


# data that we bring and can store in form of html file

# class QuotesSpider(scrapy.Spider):
#     name = "spidername"

#     def start_requests(self):
#         urls = [
#             'https://quotes.toscrape.com/page/1/',
#             'https://quotes.toscrape.com/page/2/',
#         ]
#         for url in urls:
#             yield scrapy.Request(url=url, callback=self.parse)

#     def parse(self, response):
#         page = response.url.split("/")[-2]
#         filename = f'quotes-{page}.html'
#         with open(filename, 'wb') as f:
#             f.write(response.body)
#         self.log(f'Saved file {filename}')



class QuoteSpider(scrapy.Spider):
    name = 'spidername'
    page_number = 2
    start_urls = [
        'https://quotes.toscrape.com/page/1/'
    ]

    # def parse(self, response):
    #     token = response.css('form input::attr(value)').extract_first()
    #     return FormRequest.from_response(response, formdata={
    #         'csrf_token': token,
    #         'username': 'Dhruvi',
    #         'password': 'Dhruvi@2001'
    #     }, callback=self.start_scraping)

    def parse(self, response):        
        items = ScrapItem()
        all_div_quotes = response.css('div.quote')
        for quote in all_div_quotes:

            title = quote.css('span.text::text').extract()
            author = quote.css('.author::text').extract()
            tag = quote.css('.tag::text').extract()

            items['title'] = title
            items['author'] = author
            items['tag'] = tag

            yield items

        next_page = 'https://quotes.toscrape.com/page/' + str(QuoteSpider.page_number) + '/'
        if QuoteSpider.page_number < 11:
            QuoteSpider.page_number += 1
            yield response.follow(next_page, callback=self.parse)
    


# def send_mail(self, message, title):
#     print("Sending mail...........")
    
#     gmailUser = 'makatidhruvi@gmail.com'
#     gmailPassword = 'nirlhixkgermdfmu'
#     recipient = 'makatidhruvi@gmail.com'

#     msg = MIMEMultipart()
#     msg['From'] = gmailUser
#     msg['To'] = recipient
#     msg['Subject'] = title
#     msg.attach(MIMEText(message))

#     mailServer = smtplib.SMTP('smtp.gmail.com', 587)
#     mailServer.ehlo()
#     mailServer.starttls()
#     mailServer.ehlo()
#     mailServer.login(gmailUser, gmailPassword)
#     mailServer.sendmail(gmailUser, recipient, msg.as_string())
#     mailServer.close()
#     print("Mail sent")

# send_mail("some message", "Scraper Report", "title")