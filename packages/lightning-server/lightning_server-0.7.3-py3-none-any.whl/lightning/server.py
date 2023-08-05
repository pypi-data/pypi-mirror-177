import threading
import socket
from typing import Type
from ssl import SSLContext

import time
import logging

from . import utility, backend
from .structs import Node


def create_server_conn(server_addr: tuple, max_listen, reuse_port, reuse_addr, dualstack, timeout):
    if dualstack is None:
        dualstack = utility.get_socket_family(server_addr) == socket.AF_INET6 and socket.has_dualstack_ipv6()
    if reuse_port is None:
        reuse_port = hasattr(socket, 'SO_REUSEPORT')
    conn = socket.create_server(
        server_addr, family = utility.get_socket_family(server_addr),
        backlog = max_listen, reuse_port = reuse_port, dualstack_ipv6 = dualstack)
    conn.settimeout(timeout)
    conn.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, reuse_addr)
    return conn


class Server:
    """The HTTP server class"""

    def __init__(self, server_addr: tuple[str, int] = ('', 80), *, max_listen: int = 0, timeout: int = None,
                 ssl_cert: str = None, max_worker: int = None, backend_flag: str = 'thread', reuse_port: bool = None,
                 reuse_addr: bool = True, dualstack: bool = None, keep_alive_timeout: int = 75,
                 sock: socket.socket = None, **kwargs):
        """
        :param server_addr: the address of server (host, port)
        :param max_listen: max size of listener queue (0 for default value)
        :param timeout: timeout for server socket
        :param ssl_cert: SSL certificate content
        :param max_worker: max size of worker queue
        :param backend_flag: specify if this server use single processing or mulit-thread processing
        :param keep_alive_timeout: timeout for Keep-Alive in HTTP/1.1. Set it to 0 to disable it.
        :param reuse_port: whether server socket reuse port (set SO_REUSEPORT to 1)
        :param reuse_addr: whether server socket reuse address (set SO_REUSEADDR to 1)
        :param dualstack: whether server use IPv6 dualstack if possible
        :param sock: a given socket
        """
        self.runner = None
        self.backend_cls = backend.get_backend_class(backend_flag)
        self.connection_pool = backend.ConnectionPool(timeout = keep_alive_timeout)
        self.root_node = Node(desc = 'root_node', **kwargs)
        self.bind = self.root_node.bind  # create an alias

        self._sock = sock or create_server_conn(server_addr, max_listen, reuse_port, reuse_addr, dualstack, timeout)
        # not to use server_addr directly since server_addr could contain irregular address or port number
        self.addr = self._sock.getsockname()

        if ssl_cert:
            ssl_context = SSLContext()
            ssl_context.load_cert_chain(ssl_cert)
            self._sock = ssl_context.wrap_socket(self._sock, server_side = True)

        self.backend = self.backend_cls(sock = self._sock, root_node = self.root_node, conn_pool = self.connection_pool,
                                        max_worker = max_worker)

    def run(self, block: bool = True, quiet: bool = False):
        """
        start the server\n
        :param block: if it is True, this method will be blocked until the server shutdown or critical errors occoured
        :param quiet: whether server prints greeting message
        """
        logging.info(f'Listening request on {self.addr}')
        self.runner = threading.Thread(target = self.backend.run, daemon = True)
        self.runner.start()
        if not quiet:
            print(f'Server running on {self._sock.getsockname()}. Press Ctrl+C to quit.')

        if not block:
            return
        while self.runner.is_alive():
            try:
                time.sleep(1)
            except KeyboardInterrupt:
                self.terminate()
                return

    def interrupt(self, timeout: float = 30):
        """
        Stop the server temporarily. Call run() to start the server again.\n
        :param timeout: max time for waiting single active session
        """
        if not self.is_running:
            logging.warning('The server has already stopped, interrupting it will not take any effects.')
            return

        logging.info(f'Interrupting {self}')
        self.backend.interrupt()
        if self.runner.is_alive():
            logging.info('Waiting for backend...')
            self.runner.join(timeout)
        logging.info(f'{self} interrupted successfully.')

    def terminate(self):
        """
        Stop the server permanently. After running this method, the server cannot start again.
        """
        if not self.is_running:
            logging.warning('The server has already stopped.')
            return

        logging.info(f'Terminating {self}')
        self.backend.terminate()
        if self.runner.is_alive():
            logging.info('Terminating backend...')
            self.runner.join(1)  # leave 1 sec for backend to complete termination
        logging.info(f'{self} closed successfully.')

    @property
    def is_running(self):
        return self.backend.is_running

    def __enter__(self):
        self.run(block = False)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.is_running:
            self.terminate()
        return True

    def __del__(self):
        if hasattr(self, 'backend') and self.is_running:  # prevent crash when it is called as init doesn`t finish
            self.terminate()

    def __repr__(self) -> str:
        return f'Server[{"running" if self.is_running else "closed"} on {self.addr}]'


__all__ = ['Server']
