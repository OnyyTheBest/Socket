from socket import AF_INET, SOCK_STREAM
from utils import utils
import socket, yt_dlp
import os, sys, json

class c_connector():

   
    def __init__(self) -> None:
        
        # The client will use these two variables to connect to the server!

        self.host: str = "127.0.0.1"
        self.port: int = 65432


        # Here we define the variable that we'll use for establish the connection and (send/receive) data.
        self.client: socket.socket = socket.socket(AF_INET, SOCK_STREAM)

    def connect(self) -> bool:
        #This function uses exception launched by the socket library for checking the connection, and it will also send an error / success message to the final user.

        try:
            self.client.connect((self.host, self.port))
            utils.generate_info("Connection established!")
            return True
        except ConnectionRefusedError or ConnectionError:
            utils.generate_error("An error occurred while connecting to the server!")
            return False

    def handle_q_a(self) -> None:
        
        while True:
            try:
                print("[0]Cerca canzone\n[1]Esci")
                s = input("Fai la tua scelta > ")

                if int(s) == 1:
                    self.client.sendall(
                        json.dumps(
                            {
                                "activity": "quit"
                            }
                        ).encode('utf-8')
                    )
                    self.client.close()
                    break
                
                s = input("Che canzone vuoi cercare? > ")
                self.client.sendall(
                    json.dumps(
                        {
                            "activity": "search",
                            "query": s
                        }
                    ).encode('utf-8')
                )

                result = json.loads(self.client.recv(1024).decode('utf-8'))

                song_name:str = result["result"]["song_name"]
                artist:str = result["result"]["song_author"]
                video_id:str = result["result"]["song_video_id"]

                s = input("E' questa la canzone da te richiesta? {} di {}? (y/n) > ".format(song_name, artist)).strip()[0]
                if s == "n":
                    continue
                
                link = "https://music.youtube.com/watch?v={}".format(video_id)
                with yt_dlp.YoutubeDL({'extract_audio': True, 'format': 'bestaudio', 'outtmpl': '%(title)s.mp3'}) as video:
                    info_dict = video.extract_info(link, download = True)
                    video_title = info_dict['title']
                    print(video_title)
                    video.download(link)    
            except Exception as e:
                utils.generate_error("An error occurred while handling the request!\nError: {}".format(e))

            utils.generate_info("[Client] All pings sent. Closing connection.")
        self.client.close()

if __name__ == "__main__":
    s = c_connector()
    if not s.connect():
        sys.exit(1)

    try:
        s.handle_q_a()
    except KeyboardInterrupt:
        sys.exit(0)
    sys.exit(0)