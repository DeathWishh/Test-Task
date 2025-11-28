# Troubleshooting

## Распространенные проблемы и решения

### 🔴 Проблема: Не компилируется C библиотека

**Симптомы:**

```bash
ImportError: libsocks5_parser.so: cannot open shared object file`
```

**Решения:**

1. Проверка компилятора:

```bash
gcc --version
```
   
#### Если не установлен:

```bash
sudo apt-get install gcc  # Ubuntu/Debian
brew install gcc          # macOS
```
   
2. Ручная компиляция:

```bash
gcc -c -fPIC socks5_parser.c -o socks5_parser.o
gcc -shared -Wl,-soname,libsocks5_parser.so -o libsocks5_parser.so socks5_parser.o
```

3. Проверка библиотеки:

```bash
ldd libsocks5_parser.so
file libsocks5_parser.so
```

### 🔴 Проблема: Порт уже занят

**Симптомы:**

```bash
OSError: [Errno 98] Address already in use
```

**Решения:**

1. Использование другого порта:

```bash
proxy = Socks5Proxy(port=1081)
```

2. Освобождение порта:

```bash
sudo lsof -i :1080`
sudo kill -9 <PID>`
```

3. Ожидание освобождения порта:

```bash
# Ожидание 60 секунд
for i in {1..60}; do
    nc -z localhost 1080 || break
    sleep 1
done
```

### 🔴 Проблема: Клиенты не могут подключиться

**Симптомы:**

- Connection refused
- Timeout при подключении

**Решения:**

1. Проверка firewall:

```bash
sudo ufw status  # Ubuntu
sudo iptables -L # Другие дистрибутивы
```

2. Запуск на правильном интерфейсе:

```python
# Для доступа извне
proxy = Socks5Proxy(host='0.0.0.0', port=1080)
```

3. Проверка сетевой доступности:

```bash
telnet localhost 1080
netstat -tulpn | grep 1080
```

### 🔴 Проблема: Высокая загрузка CPU

**Симптомы:**

- Медленная работа
- High CPU usage

**Решения:**

1. Ограничение подключений:

```python
import socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.listen(50)  # Ограничение очереди
```

2. Оптимизация туннелирования:

```python
# Увеличение размера буфера
data = sock.recv(8192)  # Вместо 4096
```

3. Мониторинг производительности:

```bash
top -p $(pgrep -f "python.*main.py")
```

### 🔴 Проблема: Утечки памяти

**Симптомы:**

- Память постоянно растет
- Сервер падает через некоторое время

**Решения:**

1. Проверка закрытия сокетов:

```python
try:
    # работа с сокетом
finally:
    sock.close()
```

2. Использование менеджеров контекста:

```python
with socket.socket() as sock:
    # автоматическое закрытие
```

3. Мониторинг памяти:

```bash
ps aux --sort=-%mem | head -10
```

### 🔴 Проблема: Неправильный парсинг пакетов

**Симптомы:**

- parse_handshake возвращает ошибки
- Клиенты получают некорректные ответы

**Решения:**

1. Валидация входных данных:

```python
if len(data) < 3:
    return False, None
```

2. Логирование пакетов:

```python
print(f"Raw data: {data.hex()}")
success, result = parse_handshake(data)
print(f"Parse result: {success}")
```

3. Тестирование с эталонными пакетами:

```python
# Стандартный SOCKS5 handshake
test_handshake = b'\x05\x01\x00'
success, handshake = parse_handshake(test_handshake)
assert success == True
```

### 🔴 Проблема: IPv6 не работает

**Симптомы:**

- IPv6 подключения отклоняются
- Ошибка "Unsupported address type"

**Решения:**

1. Проверка поддержки IPv6:

```python
import socket
print(socket.has_ipv6)  # Должно быть True
```

2. Обработка IPv6 в коде:

```python
if request.atyp == 0x04:  # IPv6
    # Конвертация IPv6 байтов в строку
    ipv6_str = socket.inet_ntop(socket.AF_INET6, bytes(request.dst_addr.ipv6.addr))
```


### 🔴 Проблема: SSL/TLS через прокси

**Симптомы:**

- HTTPS сайты не работают
- SSL handshake failures

**Решения:**

1. Использование правильного клиента:

```bash
# curl с поддержкой SOCKS5
curl --socks5-hostname localhost:1080 https://example.com
```

2. Проверка DNS разрешения:

```python
# Убедитесь, что доменные имена правильно резолвятся
import socket
print(socket.gethostbyname('example.com'))
```

## Диагностические команды

### Проверка состояния прокси

```bash
# Проверка запущенных процессов
ps aux | grep socks5

# Проверка открытых портов
netstat -tulpn | grep 1080
ss -tulpn | grep 1080

# Проверка подключений
lsof -i :1080
```

### Мониторинг трафика

```bash
# TCP dump для отладки
sudo tcpdump -i any -n port 1080

# Мониторинг в реальном времени
watch "netstat -an | grep 1080"
```

### Тестирование функциональности

```bash
# Быстрый тест подключения
timeout 5 nc -z localhost 1080 && echo "OK" || echo "FAIL"

# Тестирование SOCKS5 handshake
echo -ne '\x05\x01\x00' | nc localhost 1080 | hexdump -C
```

## Логи и отладка

### Включение детального логирования

```bash
import logging
logging.basicConfig(level=logging.DEBUG)

class DebugProxy(Socks5Proxy):
    def handle_client(self, client_socket):
        logging.debug(f"New client: {client_socket.getpeername()}")
        super().handle_client(client_socket)
```

### Анализ дампа пакетов

```bash
def debug_packet(data, description):
    print(f"{description}: {data.hex()}")
    
# Использование в коде
debug_packet(handshake_data, "Received handshake")
```

## Производительность и оптимизация

### Настройка для высоких нагрузок

```bash
import socket

class HighPerformanceProxy(Socks5Proxy):
    def start(self):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, 8192)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, 8192)
        server_socket.bind((self.host, self.port))
        server_socket.listen(128)  # Большая очередь
        # ...
```

### Мониторинг ресурсов

```bash
# Мониторинг в реальном времени
watch -n 1 "echo 'Connections:' && netstat -an | grep 1080 | wc -l && echo 'Memory:' && ps -o pid,ppid,cmd,%mem,%cpu --sort=-%mem | grep python"
```

Если проблема не решена, создайте issue с:

1. Версией Python: ```python --version```
2. Операционной системой: ```uname -a```
3. Логами ошибок
4. Шагами для воспроизведения