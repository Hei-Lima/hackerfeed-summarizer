import requests
from stories_service import FormatedStory
from os import getenv
from datetime import datetime, timezone, timedelta

class SenderService:
    def __init__(self, formated_stories: list[FormatedStory]):
        self.formated_stories = formated_stories
        self.discord_webhook = getenv("DISCORD_WEBHOOK")

    def Send(self):
        text = self._FormatText()
        print(text) # antipadrao mas fodase

        payload = {
            "content": text
        }

        self.SendToDiscord(payload)

    def _FormatText(self):
        text = f"*Top histórias do Hacker News em {self._GetData()}, _Powered By Hackerfeed_*\n"
        for i, story in enumerate(self.formated_stories):
            story_text = f"{i+1}. {story.translated_title} ({story.likes} likes): {story.url}\n"
            text = text + story_text

        return text            

    def SendToDiscord(self, payload: dict):
        res = requests.post(self.discord_webhook, json=payload)
        return res.status_code 

    @staticmethod
    def _GetData():
        fuso_brasilia = timezone(timedelta(hours=-3))
        now_brasil = datetime.now(fuso_brasilia)

        return now_brasil