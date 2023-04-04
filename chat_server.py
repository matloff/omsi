import socket
import sys


def listener(port):
    soc = socket.socket()
    soc.bind(('', port))
    soc.listen(5)  # At most 5 students in queue
    print("Waiting for connections...")
    while True:
        client, address = soc.accept()
        question = client.recv(1024)
        question = question.decode()
        print(question)
        reply = input("Reply: ")
        client.send(str.encode(reply))
        client.close()


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 chat_server.py <port>")
        sys.exit(1)
    listener(int(sys.argv[1]))
