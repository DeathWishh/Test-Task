import pytest
import socket
import threading
import time
import sys
import os

# Добавляем путь к src/python для импортов
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src', 'python'))

from socks5_native import parse_handshake, parse_request, Socks5Handshake, Socks5Request
from socks5_proxy import Socks5Proxy

class TestSocks5ProxyIntegration:
    """Интеграционные тесты SOCKS5 прокси"""
    
    @pytest.fixture
    def proxy_server(self):
        """Запуск тестового прокси-сервера на свободном порту"""
        # Находим свободный порт
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind(('127.0.0.1', 0))
            free_port = s.getsockname()[1]
        
        proxy = Socks5Proxy('127.0.0.1', free_port)
        server_thread = threading.Thread(target=proxy.start)
        server_thread.daemon = True
        server_thread.start()
        
        # Даем серверу время на запуск
        time.sleep(0.5)
        
        yield '127.0.0.1', free_port
        
        # Cleanup будет автоматически из-за daemon thread
    
    def test_socks5_handshake_integration(self, proxy_server):
        """Интеграционный тест SOCKS5 handshake"""
        host, port = proxy_server
        
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((host, port))
        
        try:
            # Отправляем handshake
            handshake = b'\x05\x01\x00'  # VER=5, NMETHODS=1, METHOD=0
            sock.send(handshake)
            
            # Получаем ответ
            response = sock.recv(2)
            assert response == b'\x05\x00'  # VER=5, METHOD=0 (no auth)
            
        finally:
            sock.close()
    
    def test_socks5_connect_request_integration(self, proxy_server):
        """Интеграционный тест CONNECT запроса"""
        host, port = proxy_server
        
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((host, port))
        
        try:
            # Handshake
            sock.send(b'\x05\x01\x00')
            response = sock.recv(2)
            assert response == b'\x05\x00'
            
            # CONNECT запрос к example.com:80
            request = b'\x05\x01\x00\x03\x0bexample.com\x00\x50'
            sock.send(request)
            
            # Получаем ответ
            response = sock.recv(10)
            # Прокси должен ответить, даже если не может подключиться
            assert len(response) == 10
            assert response[0] == 5  # SOCKS5 version
            
        finally:
            sock.close()
    
    def test_multiple_concurrent_connections(self, proxy_server):
        """Тест множественных одновременных подключений"""
        host, port = proxy_server
        
        def test_connection(conn_id):
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(5)
                sock.connect((host, port))
                
                # Быстрый handshake
                sock.send(b'\x05\x01\x00')
                response = sock.recv(2)
                assert response == b'\x05\x00'
                
                sock.close()
                return True
            except Exception as e:
                print(f"Connection {conn_id} failed: {e}")
                return False
        
        # Запускаем несколько подключений
        threads = []
        results = []
        
        for i in range(3):  # Уменьшим количество для стабильности
            thread = threading.Thread(target=lambda i=i: results.append(test_connection(i)))
            threads.append(thread)
            thread.start()
        
        for thread in threads:
            thread.join()
        
        # Проверяем, что все подключения успешны
        assert all(results), "Not all connections were successful"
    
    def test_proxy_actual_connection(self, proxy_server):
        """Тест реального подключения через прокси (если есть интернет)"""
        host, port = proxy_server
        
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((host, port))
        
        try:
            # Handshake
            sock.send(b'\x05\x01\x00')
            response = sock.recv(2)
            assert response == b'\x05\x00'
            
            # CONNECT запрос к google.com:80 (как пример)
            request = b'\x05\x01\x00\x03\x0agoogle.com\x00\x50'
            sock.send(request)
            
            # Получаем ответ от прокси
            response = sock.recv(10)
            assert response[0] == 5  # SOCKS5 version
            
            # Код ответа может быть разным в зависимости от возможности подключения
            response_code = response[1]
            print(f"Proxy response code: {response_code}")
            
        finally:
            sock.close()