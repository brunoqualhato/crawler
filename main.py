import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin

def crawl(url, max_depth=3):
    visited_urls = set()
    queue = [(url, 0)]

    while queue:
        current_url, depth = queue.pop(0)
        if depth > max_depth:
            continue

        if current_url in visited_urls:
            continue

        try:
            response = requests.get(current_url)
            if response.status_code == 200:
                visited_urls.add(current_url)
                soup = BeautifulSoup(response.content, 'html.parser')
                links = soup.find_all('a')
                with open(f'{urlparse(current_url).netloc}.txt', 'a') as file:
                    file.write(current_url + '\n')
                for link in links:
                    new_url = urljoin(current_url, link.get('href'))
                    queue.append((new_url, depth + 1))
            else:
                print("Erro ao acessar:", current_url)
        except Exception as e:
            print("Erro:", e)

        print("Visitando:", current_url)

# URL inicial para iniciar o rastreamento
initial_url = 'https://g1.globo.com'

# Chama a função crawl com a URL inicial
crawl(initial_url)
