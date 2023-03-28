import scrapy
import re
import requests
import operator
import time
from scrapy.crawler import CrawlerProcess

class PCGamerArticlesSpider(scrapy.Spider):
    name = "pc_gamer_articles"
    start_urls = [
        'https://www.amazon.fr/s?field-keywords=pc+gamer+intel',
    ]
    
    # Méthode pour parser les données de la page Web
    def parse(self, response):
        # Liste pour stocker les produits
        products = []
        # Boucle pour extraire les informations sur chaque produit
        for article_html in response.css("div.s-result-item"):
            product = {
                'name': article_html.css("span.a-size-medium.a-color-base.a-text-normal::text").get(),
                'description': article_html.css("span.a-size-base-plus.a-color-base.a-text-normal::text").get(),
                'price': article_html.css("span.a-offscreen::text").get(),
                'image_urls': article_html.css("img.s-image::attr(src)").get(),
                'url': article_html.css("a.a-link-normal.a-text-normal::attr(href)").get()
            }
            price = product['price']
            # Vérifie si le prix est présent
            if price:
                # Supprime les caractères non numériques du prix
                price = re.sub(r'[^\d,]+', '', price)
                price = float(price.replace(',', '.'))
                product['price'] = price
                products.append(product)
        
        # Calcule la moyenne des prix de tous les produits
        avg_price = sum(product['price'] for product in products) / len(products)
        # Obtient les produits abordables (moitié du prix moyen à 50% de plus que le prix moyen)
        affordable_products = [product for product in products if avg_price * 0.5 <= product['price'] <= avg_price * 1.5]
        # Trie les produits abordables par ordre croissant de prix
        affordable_products = sorted(affordable_products, key=operator.itemgetter('price'))[:5]
        # Envoie un message Telegram disant "Les meilleurs articles Amazon PC gamer:"
        self.send_telegram_message("Les meilleurs articles Amazon PC gamer:")
        time.sleep(1)  # Pause de 1 seconde entre chaque envoi de message
        # Boucle pour envoyer des informations sur chaque produit abordable
        for product in affordable_products:
            message = f"Nom: {product['name']}\nDescription: {product['description']}\nPrix: {product['price']}\nImage: {product['image_urls']}\nLien: {product['url']}"
            self.send_telegram_message(message)
            time.sleep(1)  # Pause de 1 seconde entre chaque envoi de message
        self.send_telegram_message("Pour d'autre type d'information que vous voulez extraire , merci de bien vouloir laisser un message dans se canal !")
    # methode qui s'exécute lorsque l'objet spider est créer
    def start_requests(self):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.66 Safari/537.3',
        }
        for url in self.start_urls:
            yield scrapy.Request(url, headers=headers)
            
    def send_telegram_message(self, message):
        # Stocker la clé d'API du bot Telegram
        bot_api_key = "6109881069:AAE8rvdnNYCkGaIzGgz3G93iGhbdh3nu2ZA"
        # Stocker l'identifiant de chat où les messages seront envoyés
        chat_id = "-1001538073569"
        # Créer l'URL pour envoyer un message via l'API Telegram
        url = f"https://api.telegram.org/bot{bot_api_key}/sendMessage?chat_id={chat_id}&text={message}"
        # Envoyer une requête GET à l'URL pour envoyer un message
        requests.get(url)
        
if __name__ == "__main__":
    process = CrawlerProcess(settings={
        "FEEDS": {
            "products.json": {"format": "json"},
        },
    })

    process.crawl(PCGamerArticlesSpider)
    process.start()