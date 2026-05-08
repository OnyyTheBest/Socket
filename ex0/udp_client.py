from socket import AF_INET, SOCK_DGRAM
from utils import utils
import socket
import os, sys, time


class c_connector():
     
    def __init__(self) -> None:
        
        # The client will use these two variables to connect to the server!

        self.host: str = "127.0.0.1"
        self.port: int = 65432


        # Here we define the variable that we'll use for establish the connection and (send/receive) data.
        self.client: socket.socket = socket.socket(AF_INET, SOCK_DGRAM)
    
    def connect(self) -> bool:
        try:
            self.client.settimeout(2.0)
            utils.generate_info("Client UDP socket ready. Will send to {}:{}".format(self.host, self.port))
            return True
        except Exception as e:
            utils.generate_error("An error occurred while connecting to the server\nError: {}".format(e))
            return False

    def handle_q_a(self) -> None:
        #This function will connect to the server and "Ping" it by sending a message with "PING" in it, then it will wait for a response and print it to the final user!
        message = "PING"
        for i in range(1, 6):
            utils.generate_info("[Client] Send #{}: {!r}".format(i, message))
            self.client.sendto(message.encode('utf-8'), (self.host, self.port))
            try:
                data, server_addr = self.client.recvfrom(1024)
                
                data = data.decode("utf-8")

                utils.generate_info("[Client] Reply: {!r}".format(data))
            except socket.timeout:
                utils.generate_error("An error occurred while handling question / answer\nError: Timed out!")
            except ConnectionResetError as e:
                utils.generate_error("An error occurred while handling question / answer\nError: {}".format(e))
                exit(0)

            time.sleep(0.5)
        

        utils.generate_info("[Client] All pings sent. Closing connection.")
        self.client.close()
    
if __name__ == "__main__":
    s = c_connector()
    if not s.connect():
        sys.exit(1)

    s.handle_q_a()
    sys.exit(0)