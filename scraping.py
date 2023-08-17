from custom_parser import Parser
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
import re


class ScrapingSpider(CrawlSpider):
    """
    Core class, where all logic is done. 
    Basic generated spider with some result validation.
    """
    name = "scraping"
    start_urls = []

    rules = (Rule(LinkExtractor(), callback="parse_item", follow=False),)

    def __init__(self, category="", **kwargs):
        """
        Accept URL from user-submitted form.
        """
        self.myBaseUrl = category
        self.start_urls.append(self.myBaseUrl)
        super().__init__(**kwargs)

    def parse_item(self, response):
        emails = self.extract_emails(response.text)
        for email in emails:
            yield {
                'URL': response.url,
                'Email': email,
            }

    def extract_emails(self, text):
        emails = re.findall(r'[\w\.-]+@[\w\.-]+\.\w+', text)
        valid_emails = []

        email_parser = Parser()

        for email in emails:
            if email_parser.parse(email):
                valid_emails.append(email)
        
        return valid_emails