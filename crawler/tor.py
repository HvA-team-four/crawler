import socket
import socks


def connectingtor():
    # Setting up the TOR proxy
    socksport = 9050  # The TOR proxy port that is default from torrc

    socks.set_default_proxy(socks.SOCKS5, "127.0.0.1", socksport)  # Defines the version, the host, the port
    socket.socket = socks.socksocket  # It builds a socket to TOR over the proxy client.

    # Perform DNS resolution through the socket to translate the DNS names to IP addresses
    def getaddrinfo(*args):  # create a tuple for
        return [(socket.AF_INET, socket.SOCK_STREAM, 6, '',
                 (args[0], args[1]))]  # Create the parameters for the socket.getaddrinfo

    socket.getaddrinfo = getaddrinfo  # See https://docs.python.org/2/library/socket.html for documentation
