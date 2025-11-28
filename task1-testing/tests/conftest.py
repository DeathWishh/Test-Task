
import pytest
import sys
import os
import tempfile

# Добавляем путь к src/python в PYTHONPATH
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src', 'python'))

from socks5_proxy import Socks5Proxy

@pytest.fixture(scope="session")
def compiled_library():
    """Фикстура для проверки скомпилированной C библиотеки"""
    lib_path = os.path.join(
        os.path.dirname(__file__), 
        '..', 'c', 'libsocks5_parser.so'
    )
    
    if not os.path.exists(lib_path):
        pytest.skip("C library not compiled. Run 'make' first.")
    
    return lib_path

@pytest.fixture
def sample_handshake():
    """Образец корректного handshake"""
    return b'\x05\x01\x00'

@pytest.fixture
def sample_ipv4_request():
    """Образец IPv4 запроса"""
    return b'\x05\x01\x00\x01\x7f\x00\x00\x01\x04\x38'

@pytest.fixture
def sample_domain_request():
    """Образец доменного запроса"""
    return b'\x05\x01\x00\x03\x0bexample.com\x00\x50'
