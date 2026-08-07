import requests
from stories_service import FormatedStory
from os import getenv
from datetime import datetime, timezone, timedelta

class SenderService:
    def __init__(self, formated_stories: list[FormatedStory], discord_webhook: str | None = None):
        self.formated_stories = formated_stories
        self.discord_webhook = discord_webhook or getenv("DISCORD_WEBHOOK")

    def send(self):
        text = self._format_text()
        print(text)

        payload = {
            "content": text
        }

        return self.send_to_discord(payload)

    def _format_text(self):
        text = f"*Top histórias do Hacker News em {self._get_data().strftime('%d/%m/%Y %H:%M')}, _Powered By Hackerfeed_*\n"
        for i, story in enumerate(self.formated_stories):
            story_text = f"{i+1}. {story.translated_title} ({story.likes} likes): {story.url}\n"
            text = text + story_text

        return text            

    def send_to_discord(self, payload: dict):
        if not self.discord_webhook:
            raise ValueError("DISCORD_WEBHOOK não configurado.")
        res = requests.post(self.discord_webhook, json=payload)
        return res.status_code 

    @staticmethod
    def _get_data():
        fuso_brasilia = timezone(timedelta(hours=-3))
        now_brasil = datetime.now(fuso_brasilia)

        return now_brasil