from socket import AF_INET, SOCK_STREAM, SOL_SOCKET, SO_REUSEADDR
from utils import utils
import socket
import os, sys, time

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

            self.server.settimeout(1.0)

            utils.generate_info("Server is listening on {}:{}".format(self.host, self.port))

            return True
        except OSError as e:
            utils.generate_error("An error occurred while starting the server...\nError: {}".format(e))
            return False
    
    def handle_connection(self) -> None:
        
        try:
            conn, addr = self.server.accept()
        except socket.timeout:
            return
        except KeyboardInterrupt:
            return
        while True:
            data = conn.recv(1024)

            if not data:
                utils.generate_info("Client closed the connection!")
                break
            
            message = data.decode("utf-8").strip()
            reply = "Unknown message: {!r}".format(message)
            utils.generate_info("Message received: {!r}".format(message))

            if message == "PING":
                reply = "PONG"

            conn.sendall(reply.encode("utf-8"))
            utils.generate_info(f"[Server] Sent: {reply!r}")

        conn.close()
        
if __name__ == "__main__":
    s = s_listener()
    try:
        if not s.start_server():
            exit(1)
        
        while True:
            try:
                s.handle_connection()
            except KeyboardInterrupt:
                break
    except KeyboardInterrupt:
        pass 
    s.server.close()