from google import genai 
from stories_service import FormatedStory
import json


class TranslatorService:
    def __init__(self, client: genai.Client, model: str):
        self.client = client
        self.prompt: str =  """
                Você é um desenvolvedor de software e jornalista técnico brasileiro especializado em tecnologia.
                Sua tarefa é adaptar os títulos de notícias do Hacker News para o português do Brasil (PT-BR).
                REGRAS DE ADAPTAÇÃO:
                1. NÃO faça tradução literal "ao pé da letra". Adapte para manchetes fluídas e naturais de portais de tecnologia brasileiros.
                2. NUNCA traduza termos técnicos consagrados, nomes de linguagens ou frameworks (ex: Assembly, Rust, Python, JIT, AI, Prompt, Framework, Open Source).
                3. Mantenha os prefixos do Hacker News como "Show HN:", "Ask HN:", "Tell HN:" sem traduzir.
                4. Mantenha nomes de produtos, empresas e ferramentas no original (ex: DeepSeek, OpenAI, Linux, GitHub).
                5. O tom deve ser direto, moderno e atraente para devs brasileiros.
                Retorne APENAS um array JSON de strings com os títulos adaptados, mantendo a mesma ordem e formato.
                """
        self.model = model

    def translate_stories(self, formated_stories: list[FormatedStory]):
        input_data = json.dumps([{"title": story.title, "url": story.url} for story in formated_stories])
        full_prompt = f"{self.prompt}\n{input_data}"

        response = self.client.models.generate_content(
            model=self.model,
            contents=full_prompt,
            config={
                "response_mime_type": "application/json",
            }
        )

        if not response.text:
            print("API DO GEMINI RETORNOU VAZIO.")
            return
        
        translations: list[str] = json.loads(response.text)

        self._format_stories(translations, formated_stories)

        return formated_stories

    def _format_stories(self, translations: list[str], stories: list[FormatedStory]) -> None:
        for i, translation in enumerate(translations):
            stories[i].translated_title = translation