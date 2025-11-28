# SOCKS5 Proxy Server

Простой код базового SOCKS5 прокси-сервера, сгенерированный AI DeepSeek, с гибридной архитектурой на Python и C.

## Архитектура

- **C библиотека**: Нативный парсинг SOCKS5 протокола, валидация пакетов
- **Python модуль**: Высокоуровневая логика, управление соединениями, туннелирование
- **Многопоточность**: Обработка множественных одновременных подключений

## Требования

- Python 3.8+
- GCC/Clang для компиляции C библиотеки
- Linux/Unix система

## Установка

### 1. Клонирование репозитория

```bash
git clone <repository-url>
cd test-task
```

### 2. Компиляция C библиотеки

#### Компиляция shared library #

```bash
gcc -c -fPIC socks5_parser.c -o socks5_parser.o
gcc -shared -Wl,-soname,libsocks5_parser.so -o libsocks5_parser.so socks5_parser.o
```

#### Или используйте Makefile #

```bash
make
```

### 3. Установка Python зависимостей

```bash
sudo apt install python3-pytest
```

### 4. Проверка установки

```bash
python -c "from socks5_native import parse_handshake; print('✅ Native library loaded successfully')"
```

## Запуск

#### Базовый запуск #

```bash
python3 main.py
```

#### С кастомными параметрами #

```bash
python3 -c "
from socks5_proxy import Socks5Proxy
proxy = Socks5Proxy(host='0.0.0.0', port=1080)
proxy.start()
"
```

#### Запуск в фоне #

```bash
nohup python3 main.py > proxy.log 2>&1 &
```

## Конфигурация

#### Измените параметры в socks5_proxy.py: #

```python
class Socks5Proxy:
    def __init__(self, host='localhost', port=1080):
        self.host = host
        self.port = port
```

## Тестирование

#### Запуск всех тестов #

```bash
python3 run_tests.py
```

#### Или отдельные группы тестов #

```bash
pytest tests/unit/ -v
pytest tests/integration/ -v
pytest tests/performance/ -v
```

## Docker (опционально)

```docker
FROM python:3.9-slim
COPY . /app
WORKDIR /app
RUN make && pip install pytest
EXPOSE 1080
CMD ["python", "main.py"]
```