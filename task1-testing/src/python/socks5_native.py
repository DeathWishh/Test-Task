import ctypes
import os
from ctypes import c_uint8, c_uint16, c_size_t, c_int, c_bool, Structure, POINTER, cast, Union
from typing import Tuple, Optional

# Загружаем C библиотеку
current_dir = os.path.dirname(os.path.abspath(__file__))
lib_path = os.path.join(current_dir, '..', 'c', 'libsocks5_parser.so')
socks5_lib = ctypes.CDLL(lib_path)

# Определяем структуры для Python
class Socks5Handshake(Structure):
    _fields_ = [
        ("version", c_uint8),
        ("nmethods", c_uint8),
        ("methods", c_uint8 * 255)
    ]

class Socks5Domain(Structure):
    _fields_ = [
        ("len", c_uint8),
        ("name", c_uint8 * 255)
    ]

class Socks5Request(Structure):
    class Domain(Structure):
        _fields_ = [
            ("len", c_uint8),
            ("name", c_uint8 * 255)
        ]
    
    class AddrUnion(Union):
        _fields_ = [
            ("ipv4", c_uint8 * 4),
            ("ipv6", c_uint8 * 16),
            ("domain", Socks5Domain)
        ]
    
    _fields_ = [
        ("version", c_uint8),
        ("cmd", c_uint8),
        ("rsv", c_uint8),
        ("atyp", c_uint8),
        ("dst_addr", AddrUnion),
        ("dst_port", c_uint16)
    ]

# Определяем сигнатуры функций
socks5_lib.parse_socks5_handshake.argtypes = [
    ctypes.POINTER(c_uint8),  # data
    c_size_t,                 # len
    ctypes.POINTER(Socks5Handshake)  # handshake
]
socks5_lib.parse_socks5_handshake.restype = c_int

socks5_lib.parse_socks5_request.argtypes = [
    ctypes.POINTER(c_uint8),  # data
    c_size_t,                 # len  
    ctypes.POINTER(Socks5Request)  # request
]
socks5_lib.parse_socks5_request.restype = c_int

def parse_handshake(data: bytes) -> Tuple[bool, Optional[Socks5Handshake]]:
    """Парсит SOCKS5 handshake используя C библиотеку"""
    handshake = Socks5Handshake()
    data_array = (c_uint8 * len(data))(*data)
    
    result = socks5_lib.parse_socks5_handshake(data_array, len(data), handshake)
    return result == 0, handshake if result == 0 else None    

def parse_request(data: bytes) -> Tuple[bool, Optional[Socks5Request]]:
    """Парсит SOCKS5 request используя C библиотеку"""
    request = Socks5Request()
    data_array = (c_uint8 * len(data))(*data)
    
    result = socks5_lib.parse_socks5_request(data_array, len(data), request)
    
    # Добавим отладочный вывод
    if result != 0:
        print(f"Parse request failed with error code: {result}")
        print(f"Data length: {len(data)}")
        print(f"Data: {data.hex()}")
    
    return result == 0, request if result == 0 else None
