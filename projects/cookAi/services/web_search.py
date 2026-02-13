from projects.cookAi.services.personas import cookai_client, make_web_search_prompt
from projects.cookAi.settings.security import GEMINI_MODEL


def search_recipes_from_web(query):
    prompt_content = make_web_search_prompt(query)

    response = cookai_client.models.generate_content(
        model=GEMINI_MODEL,
        contents=prompt_content
    )

    return response