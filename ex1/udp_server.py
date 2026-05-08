from socket import AF_INET, SOCK_DGRAM
from utils import utils
import socket
import os, sys, time

class s_listener():

    def __init__(self) -> None:
        
        # The server will use these two variables to establish a connection 
        
        self.host: str = "127.0.0.1"
        self.port: int = 65432

        self.server: socket.socket = socket.socket(AF_INET, SOCK_DGRAM)

    def start_server(self) -> bool:
        
        try:
            self.server.bind((self.host, self.port))
            
            self.server.settimeout(1.0)

            utils.generate_info("Server is listening on {}:{} for UDP datagrams".format(self.host, self.port))
            utils.generate_info("[Server] Press Ctrl+C to stop.\n")
            return True
        except OSError as e:
            utils.generate_error("An error occurred while starting the server...\nError: {}".format(e))
            return False

    def handle_connection(self) -> None:
            cnt = 0
            while True:
                try:
                    data, client_addr = self.server.recvfrom(1024)
                except socket.timeout:
                    continue
                except KeyboardInterrupt:
                    exit(0)
                message = data.decode("utf-8").strip()
                reply = "Unknown message: {!r}".format(message)
                utils.generate_info("Message received: {!r}".format(message))

                if message == "PING":
                    cnt += 1
                    reply = "PONG #{}".format(cnt)

                self.server.sendto(reply.encode("utf-8"), client_addr)
                utils.generate_info(f"[Server] Sent: {reply!r} back to {client_addr}")
        
if __name__ == "__main__":
    s = s_listener()
    try:
    
        if not s.start_server():
            exit(1)
        s.handle_connection()
        

    except KeyboardInterrupt:
        pass

    s.server.close()
    exit(0)