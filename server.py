import socket
import mimetypes

def start():
    file_path = 'config.txt'

    data = {}

    with open(file_path, 'r') as file:
        for line in file:
            key, value = line.strip().split('=')
            data[key] = value
        file.close()

    if bool(data.get('mimetypes')):
        mimetypes.add_type('text/css', '.css')

    start_server(data)

def load_page_from_get_request(request_data, data = {}):
    HDRS = 'HTTP/1.1 200 0K\r\nContent-Type: text/html; charset=utf-8\r\n\r\n'
    HDRS_404 = 'HTTP/1.1 404 0K\r\nContent-Type: text/html; charset=utf-8\r\n\r\n'

    try:
        path = request_data.split(' ')[1]
    except IndexError:
        print("IndexError")

    try:
        if path.endswith('.css'):
            with open(data.get('folder') + path, data.get('openf')) as file:
                response = file.read()
                return 'HTTP/1.1 200 OK\r\nContent-Type: text/css; charset=utf-8\r\n\r\n'.encode(data.get('encoding')) + response
        elif path.endswith('.jpg'):
            with open(data.get('folder') + path, data.get('openf')) as file:
                response = file.read()
                return 'HTTP/1.1 200 OK\r\nContent-Type: text/jpg; charset=utf-8\r\n\r\n'.encode(data.get('encoding')) + response
        elif path.endswith('.js'):
            with open(data.get('folder') + path, data.get('openf')) as file:
                response = file.read()
                return 'HTTP/1.1 200 OK\r\nContent-Type: text/jpg; charset=utf-8\r\n\r\n'.encode(data.get('encoding')) + response
        elif path.endswith('.png'):
            with open(data.get('folder') + path, data.get('openf')) as file:
                response = file.read()
                return 'HTTP/1.1 200 OK\r\nContent-Type: text/png; charset=utf-8\r\n\r\n'.encode(data.get('encoding')) + response
        else:
            with open(data.get('folder') + path, data.get('openf')) as file:
                response = file.read()
            return HDRS.encode(data.get('encoding')) + response
    except FileNotFoundError:
        with open(data.get('404_folder'), data.get('openf')) as file:
            response = file.read()
            file.close()
        return HDRS_404.encode(data.get('encoding')) + response
        
def start_server(data = {}):
    SERVER_HOST = data.get('host')
    SERVER_PORT = int(data.get('port'))

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    server_socket.bind((SERVER_HOST, SERVER_PORT))
    server_socket.listen(int(data.get('listen')))

    print(f'Listening http://{SERVER_HOST}:{SERVER_PORT}/index.html')

    while True:
        client_connection, client_address = server_socket.accept()
        request = client_connection.recv(1024).decode()
        print(request)
        connect = load_page_from_get_request(request, data)
        client_connection.send(connect)
        client_connection.shutdown(socket.SHUT_WR)

    server_socket.close()

if __name__ == '__main__':
    start()