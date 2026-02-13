from urllib import response
from google import genai
import os
from dotenv import load_dotenv

from projects.cookAi.settings.security import GOOGLE_API_KEY

load_dotenv()

cookai_client = genai.Client(api_key=GOOGLE_API_KEY)

def make_scrapping_prompt(text: str, font_of_url: str):
    scrap_persona = f"""
            Resuma essa receita, passando os ingredientes, tempo de forno e o modo de preparo:

            {text}
            
            Caso não tenha o tempo de forno indique o recomendado.
            Use títulos de seção para separar os ingredientes do modo de preparo.
            O título da receita deve ser o primeiro item do resumo e deve usar heading 1.
            Abaixo do titulo, coloque a fonte da receita (site) e o link. Pode utilizar a váriavel {font_of_url} para isso.
            Traduza para o português.
            """
    return scrap_persona

def make_web_search_prompt(query:str):
    
    search_persona = f"""
    Encontre receitas com base na seguinte especificação: {query}.
    Busque receitas populares e bem avaliadas na internet.
    Não invente receitas.
    Retorne as receitas no seguinte formato:
    [
        {{
            "title": "Título da receita",
            "font": "Fonte da receita",
            "link": "Link da receita",
            "content": "Descrição ou instruções da receita"
        }},
    ]
    """
    return search_persona
