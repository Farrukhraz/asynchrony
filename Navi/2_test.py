import socket
from select import select

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # SOCK_STREAM == tcp protocol
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, True)
server_socket.bind(('localhost', 100))
server_socket.listen()

TO_MONITOR = list()


def accept_connection(server_socket):
    client_socket, address = server_socket.accept()         # приниает входящее подключение и возвращает кортеж
    print(f"Connection from {address}")

    TO_MONITOR.append(client_socket)


def send_message(client_socket):
    request = client_socket.recv(4096)              # запрос клиента. Определяем размер буфера для сообщения

    if request:
        response = "Hello client\n".encode()
        client_socket.send(response)
    else:
        client_socket.close()


def even_loop():
    while True:

        ready_for_read, _, _ = select(TO_MONITOR, [], [])   # select(read, write, errors)

        for sock in ready_for_read:
            if sock is server_socket:
                accept_connection(sock)
            else:
                send_message(sock)


if __name__ == '__main__':
    print(server_socket)
    TO_MONITOR.append(server_socket)
    even_loop()


