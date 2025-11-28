import socket
import threading
import select
from socks5_native import parse_handshake, parse_request, Socks5Handshake, Socks5Request

class Socks5Proxy:
    def __init__(self, host='localhost', port=1080):
        self.host = host
        self.port = port
    
    def start(self):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind((self.host, self.port))
        server_socket.listen(5)
        print(f"SOCKS5 proxy listening on {self.host}:{self.port}")
        
        while True:
            client_socket, addr = server_socket.accept()
            print(f"New connection from {addr}")
            threading.Thread(target=self.handle_client, args=(client_socket,)).start()
            
    def handle_client(self, client_socket):
        try:
            # Получаем handshake
            handshake_data = client_socket.recv(1024)
            if not handshake_data:
                client_socket.close()
                return
            
            success, handshake = parse_handshake(handshake_data)
        
            if not success:
                # Отправляем ошибку перед закрытием
                client_socket.send(b'\x05\xFF')  # No acceptable methods
                client_socket.close()
                return
        
            # Отправляем response (NO AUTHENTICATION)
            client_socket.send(b'\x05\x00')
        
            # Получаем request
            request_data = client_socket.recv(1024)
            if not request_data:
                client_socket.close()
                return
            
            success, request = parse_request(request_data)
        
            if not success:
                # Отправляем ошибку для невалидного запроса
                client_socket.send(b'\x05\x07\x00\x01\x00\x00\x00\x00\x00\x00')  # Command not supported
                client_socket.close()
                return
        
            # Обрабатываем CONNECT запрос
            if request.cmd == 0x01:  # CONNECT
                self.handle_connect(client_socket, request)
            else:
                # Unsupported command
                client_socket.send(b'\x05\x07\x00\x01\x00\x00\x00\x00\x00\x00')
                client_socket.close()
            
        except Exception as e:
            print(f"Error handling client: {e}")
            try:
                # Пытаемся отправить ошибку перед закрытием
                client_socket.send(b'\x05\x01\x00\x01\x00\x00\x00\x00\x00\x00')  # General failure
            except:
                pass
            finally:
                try:
                    client_socket.close()
                except:
                    pass
                
    def handle_connect(self, client_socket, request: Socks5Request):
        # Инициализируем переменные заранее
        host = None
        port = None
    
        try:
            if request.atyp == 0x01:  # IPv4
                host = '.'.join(str(b) for b in request.dst_addr.ipv4)
            elif request.atyp == 0x03:  # Domain
                domain_bytes = bytes(request.dst_addr.domain.name)[:request.dst_addr.domain.len]
                host = domain_bytes.decode('utf-8')
            elif request.atyp == 0x04:  # IPv6
                # Конвертируем IPv6 в строку
                host = ':'.join(f'{b:02x}' for b in request.dst_addr.ipv6)
            else:
                # Unsupported address type
                client_socket.send(b'\x05\x08\x00\x01\x00\x00\x00\x00\x00\x00')
                client_socket.close()
                return
        
            port = request.dst_port
        
            # Устанавливаем соединение с целевым сервером
            remote_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            remote_socket.settimeout(5)
            remote_socket.connect((host, port))
        
            # Отправляем успешный response
            client_socket.send(b'\x05\x00\x00\x01\x00\x00\x00\x00\x00\x00')
        
            # Начинаем туннелирование
            self.tunnel_data(client_socket, remote_socket)
        
        except socket.timeout:
            error_msg = f"Connection to {host}:{port} timed out" if host and port else "Connection timed out"
            print(error_msg)
            client_socket.send(b'\x05\x04\x00\x01\x00\x00\x00\x00\x00\x00')
            client_socket.close()
        except Exception as e:
            error_msg = f"Failed to connect to {host}:{port}: {e}" if host and port else f"Failed to connect: {e}"
            print(error_msg)
            client_socket.send(b'\x05\x04\x00\x01\x00\x00\x00\x00\x00\x00')
            client_socket.close()
    
    def tunnel_data(self, client_socket, remote_socket):
        """Туннелирование данных между клиентом и удаленным сервером"""
        sockets = [client_socket, remote_socket]
        
        while True:
            try:
                read_sockets, _, error_sockets = select.select(sockets, [], sockets, 1)
                
                if error_sockets:
                    break
                    
                for sock in read_sockets:
                    data = sock.recv(4096)
                    if not data:
                        break
                    
                    if sock is client_socket:
                        remote_socket.send(data)
                    else:
                        client_socket.send(data)
            except:
                break
        
        client_socket.close()
        remote_socket.close()
