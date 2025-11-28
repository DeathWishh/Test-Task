import pytest
import time
import threading
import sys
import os

# Добавляем путь к src/python для импортов
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src', 'python'))

from socks5_native import parse_handshake, parse_request, Socks5Handshake, Socks5Request
from socks5_proxy import Socks5Proxy

class TestPerformance:
    """Performance тесты"""
    
    def test_handshake_parsing_performance(self):
        """Тест производительности парсинга handshake"""
        test_data = b'\x05\x01\x00'
        
        start_time = time.time()
        iterations = 10000
        
        for _ in range(iterations):
            success, handshake = parse_handshake(test_data)
            assert success == True
        
        end_time = time.time()
        total_time = end_time - start_time
        
        # Проверяем, что парсинг достаточно быстрый
        # Менее 1 микросекунды на операцию в среднем
        time_per_operation = total_time / iterations
        assert time_per_operation < 0.001  # 1ms per operation
    
    def test_request_parsing_performance(self):
        """Тест производительности парсинга запросов"""
        # IPv4 запрос
        ipv4_data = b'\x05\x01\x00\x01\x7f\x00\x00\x01\x04\x38'
        # Domain запрос
        domain_data = b'\x05\x01\x00\x03\x0bexample.com\x00\x50'
        
        start_time = time.time()
        iterations = 10000
        
        for i in range(iterations):
            # Чередуем типы запросов
            data = ipv4_data if i % 2 == 0 else domain_data
            success, request = parse_request(data)
            assert success == True
        
        end_time = time.time()
        total_time = end_time - start_time
        
        time_per_operation = total_time / iterations
        assert time_per_operation < 0.001  # 1ms per operation
    
    def test_concurrent_parsing_performance(self):
        """Тест производительности при конкурентном парсинге"""
        test_data = b'\x05\x01\x00\x01\x7f\x00\x00\x01\x04\x38'
        results = []
        
        def parse_worker(worker_id, data, iterations):
            for _ in range(iterations):
                success, request = parse_request(data)
                results.append(success)
        
        start_time = time.time()
        
        threads = []
        for i in range(4):  # 4 потока
            thread = threading.Thread(
                target=parse_worker, 
                args=(i, test_data, 2500)  # 2500 итераций на поток
            )
            threads.append(thread)
            thread.start()
        
        for thread in threads:
            thread.join()
        
        end_time = time.time()
        total_time = end_time - start_time
        
        # Проверяем, что многопоточность не значительно замедляет работу
        assert total_time < 2.0  # Общее время менее 2 секунд
        assert all(results)  # Все операции успешны
