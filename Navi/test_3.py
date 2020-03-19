import socket
import selectors

selector = selectors.DefaultSelector()


def server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # SOCK_STREAM == tcp protocol
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, True)
    server_socket.bind(('localhost', 1234))
    server_socket.listen()
    selector.register(fileobj=server_socket, events=selectors.EVENT_READ, data=accept_connection)


def accept_connection(server_socket):
    client_socket, address = server_socket.accept()         # приниает входящее подключение и возвращает кортеж
    print(f"Connection from {address}")
    selector.register(fileobj=client_socket, events=selectors.EVENT_READ, data=send_message)


def send_message(client_socket):
    request = client_socket.recv(4096)              # запрос клиента. Определяем размер буфера для сообщения

    if request:
        response = "Hello client\n".encode()
        client_socket.send(response)
    else:
        print('closing', client_socket)
        selector.unregister(client_socket)
        client_socket.close()


def even_loop():
    while True:
        events = selector.select()              # (key, mask)
        for key, _ in events:
            callback = key.data
            callback(key.fileobj)


if __name__ == '__main__':
    server()
    even_loop()


