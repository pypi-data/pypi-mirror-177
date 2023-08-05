import socket
import ipaddress
from urllib.parse import unquote
from typing import Literal


class CaseInsensitiveDict(dict):
    def __init__(self, *args, **kwargs):
        new_args = []
        if args:
            for arg_obj in args[0]:
                new_args.append((arg_obj[0].lower(), arg_obj[1]))
        new_kwargs = {}
        for kwarg_key in kwargs:
            new_kwargs[kwarg_key.lower()] = kwargs[kwarg_key]
        super().__init__(new_args, **new_kwargs)

    def __setitem__(self, key: str, value):
        return super().__setitem__(key.lower(), value)

    def __getitem__(self, item: str):
        return super().__getitem__(item.lower())

    def get(self, __key: str, default = None):
        return super().get(__key.lower(), default)

    def update(self, __m, **kwargs):
        for key in __m:
            self[key.lower()] = __m[key]
        for k in kwargs:
            self[k.lower()] = kwargs[k]

    def __contains__(self, item):
        return super().__contains__(item.lower())

    def __or__(self, other) -> 'CaseInsensitiveDict':
        ret = CaseInsensitiveDict()
        ret.update(self)
        ret.update(other)
        return ret


def format_header(header: str) -> str:
    """
    format the given header. Example:format_header('connection:keep-alive') -> 'Connection:Keep-Alive'
    """
    return '-'.join(map(lambda x: x.capitalize(), header.split('-')))


def format_socket(conn: socket.socket):
    if getattr(conn, '_closed'):
        return '[CLOSED]'
    try:
        return f'{conn.getpeername()}[{conn.fileno()}]'
    except OSError:  # server socket
        return f'{conn.getsockname()}[{conn.fileno()}][SERVER]'


def recv_request_head(conn: socket.socket, readed: bytes = b'') -> bytes:
    """Receive HTTP header (like Host: localhost)"""
    stack = readed
    while b'\r\n\r\n' not in stack:
        current_recv = conn.recv(1)
        stack += current_recv
        if not current_recv:
            break
    return stack.split(b'\r\n\r\n')[0]


def recv_all(conn: socket.socket, buffer: int = 1024, blocking: bool = False) -> bytes:
    """Receive all data"""
    block_status = conn.getblocking()
    conn.setblocking(blocking)
    content = b''
    c = True
    try:
        while c:
            c = conn.recv(buffer)
            content += c
    except BlockingIOError:
        pass
    conn.setblocking(block_status)
    return content


def parse_req(content: bytes) -> dict:
    """Parse a request data into a dict object in order to construct a Request object"""
    try:
        content_seq = content.decode('utf-8')
    except UnicodeDecodeError:
        content_seq = content.decode('gbk')
    line, *head = content_seq.split('\r\n')
    method, uv = line.split(' ', 1)
    url, ver = uv.rsplit(' ', 1)

    url = unquote(url)
    path, param = url.split('?', 1) if '?' in url else (url, '')

    keyword, arg = {}, set()
    for p in param.split('&'):
        if '=' in p:
            k, w = p.split('=')
            keyword[k] = w
        else:
            arg.add(p)

    header = CaseInsensitiveDict()
    for h, v in (h.split(':', 1) for h in head):
        header[format_header(h.strip())] = v.strip()

    return {'method': method, 'url': path, 'keyword': keyword,
            'arg': arg, 'version': ver, 'header': header, 'query': '?' + param if param else ''}


def get_socket_family(address):
    if address[0] == '':
        return socket.AF_INET6 if socket.has_ipv6 else socket.AF_INET
    try:
        addr = ipaddress.ip_address(address[0])
    except ValueError:  # address might be a domain name, return the better one
        return socket.AF_INET6 if socket.has_ipv6 else socket.AF_INET
    return socket.AF_INET if isinstance(addr, ipaddress.IPv4Address) else socket.AF_INET6


HTTP_CODE = {
    100: "Continue",
    101: "Switching Protocols",
    102: "Processing",
    200: "OK",
    201: "Created",
    202: "Accepted",
    203: "Non-Authoritative Information",
    204: "No Content",
    205: "Reset Content",
    206: "Partial Content",
    207: "Multi-Status",
    300: "Multiple Choices",
    301: "Moved Permanently",
    302: "Move Temporarily",
    303: "See Other",
    304: "Not Modified",
    305: "Use Proxy",
    306: "Switch Proxy",
    307: "Temporary Redirect",
    400: "Bad Request",
    401: "Unauthorized",
    402: "Payment Required",
    403: "Forbidden",
    404: "Not Found",
    405: "Method Not Allowed",
    406: "Not Acceptable",
    407: "Proxy Authentication Required",
    408: "Request Timeout",
    409: "Conflict",
    410: "Gone",
    411: "Length Required",
    412: "Precondition Failed",
    413: "Request Entity Too Large",
    414: "Request-URI Too Long",
    415: "Unsupported Media Type",
    416: "Requested Range Not Satisfiable",
    417: "Expectation Failed",
    418: "I'm a teapot",
    421: "Misdirected Request",
    422: "Unprocessable Entity",
    423: "Locked",
    424: "Failed Dependency",
    425: "Too Early",
    426: "Upgrade Required",
    449: "Retry With",
    451: "Unavailable For Legal Reasons",
    500: "Internal Server Error",
    501: "Not Implemented",
    502: "Bad Gateway",
    503: "Service Unavailable",
    504: "Gateway Timeout",
    505: "HTTP Version Not Supported",
    506: "Variant Also Negotiates",
    507: "Insufficient Storage",
    509: "Bandwidth Limit Exceeded",
    510: "Not Extended",
    600: "Unparseable Response Headers"
}
Method = Literal['GET', 'POST', 'PUT', 'DELETE', 'HEAD', 'CONNECT', 'TRACE', 'OPTIONS', 'PATCH']
__all__ = ['recv_request_head', 'recv_all', 'parse_req', 'format_socket', 'get_socket_family',
           'HTTP_CODE', 'Method', 'CaseInsensitiveDict']
