import socket
import threading
# import time
import traceback
import subprocess
# import os
# import json

HOST = socket.gethostbyname(socket.gethostname())
PORT = 5050
LISTENER_LIMIT = 5
active_clients = {}
lock = threading.Lock()
subprocess.Popen(["python", "client.py"])


def listen_for_messages(client, username):
    try:
        while True:
            data = client.recv(4096)
            if not data:
                raise ConnectionError("Connection closed by client")

            # if data == b'SHUTDOWN':
            #     print("💻: Shutdown signal received from client.")
            #     break  # Exit the loop to gracefully close the connection

            try:
                decoded_data = data.decode('ascii')
                if decoded_data == 'exit':
                    print("the exit message got " + decoded_data)
                    exit_message = f"🏃{username} Left "
                    send_messages_to_all(exit_message)
                    with lock:
                        active_clients.pop(username)
                    client.close()
                    break
            except UnicodeDecodeError:
                pass

            else:
                message = data.decode('utf-8')
                log_message = f"{username}:{message}"
                send_messages_to_all(log_message)
            # print("datareceived from client " +data.decode('utf-8'))
    except ConnectionError as ce:
        print(f"Error in listen_for_messages for client {username}: {ce}")
    except Exception as e:
        print(f"Error in listen_for_messages for client {username}: {e}")
        traceback.print_exc()


def send_message_to_client(client, message):
    try:
        client.sendall(message.encode())
    except Exception as e:
        print(f"Error sending message to client: {e}")
        traceback.print_exc()


def send_messages_to_all(message):
    with lock:
        # receiver = message[:message.index(":")]
        msg = message.split(":")
        if msg[1].strip() == "all":
            for user, cl in active_clients.items():
                if cl != msg[0]:
                    send_message_to_client(cl, message)
        else:
            try:
                send_message_to_client(active_clients[msg[1]], message)
            except:
                print(msg[1], " is offline.")


def client_handler(client, address):
    try:
        while True:
            username = client.recv(2048).decode('utf-8')
            if username:
                with lock:
                    active_clients[username] = client
                join_message = f"{username}:all:joined the chat"
                send_messages_to_all(join_message)
                break
            else:
                print("Client username is empty")
    except Exception as e:
        print(f"Error in client_handler: {e}")
        traceback.print_exc()

    threading.Thread(target=listen_for_messages, args=(client, username)).start()


def main():

    # creating the server
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        server.bind((HOST, PORT))
        print(f"Running the server on {HOST}:{PORT}")
    except Exception as e:
        print(f"Unable to bind to host {HOST} and port {PORT}: {e}")
        traceback.print_exc()

    server.listen(LISTENER_LIMIT)

    while True:
        try:
            client, address = server.accept()
            print(f"💻: Successfully connected to client {address[0]}:{address[1]}")
            threading.Thread(target=client_handler, args=(client, address)).start()
        except Exception as e:
            print(f"Error accepting client connection: {e}")
            traceback.print_exc()


if __name__ == '__main__':
    main()
