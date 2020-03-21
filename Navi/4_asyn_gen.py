import socket
from select import select
from collections import deque

to_read = dict()
to_write = dict()
tasks = deque()
log_out = list()


def server():
    """
    creates server socket. binds it to localhost's 100 port. And "listen" for any changes
    """
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, True)
    server_socket.bind(('localhost', 100))
    server_socket.listen()

    while True:

        yield 'read', server_socket  # don't let stuck up in ...accept(). Go further if there is any connection
        client_socket, address = server_socket.accept()  # read

        print(f"Connection from {address}")
        tasks.append(client(client_socket, address))


def client(client_socket, address):
    while True:

        yield 'read', client_socket
        request = client_socket.recv(1024)              # read

        if not request:
            break
        else:
            response = "Hello from server!\n ".encode()

            yield 'write', client_socket
            client_socket.send(response)                # write

    log_out.append(address)
    client_socket.close()


def event_loop():

    while any([tasks, to_read, to_write]):

        while not tasks:                    # if "tasks" list is empty

            ready_to_read, ready_to_write, _ = select(to_read, to_write, [])    # we get dict keys; keys are sockets

            for sock in ready_to_read:
                tasks.append(to_read.pop(sock))     # append to deque generators

            for sock in ready_to_write:
                tasks.append(to_write.pop(sock))    # append to deque generators

        try:
            task = tasks.popleft()          # task is generator

            reason, sock = next(task)       # ('write', client_socket)

            if reason == 'read':
                to_read[sock] = task        # add to dict generators as value of socket key
            if reason == 'write':
                to_write[sock] = task       # add to dict generators as value of socket key

        except StopIteration:
            print(f'User: {log_out.pop()} log out.')


tasks.append(server())
event_loop()

