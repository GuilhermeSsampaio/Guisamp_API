import time
from bs4 import BeautifulSoup
from google import genai
from urllib.parse import urlparse
import cloudscraper
from projects.cookAi.services.cookai import cookai, make_prompt 

def scrap_recipe(url: str):
    """
    Faz o scrapping da receita da url recebida e retorna sem conteúdo limpo
    """
    start_time = time.time()
    parsed_url = urlparse(url)
    font_of_url = parsed_url.netloc

    scraper = cloudscraper.create_scraper()

    try:
        # Fazendo req http
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }

        response = scraper.get(url, headers=headers, timeout=10)
        print(f"HTTP request completed with status code {response.status_code}.")
        response.raise_for_status()

        # parsing html
        soup = BeautifulSoup(response.text, "html.parser")

        # remove tags script e style
        for script in soup(["script", "style"]):
            script.decompose()

        text = soup.get_text(separator="\n", strip=True)

        conversion_time = time.time() - start_time
        print(f"Tempo de conversão: {conversion_time:.2f} segundos")

        prompt_content = make_prompt(text, font_of_url)

        model_start_time = time.time()
        response = cookai.models.generate_content(
            model="gemini-2.5-flash",
            contents= prompt_content
        )

        model_time = time.time() - model_start_time
        print(f"Tempo de processamento do modelo: {model_time:.2f} segundos")
        
        total_time = time.time() - start_time
        print(f"Tempo total de execução: {total_time:.2f} segundos")
        print(f"Receita extraída: {response.text}")
        
        return response.text

    except Exception as error:
        return {"error": f"Failed to scrape recipe from {url}: {error}"}


# url_teste = "https://www.tudogostoso.com.br/receita/23-bolo-de-cenoura.html"    
# url_teste = "https://www.receitasnestle.com.br/receitas/bolo-de-limao-de-liquidificador"    

# # ALTERAÇÃO AQUI: Imprima o resultado da função
# resultado = scrap_recipe(url_teste)
# print(resultado)