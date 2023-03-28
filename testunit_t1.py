import unittest
from scrapy.http import HtmlResponse
from traitement_1 import PCGamerArticlesSpider

class TestPCGamerArticlesSpider(unittest.TestCase):

    def setUp(self):
        self.spider = PCGamerArticlesSpider()

    def test_parse(self):
        # Créer une réponse factice à partir d'un fichier HTML de test
        with open('test_response.html', 'r') as f:
            html_content = f.read()
        response = HtmlResponse(url='https://www.amazon.fr/s?field-keywords=pc+gamer+intel', body=html_content, encoding='utf-8')

        # Appeler la méthode parse de la classe Spider et vérifier la sortie
        parsed_data = self.spider.parse(response)
        self.assertEqual(len(parsed_data), 1)
        self.assertEqual(parsed_data[0]['name'], 'Produit 1')
        self.assertEqual(parsed_data[0]['description'], 'Description du produit 1')
        self.assertEqual(parsed_data[0]['price'], 1099.99)
        self.assertEqual(parsed_data[0]['image_urls'], 'https://www.example.com/image1.jpg')
        self.assertEqual(parsed_data[0]['url'], 'https://www.example.com/produit1.html')

        
if __name__ == '__main__':
    unittest.main()
     