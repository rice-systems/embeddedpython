# emulates Python socket layer

import ip

AF_INET = 1
SOCK_STREAM = 1

class socket:
    def __init__(self, address_family, socket_type):
        pass

    def bind(self, tup):
        host, port = tup
        ip.bind('', port)

    def listen(self, backlog):
        if not backlog==1:
            raise_user_ex("backlog must be 1")
        else:
            ip.listen(backlog)

    def accept(self):
        ip.accept()
        return (connection(), "(none)")

    def recv(self, n=0):
        # for now we ignore the maximum recv window
        return ip.recv()

    def send(self, s):
        ip.send(s)

    def close(self):
        ip.close()

class connection:
    def recv(self, n=0):
        return ip.recv()

    def send(self, s):
        ip.send(s)

    def close(self):
        ip.close()

ip.init()

