from urllib import response
from google import genai
import os
from dotenv import load_dotenv

load_dotenv()

cookai = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

def make_prompt(text: str, font_of_url: str):
    persona = f"""
            Resuma essa receita, passando os ingredientes, tempo de forno e o modo de preparo:

            {text}
            
            Caso não tenha o tempo de forno indique o recomendado.
            Use títulos de seção para separar os ingredientes do modo de preparo.
            O título da receita deve ser o primeiro item do resumo e deve usar heading 1.
            Abaixo do titulo, coloque a fonte da receita (site) e o link. Pode utilizar a váriavel {font_of_url} para isso.
            Traduza para o português.
            """
    return persona
