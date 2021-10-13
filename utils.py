import socket
import pickle
import struct

GET_ALL_CLIENTS = "GET_ALL_CLIENTS"


def send(channel, *args):
    buffer = pickle.dumps(args)
    value = socket.htonl(len(buffer))
    size = struct.pack("L", value)
    channel.send(size)
    channel.send(buffer)


def receive(channel):
    size = struct.calcsize("L")
    size = channel.recv(size)
    try:
        size = socket.ntohl(struct.unpack("L", size)[0])
    except struct.error as e:
        return ''
    buf = ""
    while len(buf) < size:
        buf = channel.recv(size - len(buf))
    return pickle.loads(buf)[0]


def send_list_clients(sock, requesting_client_name, list_clients: list):
    # print log message
    print(
        f"Sending a list of clients to '{requesting_client_name}'")

    # Send the list of clients back to the requesting client
    send(sock, list_clients)


def receieve_list_clients(list_clients):
    # Sort the clients by name in alphabetical order
    list_clients.sort()

    # Turn the list into a csv string
    formatted_clients = ', '.join(list_clients)

    return formatted_clients
