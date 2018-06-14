import socket
import time

if __name__ == "__main__":
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(('localhost', 10000))
    sock.listen(1)
    print('Łączę z agentem...\n')
    connection, client_address = sock.accept()
    try:
        print('Połączenie z agentem {}\n'.format(client_address))
        print('Wprowadz adresy URL ofert, ktore Ci sie podobaja (oddziel oferty przyciskiem [ENTER],\n' +
              'aby zakonczyc wcisnij "q" i zatwierdz klawiszem [ENTER]):\n')
        while True:
            data = input()
            if data == 'q':
                connection.sendall('END_OF_URLS'.encode())
                print('Oczekiwanie na wyniki...\n')
                break
            print('Wysyłam adres URL do agenta\n')
            connection.sendall(data.encode())

        data = ''
        while True:
            data = connection.recv(256)
            data = data.decode()
            if data == 'END_OF_RESULTS':
                print("To wszystkie wyniki\n")
                break
            print(data)

    finally:
        print('Zamykanie połączenia\n')
        time.sleep(2)
        connection.close()
