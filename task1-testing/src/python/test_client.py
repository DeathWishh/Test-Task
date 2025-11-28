import socket
import time
from socks5_native import parse_request, Socks5Request

def test_socks5_proxy_debug():
    # Подключаемся к прокси
    proxy_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    proxy_socket.connect(('localhost', 1080))
    
    print("Connected to proxy")
    
    # Отправляем handshake
    handshake = b'\x05\x01\x00'  # VER=5, NMETHODS=1, METHOD=0
    proxy_socket.send(handshake)
    
    # Получаем ответ
    response = proxy_socket.recv(2)
    print(f"Handshake response: {response.hex()}")
    
    if response == b'\x05\x00':
        print("Handshake successful!")
        
        # Отправляем CONNECT запрос к httpbin.org:80
        host = b'httpbin.org'
        request_data = b'\x05\x01\x00\x03' + bytes([len(host)]) + host + b'\x00\x50'
        print(f"Sending request: {request_data.hex()}")
        
        # Декодируем и проверим запрос локально
        success, parsed_request = parse_request(request_data)
        if success:
            print(f"Request parsed successfully: cmd={parsed_request.cmd}, atyp={parsed_request.atyp}")
        else:
            print("Failed to parse request locally!")
        
        proxy_socket.send(request_data)
        
        # Получаем ответ
        response = proxy_socket.recv(10)
        print(f"Connect response: {response.hex()}")
        
        response_code = response[1] if len(response) > 1 else -1
        print(f"Response code: {response_code}")
        
        if response_code == 0x00:  # Success
            print("Connection established!")
            
            # Отправляем простой HTTP запрос
            http_request = b"GET /ip HTTP/1.1\r\nHost: httpbin.org\r\n\r\n"
            proxy_socket.send(http_request)
            
            # Получаем ответ
            time.sleep(1)
            response = proxy_socket.recv(4096)
            print("HTTP response:")
            print(response.decode())
        else:
            error_codes = {
                0x01: 'General failure',
                0x02: 'Connection not allowed',
                0x03: 'Network unreachable', 
                0x04: 'Host unreachable',
                0x05: 'Connection refused',
                0x06: 'TTL expired',
                0x07: 'Command not supported',
                0x08: 'Address type not supported'
            }
            error_msg = error_codes.get(response_code, f'Unknown error {response_code}')
            print(f"Connection failed: {error_msg}")
    else:
        print("Handshake failed")
    
    proxy_socket.close()

if __name__ == "__main__":
    test_socks5_proxy_debug()