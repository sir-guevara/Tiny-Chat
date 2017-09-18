"""Chat software by MC Guevara"""
import socket
HOST = ''
PORT = 4040
def create_listen_socket(host, port):
    """ Setup the sockets our server will receive connection  
    requests on """
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind((host, port))
    sock.listen(100)
    return sock
def recv_msg(sock):
     """Wait for data to arrive on the socket, then parse into  
    messages using b'\0' as message delimiter """
     data = bytearray()
     msg = ''
    # Repeatedly read 4096 bytes off the socket, storing the bytes
   # data until we see a delimiter
     while not msg:
        recvd = sock.recv(4096)
        if not recvd:
            # Socket has been closed prematurely
            raise ConnectionError()
        data = data + recvd
        if b'\0' in recvd:
            # we know from our protocol rules that we only send
            # one message per connection, so b'\0' will always be
            # the last character
            msg = data.rstrip(b'\0')
     msg = msg.decode('utf-8')
     return msg
def prep_msg(msg):
    # Prepare a string to be sent as a message 
    msg += '\0'
    return msg.encode('utf-8')
def send_msg(sock, msg):
   #Send a string over a socket, preparing it first 
    data = prep_msg(msg)
    sock.sendall(data)
def parse_recvd_data(data):
    """ Break up raw received data into messages, delimited
        by null byte """
    parts = data.split(b'\0')
    msgs = parts[:-1]
    rest = parts[-1]
    return (msgs, rest)
def recv_msgs(sock, data=bytes()):
    """ Receive data and break into complete messages on null byte
       delimiter. Block until at least one message received, then
       return received messages """
    msgs = []
    while not msgs:
        recvd = sock.recv(4096)
        if not recvd:
            raise ConnectionError()
        data = data + recvd
        (msgs, rest) = parse_recvd_data(data)
    msgs = [msg.decode('utf-8') for msg in msgs]
    return (msgs, rest)
