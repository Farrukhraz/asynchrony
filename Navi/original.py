import socket

# socket = domain:port (localhost:5000)

# это серверный сокет, серверная сторона
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)       # Создаем сокет; SOCK_STREAM - это tcp
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, True)  # не ждем пакеты после вырубания программы
server_socket.bind(('localhost', 100))                                  # привяжем сокет к адрессу
server_socket.listen()                                                  # Разрещить серверу получать подключения

# это клиентский сокет, клиентская сторона
while True:
    print("Before accept()")
    client_socket, address = server_socket.accept()     # приниает входящее подключение и возвращает кортеж. Функция
    print(f"Connection from {address}")                 # блокировка. Стопает выполнение программы

    while True:
        request = client_socket.recv(4096)              # Принимает данные от клиентского сокета. 4096 размер
                                                        # максимального размера буфера который может быть принят за раз
        if not request:
            break
        else:
            response = "What's your name?\nHello ".encode() + request
            client_socket.send(response)                # Отправляет ответ клиенту
    print("We are outside inner while loop")
    client_socket.close()
