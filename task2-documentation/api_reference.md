# API Documentation

## Native C Library API

### Структуры данных:

#### `socks5_handshake_t`
```c
// Структура для handshake-пакета SOCKS5
typedef struct {
    uint8_t version;      // Версия протокола (должна быть 0x05)
    uint8_t nmethods;     // Количество поддерживаемых методов
    uint8_t methods[255]; // Список методов аутентификации
} socks5_handshake_t;
```

#### `socks5_request_t`
```c
// Структура для запроса SOCKS5
typedef struct {
    uint8_t version;      // Версия протокола
    uint8_t cmd;          // Команда (CONNECT = 0x01, BIND = 0x02, UDP = 0x03)
    uint8_t rsv;          // Зарезервировано (должно быть 0x00)
    uint8_t atyp;         // Тип адреса (IPv4=0x01, DOMAIN=0x03, IPv6=0x04)
    union {
        struct { uint8_t addr[4]; } ipv4;     // IPv4 адрес
        struct { uint8_t addr[16]; } ipv6;    // IPv6 адрес  
        socks5_domain_t domain;               // Доменное имя
    } dst_addr;           // Целевой адрес
    uint16_t dst_port;    // Целевой порт
} socks5_request_t;
```
### Функции C библиотеки:

#### `parse_socks5_handshake`
```c
int parse_socks5_handshake(const uint8_t* data, size_t len, socks5_handshake_t* handshake);
```

#### Параметры:

- `data`: Входные байты SOCKS5 handshake
- `len`: Длина данных
- `handshake`: Выходная структура для разобранных данных

#### Возвращает:

- `0`: Успешный парсинг
- `-1`: Неверные параметры (нулевые указатели или недостаточная длина)
- `-2`: Неверная версия протокола SOCKS (не 0x05)
- `-3`: Неверное количество методов
- `-4`: Недостаточно данных

#### `parse_socks5_request`
```c
int parse_socks5_request(const uint8_t* data, size_t len, socks5_request_t* request);
```

#### Параметры:

- `data`: Входные байты SOCKS5 запроса
- `len`: Длина данных
- `request`: Выходная структура для разобранных данных

#### Возвращает:

- `0`: Успешный парсинг
- `-1`: Неверные параметры (нулевые указатели или недостаточная длина)
- `-2`: Недостаточно данных для IPv4
- `-3/-4`: Недостаточная/неверная длина доменного имени
- `-5`: Недостаточная длина данных домена
- `-6`: Недостаточно данных для IPv6
- `-7`: Неподдерживаемый тип адреса
- `-8`: Недостаточная длина для порта


## Python API

### Класс `Socks5Proxy`

#### Конструктор

```python
Socks5Proxy(host='localhost', port=1080)
```

#### Параметры:

- `host`: Хост для привязки ('localhost', '0.0.0.0', etc.)
- `port`: Порт для прослушивания, например 1080

Пример использования:

```proxy = Socks5Proxy(host='0.0.0.0', port=1080)```

### Методы:

#### **`start()`**

Запускает прокси-сервер в бесконечном цикле прослушивания.

Пример использования:

```proxy.start()```

#### **`handle_client(client_socket)`**

Обрабатывает подключение клиента.

- `client_socket`: Socket объект клиента

Вызывается автоматически для каждого нового подключения.

#### **`handle_connect(client_socket, request)`**

Обрабатывает CONNECT запрос.

- `client_socket`: Socket объект клиента
- `request`: Разобранный SOCKS5 запрос

#### **`tunnel_data(client_socket, remote_socket)`**

- `client_socket`: socket.socket - сокет клиентского соединения
- `remote_socket`: socket.socket - сокет соединения с целевым сервером

Туннелирует данные между клиентом и целевым сервером.

```python
# Внутри handle_connect после установки соединения
self.tunnel_data(client_socket, remote_socket)
```

### Модуль socks5_native

#### **`parse_handshake(data: bytes) -> Tuple[bool, Optional[Socks5Handshake]]`**

Входные параметры:

- `data:` bytes - байтовая строка с данными handshake

Возвращаемое значение:

- `Tuple[bool, Optional[Socks5Handshake]]` - кортеж из:
- `bool` - успешность парсинга (True/False)
- `Socks5Handshake` - объект с разобранными данными или None при ошибке

Парсит SOCKS5 handshake используя C библиотеку.

Пример использования:

```python
data = b'\x05\x01\x00'
success, handshake = parse_handshake(data)
if success:
    print(f"Version: {handshake.version}")
```

#### **`parse_request(data: bytes) -> Tuple[bool, Optional[Socks5Request]]`**

Входные параметры:

- `data`: bytes - байтовая строка с данными запроса

Возвращаемое значение:

- `Tuple[bool, Optional[Socks5Request]]` - кортеж из:

- `bool` - успешность парсинга (True/False)
- `Socks5Request` - объект с разобранными данными или None при ошибке

Парсит SOCKS5 запрос используя C библиотеку.

Пример использования:

```python
success, request = parse_request(request_data)
if success and request.cmd == 0x01:  # CONNECT
    handle_connect(request)
```

### Поддерживамые константы SOCKS5

#### Команды (cmd)

- `0x01`: CONNECT

#### Типы адресов (atyp)

- `0x01`: IPv4
- `0x03`: Доменное имя
- `0x04`: IPv6

#### Методы аутентификации

- `0x00`: NO AUTHENTICATION REQUIRED