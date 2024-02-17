import socket
import mimetypes

def text_up():
    with open('index.html', 'rb') as file:
        text = file.read()
        file.close()
    return text

mimetypes.add_type('text/css', '.css')
def load_page_from_get_request(request_data):
    HDRS = 'HTTP/1.1 200 0K\r\nContent-Type: text/html; charset=utf-8\r\n\r\n'
    HDRS_404 = 'HTTP/1.1 404 0K\r\nContent-Type: text/html; charset=utf-8\r\n\r\n'
    path = request_data.split(' ')[1]

    try:
        if path.endswith('.css'):
            with open('web' + path, 'rb') as file:
                response = file.read()
                return 'HTTP/1.1 200 OK\r\nContent-Type: text/css; charset=utf-8\r\n\r\n'.encode('utf-8') + response
        elif path.endswith('.jpg'):
            with open('web' + path, 'rb') as file:
                response = file.read()
                return 'HTTP/1.1 200 OK\r\nContent-Type: text/jpg; charset=utf-8\r\n\r\n'.encode('utf-8') + response
        elif path.endswith('.png'):
            with open('web' + path, 'rb') as file:
                response = file.read()
                return 'HTTP/1.1 200 OK\r\nContent-Type: text/png; charset=utf-8\r\n\r\n'.encode('utf-8') + response
        else:
            with open('web' + path, 'rb') as file:
                response = file.read()
            return HDRS.encode('utf-8') + response
    except FileNotFoundError:
        return (HDRS_404 + 'Sorry, bro! No page...').encode()


def start_server():

    # Define socket host and port
    SERVER_HOST = '192.168.0.111'
    SERVER_PORT = 8480

    # Create socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    server_socket.bind((SERVER_HOST, SERVER_PORT))
    server_socket.listen(1)

    print(f'Listening http://{SERVER_HOST}:{SERVER_PORT}/index.html')

    text = ''
    while True:

        # Wait for client connections
        client_connection, client_address = server_socket.accept()

        # Get the client request
        request = client_connection.recv(1024).decode()
        print(request)
        connect = load_page_from_get_request(request)
        client_connection.send(connect)
        client_connection.shutdown(socket.SHUT_WR)

    # Close socket
    server_socket.close()

if __name__ == '__main__':
    start_server()