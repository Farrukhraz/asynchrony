import socket

# socket = domain:port (localhost:5000)

# это серверный сокет, серверная сторона
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)       # SOCK_STREAM == tcp protocol
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, True)
server_socket.bind(('localhost', 100))
server_socket.listen()

# это клиентский сокет, клиентская сторона
while True:
    print("Before accept()")
    client_socket, address = server_socket.accept()         # приниает входящее подключение и возвращает кортеж
    print(f"Connection from {address}")

    while True:
        request = client_socket.recv(4096)              # запрос клиента. Определяем размер буфера для сообщения

        if not request:
            break
        else:
            response = "Hello client\n".encode()
            client_socket.send(response)
    print("We are outside inner while loop")
    client_socket.close()
