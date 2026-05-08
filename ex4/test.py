from innertube import InnerTube
import json

class youtube_music_metadata():

    def __init__(self, name: str, author: str, video_id: str):
        self.name: str = name
        self.author: str = author
        self.video_id: str = video_id

    def toDict(self) -> dict:
        return {
            "song_name": self.name,
            "song_author": self.author,
            "song_video_id": self.video_id
        }


class youtube_music_query():

    @staticmethod
    def search_song(query: str) -> json.dumps:

        songs = []

        client = InnerTube("WEB_REMIX")

        query_result = client.search(query)

        sections = query_result["contents"]["tabbedSearchResultsRenderer"]["tabs"]

        for tab in sections:

            tab_renderer = tab.get("tabRenderer")

            if not tab_renderer:
                continue

            content = (
                tab_renderer
                .get("content", {})
                .get("sectionListRenderer", {})
                .get("contents", [])
            )

            for section in content:

                music_shelf = section.get("musicShelfRenderer")

                if not music_shelf:
                    continue

                for item in music_shelf.get("contents", []):

                    renderer = item.get("musicResponsiveListItemRenderer")

                    if not renderer:
                        continue

                    
                
                    # video_id = None

                    # # prova watchEndpoint
                    # endpoint = renderer.get("navigationEndpoint", {})
                    # video_id = endpoint.get("watchEndpoint", {}).get("videoId")

                    # # fallback: alcuni risultati usano questa struttura
                    # if not video_id:
                    #     video_id = endpoint.get("watchEndpoint", {}).get("videoId")

                    # if not video_id:
                    #     video_id = (
                    #         renderer
                    #         .get("overlayNavigationEndpoint", {})
                    #         .get("watchEndpoint", {})
                    #         .get("videoId")
                    #     )

                    # if not video_id:
                    #     continue

                    flex_columns = renderer.get("flexColumns", [])

                    if len(flex_columns) < 2:
                        continue

                    try:
                        title = (
                            flex_columns[0]
                            ["musicResponsiveListItemFlexColumnRenderer"]
                            ["text"]["runs"][0]["text"]
                        )

                        subtitle_runs = (
                            flex_columns[1]
                            ["musicResponsiveListItemFlexColumnRenderer"]
                            ["text"]["runs"]
                        )

                    except (KeyError, IndexError):
                        continue

                    subtitle = "".join(
                        run.get("text", "")
                        for run in subtitle_runs
                    )

                    parts = [p.strip() for p in subtitle.split("•")]

                    if len(parts) < 2:
                        continue

                    artist = parts[1]
                    video_id = renderer.get("playlistItemData", {}).get("videoId", None)
                    if video_id:
                        songs.append(
                            youtube_music_metadata(
                                title,
                                artist,
                                video_id
                            ).toDict()
                        )

        return json.dumps(songs, ensure_ascii=False, indent=2)


res = youtube_music_query.search_song("Peccati")

