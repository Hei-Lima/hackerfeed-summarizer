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
    def get_stories(self, top: int = 5) -> list[FormatedStory]:
        # Busca todas as notícias da front page em 1 ÚNICA chamada HTTP (API da Algolia)
        fetch_url = "https://hn.algolia.com/api/v1/search?tags=front_page"
        response = requests.get(fetch_url)
        data = response.json()

        hits = data.get("hits", [])
        formated_stories: list[FormatedStory] = []

        for item in hits:
            story_id = int(item.get("objectID", 0))
            title = item.get("title") or ""
            likes = int(item.get("points") or 0)
            url = item.get("url") or f"https://news.ycombinator.com/item?id={story_id}"

            if title:
                formated_stories.append(
                    FormatedStory(id=story_id, title=title, likes=likes, url=url)
                )

        # Ordena as notícias pelo número de likes (do maior para o menor)
        formated_stories.sort(key=lambda story: story.likes, reverse=True)

        # Retorna os top N mais curtidos
        return formated_stories[:top]

    @staticmethod
    def format_stories_list_to_json(formated_stories: list[FormatedStory]) -> str:
        stories_dict = [asdict(story) for story in formated_stories]
        return json.dumps(stories_dict, ensure_ascii=False, indent=2)

