import requests
from dataclasses import dataclass, asdict
import json

@dataclass
class FormatedStory:
    id: int 
    title: str
    likes: int
    url: str
    translated_title: str | None = None

class StoriesService:
    def GetStories(self, top: int = 5):
        stories_id = self._FetchTopStoriesIds(top)
        formated_stories = self._FetchTopStoriesContent(stories_id)
            
        return formated_stories

    def _FetchTopStoriesIds(self, top: int):
        fetch_url = "https://hacker-news.firebaseio.com/v0/topstories.json"
        response = requests.get(fetch_url)
        stories = response.json()
        top_stories = stories[0:top]

        return top_stories

    def _FetchTopStoriesContent(self, ids: list[int]) -> list[FormatedStory]:
        formated_stories: list[FormatedStory] = list()

        for id in ids:
            fetch_url = f"https://hacker-news.firebaseio.com/v0/item/{id}.json"
            response = requests.get(fetch_url)
            story = response.json()
            formated_story = FormatedStory(id=id, title=story["title"], likes=story["score"], url=story["url"])

            formated_stories.append(formated_story)

        return formated_stories

    @staticmethod
    def formatStoriesListToJson(formated_stories: list[FormatedStory]):
        stories_dict = [asdict(story) for story in formated_stories]
        json_output = json.dumps(stories_dict, ensure_ascii=False, indent=2)

        return json_output