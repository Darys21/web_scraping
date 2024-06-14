import scrapy
import re
import requests
import operator
import time
from scrapy.crawler import CrawlerProcess

class PCGamerArticlesSpider(scrapy.Spider):
    """Scraper for Amazon PC gamer articles."""

    name = "pc_gamer_articles"
    start_urls = [
        'https://www.amazon.fr/s?field-keywords=pc+gamer+intel',
    ]

    def parse(self, response):
        """Parse the webpage and extract product information."""
        products = self._extract_product_info(response)
        affordable_products = self._get_affordable_products(products)
        self._send_telegram_messages(affordable_products)

    def start_requests(self):
        """Return the start requests for the spider."""
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.66 Safari/537.3',
        }
        for url in self.start_urls:
            yield scrapy.Request(url, headers=headers)

    @staticmethod
    def _extract_product_info(response):
        """Extract product information from the webpage."""
        products = []
        for article_html in response.css("div.s-result-item"):
            product = {
                'name': article_html.css("span.a-size-medium.a-color-base.a-text-normal::text").get(),
                'description': article_html.css("span.a-size-base-plus.a-color-base.a-text-normal::text").get(),
                'price': article_html.css("span.a-offscreen::text").get(),
                'image_urls': article_html.css("img.s-image::attr(src)").get(),
                'url': article_html.css("a.a-link-normal.a-text-normal::attr(href)").get()
            }
            price = product['price']
            if price:
                price = re.sub(r'[^\d,]+', '', price)
                price = float(price.replace(',', '.'))
                product['price'] = price
                products.append(product)
        return products

    @staticmethod
    def _get_affordable_products(products):
        """Get affordable products based on average price."""
        avg_price = sum(product['price'] for product in products) / len(products)
        affordable_products = [product for product in products if avg_price * 0.5 <= product['price'] <= avg_price * 1.5]
        affordable_products = sorted(affordable_products, key=operator.itemgetter('price'))[:5]
        return affordable_products

    def _send_telegram_messages(self, affordable_products):
        """Send Telegram messages with product information."""
        for product in affordable_products:
            message = f"Nom: {product['name']}\nDescription: {product['description']}\nPrix: {product['price']}\nImage: {product['image_urls']}\nLien: {product['url']}"
            self.send_telegram_message(message)
            time.sleep(1)
        self.send_telegram_message("Pour d'autres types d'informations que vous voulez extraire, merci de bien vouloir laisser un message dans le canal !")

    def send_telegram_message(self, message):
        """Send a Telegram message."""
        bot_api_key = "6109881069:AAE8rvdnNYCkGaIzGgz3G93iGhbdh3nu2ZA"
        chat_id = "-1001538073569"
        url = f"https://api.telegram.org/bot{bot_api_key}/sendMessage?chat_id={chat_id}&text={message}"
        requests.get(url)

if __name__ == "__main__":
    process = CrawlerProcess(settings={
        "FEEDS": {
            "products.json": {"format": "json"},
        },
    })

    process.crawl(PCGamerArticlesSpider)
    process.start()
