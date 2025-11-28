# Примеры использования

## Базовое использование

### Запуск прокси-сервера

```python
from socks5_proxy import Socks5Proxy

# Запуск на всех интерфейсах
proxy = Socks5Proxy(host='0.0.0.0', port=1080)
proxy.start()

# Или с кастомными настройками
proxy = Socks5Proxy(host='192.168.1.100', port=8080)
proxy.start()
```

## Использование в других приложениях

### Интеграция в существующий код

```python
from socks5_proxy import Socks5Proxy
import threading
import time
import socket

class MyApplication:
    def __init__(self, proxy_port=1080):
        self.proxy = Socks5Proxy(port=proxy_port)
        self.proxy_thread = None
    
    def start_proxy(self):
        def run_proxy():
            try:
                self.proxy.start()
            except Exception as e:
                print(f"Proxy error: {e}")
        
        self.proxy_thread = threading.Thread(target=run_proxy)
        self.proxy_thread.daemon = True
        self.proxy_thread.start()
        
        # Ждем немного чтобы убедиться что прокси запустился
        time.sleep(0.5)
        
        # Проверяем что порт слушается
        if self.is_proxy_running():
            print("SOCKS5 proxy started in background")
        else:
            print("Failed to start SOCKS5 proxy")
    
    def is_proxy_running(self):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)
            result = sock.connect_ex(('localhost', self.proxy.port))
            sock.close()
            return result == 0
        except:
            return False
    
    def main(self):
        self.start_proxy()
        
        # Ваша основная логика приложения
        try:
            while True:
                time.sleep(1)
                # Основная работа приложения
        except KeyboardInterrupt:
            print("Application stopped")

if __name__ == "__main__":
    app = MyApplication(proxy_port=1080)
    app.main()
```

### Использование только парсера

```python
from socks5_native import parse_handshake, parse_request

# Анализ SOCKS5 пакетов
packet_data = b'\x05\x01\x00\x01\x7f\x00\x00\x01\x04\x38'
success, request = parse_request(packet_data)

if success:
    print(f"Command: {request.cmd}")
    print(f"Address type: {request.atyp}")
    print(f"Port: {request.dst_port}")
```

## Клиентские примеры

### Использование с curl

```bash
# Тестирование через прокси
curl --socks5-hostname localhost:1080 https://httpbin.org/ip

# Или с явным указанием
curl -x socks5://localhost:1080 https://httpbin.org/ip
```

### Использование в браузере

1. Откройте настройки сети браузера
2. Настройте ручную прокси конфигурацию:
- SOCKS Host: localhost
- Port: 1080
- Тип: SOCKS v5

## Продвинутые сценарии

### Мониторинг активности

```python
from socks5_proxy import Socks5Proxy
import time

class MonitoringProxy(Socks5Proxy):
    def handle_connect(self, client_socket, request):
        # Правильное форматирование адреса
        if request.atyp == 0x01:  # IPv4
            host = '.'.join(str(b) for b in request.dst_addr.ipv4)
        elif request.atyp == 0x03:  # Domain
            domain_bytes = bytes(request.dst_addr.domain.name)[:request.dst_addr.domain.len]
            host = domain_bytes.decode('utf-8')
        else:  # IPv6
            host = ':'.join(f'{b:02x}' for b in request.dst_addr.ipv6)
            
        print(f"New connection: {host}:{request.dst_port}")
        start_time = time.time()
        
        try:
            # Вызываем родительский метод
            super().handle_connect(client_socket, request)
        finally:
            duration = time.time() - start_time
            print(f"Connection closed after {duration:.2f} seconds")

proxy = MonitoringProxy()
proxy.start()
```

### Фильтрация запросов

```python
from socks5_proxy import Socks5Proxy

class FilteringProxy(Socks5Proxy):
    def handle_connect(self, client_socket, request):
        # Блокировка определенных портов
        if request.dst_port in [25, 110, 143]:  # Example ports
            client_socket.send(b'\x05\x02\x00\x01\x00\x00\x00\x00\x00\x00')  # Connection not allowed
            client_socket.close()
            return
        
        super().handle_connect(client_socket, request)
```

### Логирование в файл

```python
import logging

logging.basicConfig(
    filename='proxy.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class LoggingProxy(Socks5Proxy):
    def handle_client(self, client_socket):
        try:
            super().handle_client(client_socket)
            logging.info("Client handled successfully")
        except Exception as e:
            logging.error(f"Error handling client: {e}")
```

### Тестирование парсинга

```python
from socks5_native import parse_handshake, parse_request

# Тестирование handshake
handshake_data = b'\x05\x01\x00'
success, handshake = parse_handshake(handshake_data)
print(f"Handshake: success={success}, version={handshake.version if success else 'N/A'}")

# Тестирование запроса
request_data = b'\x05\x01\x00\x01\x7F\x00\x00\x01\x1F\x40'  # 127.0.0.1:8000
success, request = parse_request(request_data)
if success:
    print(f"Request: cmd={request.cmd}, atyp={request.atyp}, port={request.dst_port}")
```

### Интеграционное тестирование

```python
import socket
from socks5_proxy import Socks5Proxy
import threading
import time

def test_proxy():
    # Запуск прокси в отдельном потоке
    proxy = Socks5Proxy(host='localhost', port=1081)
    thread = threading.Thread(target=proxy.start)
    thread.daemon = True
    thread.start()
    time.sleep(1)  # Даем время на запуск
    
    # Тестирование подключения
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(('localhost', 1081))
    
    # Отправка handshake
    sock.send(b'\x05\x01\x00')
    response = sock.recv(2)
    print(f"Handshake response: {response.hex()}")
    
    sock.close()

test_proxy()
```

### Бенчмаркинг

```python
# Бенчмарк обработки запросов
import time
from socks5_native import parse_request

def benchmark_parsing():
    # Корректный SOCKS5 запрос (CONNECT 127.0.0.1:1080)
    test_data = b'\x05\x01\x00\x01\x7f\x00\x00\x01\x04\x38'
    
    # Предварительный вызов для "прогрева"
    success, request = parse_request(test_data)
    if not success:
        print("ERROR: Test data is invalid!")
        return
    
    start = time.time()
    success_count = 0
    
    for i in range(10000):
        success, request = parse_request(test_data)
        if success:
            success_count += 1
    
    duration = time.time() - start
    
    print(f"10,000 requests parsed in {duration:.3f} seconds")
    print(f"Average: {duration/10000*1000:.3f} ms per request")
    print(f"Success rate: {success_count}/10000 ({success_count/100:.1f}%)")

# Для устранения отладочного вывода временно модифицируйте socks5_native.py:
# Закомментируйте или удалите блок print в функции parse_request
```