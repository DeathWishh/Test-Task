import pytest
import socket
import threading
import sys
import os
from unittest.mock import Mock, patch, MagicMock
import ctypes

# Добавляем путь к src/python для импортов
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src', 'python'))

from socks5_native import parse_handshake, parse_request, Socks5Handshake, Socks5Request
from socks5_proxy import Socks5Proxy

class TestProxyLogic:
    """Unit-тесты для логики прокси-сервера"""
    
    def test_proxy_initialization(self):
        """Тест инициализации прокси"""
        proxy = Socks5Proxy('127.0.0.1', 9999)
        assert proxy.host == '127.0.0.1'
        assert proxy.port == 9999
    
    @patch('socket.socket')
    def test_handle_connect_ipv4(self, mock_socket):
        """Тест обработки IPv4 подключения"""
        proxy = Socks5Proxy()
        
        # Mock клиентского сокета
        mock_client = MagicMock()
        
        # Создаем реальный SOCKS5 запрос с IPv4
        request = Socks5Request()
        request.cmd = 0x01  # CONNECT
        request.atyp = 0x01  # IPv4
        # Создаем массив для IPv4 адреса
        ip_array = (ctypes.c_uint8 * 4)(8, 8, 8, 8)
        request.dst_addr.ipv4 = ip_array
        request.dst_port = 80
        
        # Mock удаленного сокета
        mock_remote = MagicMock()
        mock_socket.return_value = mock_remote
        
        proxy.handle_connect(mock_client, request)
        
        # Проверяем, что создан сокет и выполнено подключение
        mock_socket.assert_called_with(socket.AF_INET, socket.SOCK_STREAM)
        mock_remote.connect.assert_called_with(('8.8.8.8', 80))
        mock_client.send.assert_called_with(b'\x05\x00\x00\x01\x00\x00\x00\x00\x00\x00')
    
    @patch('socket.socket')
    def test_handle_connect_domain(self, mock_socket):
        """Тест обработки доменного подключения"""
        proxy = Socks5Proxy()
        
        mock_client = MagicMock()
        
        # Создаем реальный SOCKS5 запрос с доменом
        request = Socks5Request()
        request.cmd = 0x01  # CONNECT
        request.atyp = 0x03  # Domain
        request.dst_port = 443
        
        # Устанавливаем домен
        domain_name = b'example.com'
        request.dst_addr.domain.len = len(domain_name)
        # Создаем массив для доменного имени
        domain_array = (ctypes.c_uint8 * 255)(*domain_name.ljust(255, b'\0'))
        request.dst_addr.domain.name = domain_array
        
        mock_remote = MagicMock()
        mock_socket.return_value = mock_remote
        
        proxy.handle_connect(mock_client, request)
        
        mock_remote.connect.assert_called_with(('example.com', 443))
    
    def test_handle_connect_unsupported_atyp(self):
        """Тест неподдерживаемого типа адреса"""
        proxy = Socks5Proxy()
        
        mock_client = MagicMock()
        mock_request = MagicMock()
        mock_request.cmd = 0x01
        mock_request.atyp = 0x02  # Unsupported
        
        proxy.handle_connect(mock_client, mock_request)
        
        mock_client.send.assert_called_with(b'\x05\x08\x00\x01\x00\x00\x00\x00\x00\x00')
        mock_client.close.assert_called_once()
    
    @patch('socket.socket')
    def test_handle_connect_connection_error(self, mock_socket):
        """Тест ошибки подключения"""
        proxy = Socks5Proxy()
        
        mock_client = MagicMock()
        
        # Создаем реальный SOCKS5 запрос
        request = Socks5Request()
        request.cmd = 0x01
        request.atyp = 0x01
        ip_array = (ctypes.c_uint8 * 4)(192, 0, 2, 1)
        request.dst_addr.ipv4 = ip_array
        request.dst_port = 9999
        
        # Симулируем ошибку подключения
        mock_remote = MagicMock()
        mock_remote.connect.side_effect = Exception("Connection failed")
        mock_socket.return_value = mock_remote
        
        proxy.handle_connect(mock_client, request)
        
        mock_client.send.assert_called_with(b'\x05\x04\x00\x01\x00\x00\x00\x00\x00\x00')
        mock_client.close.assert_called_once()

class TestErrorHandling:
    """Тесты обработки ошибок"""
    
    def test_handle_client_invalid_handshake(self):
        """Тест невалидного handshake"""
        proxy = Socks5Proxy()
        mock_client = MagicMock()
        
        with patch('socks5_native.parse_handshake') as mock_parse:
            mock_parse.return_value = (False, None)
            mock_client.recv.return_value = b'invalid_data'
            
            proxy.handle_client(mock_client)
            
            mock_client.send.assert_called_with(b'\x05\xFF')  # No acceptable methods
            mock_client.close.assert_called_once()
    
    def test_handle_client_connection_reset(self):
        """Тест разрыва соединения"""
        proxy = Socks5Proxy()
        mock_client = MagicMock()
        mock_client.recv.side_effect = ConnectionResetError
        
        proxy.handle_client(mock_client)
        
        # Проверяем, что была попытка отправить ошибку
        mock_client.send.assert_called_once()
        mock_client.close.assert_called_once()