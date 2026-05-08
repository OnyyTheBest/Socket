from socket import AF_INET, SOCK_STREAM
from utils import utils
import socket
import os, sys, time

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
        #This function will connect to the server and "Ping" it by sending a message with "PING" in it, then it will wait for a response and print it to the final user!
        message = "PING"
        try:
            for i in range(1, 6):

                utils.generate_info("[Client] Send #{}: {!r}".format(i, message))
                self.client.sendall(message.encode('utf-8'))

                recv_data = self.client.recv(1024)
                utils.generate_info("[Client] Reply: {!r}".format(recv_data.decode('utf-8')))

                time.sleep(0.5)
        except Exception as e:
            utils.generate_error("An error occurred while handling question / answer\nError: {}".format(e))

        utils.generate_info("[Client] All pings sent. Closing connection.")
        self.client.close()

if __name__ == "__main__":
    s = c_connector()
    if not s.connect():
        sys.exit(1)

    s.handle_q_a()
    sys.exit(0)