import sys
import os

# Добавляем путь к src/python для импортов
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src', 'python'))

from socks5_native import parse_handshake, parse_request, Socks5Handshake, Socks5Request

class TestSocks5Parser:
    """Unit-тесты для C библиотеки парсинга SOCKS5"""
    
    def test_handshake_valid(self):
        """Тест корректного handshake пакета"""
        data = b'\x05\x01\x00'
        success, handshake = parse_handshake(data)
        
        assert success == True
        assert handshake.version == 5
        assert handshake.nmethods == 1
        assert handshake.methods[0] == 0
    
    def test_handshake_invalid_version(self):
        """Тест handshake с неверной версией"""
        data = b'\x04\x01\x00'  # Wrong version
        success, handshake = parse_handshake(data)
        assert success == False
    
    def test_handshake_insufficient_data(self):
        """Тест handshake с недостаточными данными"""
        data = b'\x05'  # Only version
        success, handshake = parse_handshake(data)
        assert success == False
    
    def test_request_ipv4(self):
        """Тест IPv4 запроса"""
        # SOCKS5 CONNECT to 127.0.0.1:1080
        data = b'\x05\x01\x00\x01\x7f\x00\x00\x01\x04\x38'
        success, request = parse_request(data)
        
        assert success == True
        assert request.version == 5
        assert request.cmd == 1  # CONNECT
        assert request.atyp == 1  # IPv4
        #assert list(request.dst_addr.ipv4.addr) == [127, 0, 0, 1]
        assert list(request.dst_addr.ipv4) == [127, 0, 0, 1]
        assert request.dst_port == 1080  # 0x0438 = 1080
    
    def test_request_domain(self):
        """Тест доменного запроса"""
        # SOCKS5 CONNECT to example.com:80
        data = b'\x05\x01\x00\x03\x0bexample.com\x00\x50'
        success, request = parse_request(data)
        
        assert success == True
        assert request.atyp == 3  # Domain
        # Используем правильный способ чтения домена
        #domain_bytes = bytearray(request.dst_addr.domain.name)
        #domain_str = domain_bytes[:request.dst_addr.domain.len].decode('utf-8')
        # В test_socks5_parser.py замените все случаи чтения домена:
        domain_bytes = list(request.dst_addr.domain.name)[:request.dst_addr.domain.len]
        domain_str = bytes(domain_bytes).decode('utf-8')
        assert domain_str == 'example.com'
        assert request.dst_port == 80
    
    def test_request_invalid_data(self):
        """Тест некорректного запроса"""
        data = b'\x05\x01\x00'  # Incomplete
        success, request = parse_request(data)
        assert success == False
    
    def test_request_unsupported_atyp(self):
        """Тест неподдерживаемого типа адреса"""
        data = b'\x05\x01\x00\x02\x00\x50'  # Unsupported atyp=2
        success, request = parse_request(data)
        assert success == False

class TestEdgeCases:
    """Тесты edge cases"""
    
    def test_handshake_multiple_methods(self):
        """Тест handshake с несколькими методами"""
        data = b'\x05\x03\x00\x01\x02'  # 3 methods: 0, 1, 2
        success, handshake = parse_handshake(data)
        
        assert success == True
        assert handshake.nmethods == 3
        # Проверяем только первые 3 метода
        methods_list = [handshake.methods[i] for i in range(3)]
        assert methods_list == [0, 1, 2]
    
    def test_request_max_domain_length(self):
        """Тест максимальной длины домена"""
        # Максимальная длина теперь 254 (не 255)
        long_domain = b'a' * 254
        data = b'\x05\x01\x00\x03' + bytes([254]) + long_domain + b'\x00\x50'
        success, request = parse_request(data)
        
        assert success == True
        assert request.dst_addr.domain.len == 254
        
        # Проверяем содержимое домена
        #domain_bytes = bytearray(request.dst_addr.domain.name)
        #domain_str = domain_bytes[:request.dst_addr.domain.len].decode('utf-8')
        domain_bytes = list(request.dst_addr.domain.name)[:request.dst_addr.domain.len]
        domain_str = bytes(domain_bytes).decode('utf-8')
        assert len(domain_str) == 254
        assert domain_str == 'a' * 254
    
    def test_request_domain_too_long(self):
        """Тест слишком длинного домена"""
        long_domain = b'a' * 255
        data = b'\x05\x01\x00\x03' + bytes([255]) + long_domain + b'\x00\x50'
        success, request = parse_request(data)
        
        # Теперь должен вернуть ошибку
        assert success == False
    
    def test_zero_length_domain(self):
        """Тест домена нулевой длины"""
        data = b'\x05\x01\x00\x03\x00\x00\x50'
        success, request = parse_request(data)
        
        # Нулевая длина теперь не допускается
        assert success == False
    
    def test_valid_domain_min_length(self):
        """Тест домена минимальной длины"""
        data = b'\x05\x01\x00\x03\x01a\x00\x50'
        success, request = parse_request(data)
    
        # Добавим подробную отладочную информацию
        if not success:
            print(f"Failed to parse minimal domain request")
            print(f"Data: {data.hex()}")
            print(f"Expected: version=5, cmd=1, atyp=3, domain_len=1, domain='a', port=80")
    
        assert success == True
        if success:
            assert request.dst_addr.domain.len == 1
            domain_bytes = bytes(request.dst_addr.domain.name)[:request.dst_addr.domain.len]
            domain_str = domain_bytes.decode('utf-8')
            assert domain_str == 'a'
            assert request.dst_port == 80
    
    #def test_valid_domain_min_length(self):
    #    """Тест домена минимальной длины (1 символ)"""
    #    data = b'\x05\x01\x00\x03\x01a\x00\x50'
    #    success, request = parse_request(data)
    #    
    #    assert success == True
    #    assert request.dst_addr.domain.len == 1
    #    #domain_bytes = bytearray(request.dst_addr.domain.name)
    #    #domain_str = domain_bytes[:request.dst_addr.domain.len].decode('utf-8')
    #    domain_bytes = list(request.dst_addr.domain.name)[:request.dst_addr.domain.len]
    #    domain_str = bytes(domain_bytes).decode('utf-8')
    #    
    #    assert domain_str == 'a'
