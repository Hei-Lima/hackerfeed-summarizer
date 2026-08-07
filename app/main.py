from google import genai
from dotenv import load_dotenv
from os import getenv
from translator_service import TranslatorService
from stories_service import StoriesService
from sender_service import SenderService
load_dotenv()


def main():
    print("Iniciando envio de mensagens...")

    client = genai.Client(api_key=getenv("GOOGLE_API_KEY"))
    model = getenv("GOOGLE_GEMINI_MODEL")

    print("Conseguindo as stories...")
    stories = StoriesService().GetStories()

    print("Traduzindo...")
    translated_stories = TranslatorService(client=client, model=model).TranslateStories(stories)

    sender = SenderService(translated_stories).Send()

    print(StoriesService.formatStoriesListToJson(translated_stories))
    

if __name__ == "__main__":
    main()