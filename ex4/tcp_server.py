"""
SIMPLE Youtube music downloader!

this server will provide a link to a song listed on youtube music library excluding youtube music videos.

PROTOCOL: TCP
Why?: Speed is not something i need as much as stability, that's my way to shrink a much complex explenation on why i use TCP over UDP.

FOM (Format of messages): JSON
What happens if the client sends a malformed message?: the server just ignore the message.

Is there a termination condition, and if so, who initiates it?: When the client sends a message saying {"activity": "quit"} the server will close the connection
"""


from socket import AF_INET, SOCK_STREAM, SOL_SOCKET, SO_REUSEADDR
from innertube import InnerTube
from utils import utils
import socket
import os, sys, json

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
    def search_song(query: str) -> list[dict]:

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

        return songs

class s_listener():

    def __init__(self) -> None:
        
        # The server will use these two variables to establish a connection 
        
        self.host: str = "127.0.0.1"
        self.port: int = 65432

        self.server: socket.socket = socket.socket(AF_INET, SOCK_STREAM)

    def start_server(self) -> bool:
        
        try:
            self.server.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        
            self.server.bind((self.host, self.port))
        
            self.server.listen(1)

            return True
        except OSError as e:
            utils.generate_error("An error occurred while starting the server...\nError: {}".format(e))
            return False
    
    def handle_connection(self) -> None:
        
        utils.generate_info("Server is listening on {}:{}".format(self.host, self.port))
        conn, addr = self.server.accept()
        
        while True:
            data = conn.recv(1024)

            if not data:
                utils.generate_info("Client closed the connection!")
                break
            
            message = json.loads(data.decode("utf-8").strip())
            utils.generate_info("Message received: {!r}".format(message))

            if message["activity"] == "quit":
                break

            if message["activity"] == "search":
                query = message["query"]

                query_result: youtube_music_metadata = youtube_music_query().search_song(query)[0]
                conn.sendall(
                    json.dumps(
                        {
                            "status":"success",
                            "result": query_result
                        }
                    ).encode("utf-8")
                )

                

        conn.close()
        
if __name__ == "__main__":
    s = s_listener()
    if not s.start_server():
        exit(1)
    
    s.handle_connection()

    s.server.close()