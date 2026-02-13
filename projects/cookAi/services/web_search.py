import json
from projects.cookAi.services.personas import cookai_client, make_web_search_prompt
from projects.cookAi.settings.security import GEMINI_MODEL

def search_recipes_from_web(query):
    prompt_content = make_web_search_prompt(query)

    response = cookai_client.models.generate_content(
        model=GEMINI_MODEL,
        contents=prompt_content
    )
    try:
        raw_text = response.text.strip()
        # print("Receitas extraídas \n")
        # print(raw_text)
        
        start_index = raw_text.find('[')
        end_index = raw_text.rfind(']')

        if start_index != -1 and end_index != -1:
            json_str = raw_text[start_index : end_index + 1]
            return json.loads(json_str)
        
        return raw_text
    
    except Exception as e:
        return {"error": f"Não é possível interpretar resposta: {e}"}


