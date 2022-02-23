from http import server
from socket import *
from trade_server import order_book, order, trade
from collections import defaultdict

def createServer():
    serversocket = socket(AF_INET, SOCK_STREAM)
    try:
        serversocket.bind(('localhost', 9000))
        serversocket.listen(5)
        while True:
            (clientsocket, address) = serversocket.accept()

            rd = clientsocket.recv(5000).decode()
            pieces = rd.split('\n')
            if len(pieces) > 0:
                print(pieces[0])
            
            data = 'HTTP/1.1 200 OK\r\n'
            data += 'Content-Type: text/html; charset=utf-8\r\n'
            data += '<html><body>Hello World!</body></html>\r\n\r\n'
            clientsocket.sendall(data.encode())
            clientsocket.shutdown(SHUT_WR)

    except KeyboardInterrupt:
        print('Shutting down...')
    except Exception as exc:
        print('Error:\n')
        print(exc)

print('Access http://localhost:9000')
# createServer()

catalog = defaultdict(order_book.OrderBookFIFO)
catalog['BTC'].process(order.Order(300, 10, 1, 'S'))
catalog['BTC'].process(order.Order(300, 10, 2, 'S'))
catalog['BTC'].process(order.Order(200, 15, 3, 'S'))
catalog['BTC'].process(order.Order(200, 20, 4, 'S'))
catalog['BTC'].process(order.Order(300, 10, 5, 'S'))
catalog['BTC'].process(order.Order(300, 10, 6, 'S'))
catalog['BTC'].process(order.Order(300, 10, 7, 'S'))
catalog['BTC'].process(order.Order(300, 10, 8, 'S'))

print('Original sell orders')
for od in catalog['BTC'].sell_orders:
    print(od)

print('The respective mapping')
for oid in catalog['BTC'].id_mapping.keys():
    print(oid)


catalog['BTC'].process(order.Order(500, 5, 1, 'B'))
print('Sell orders after buying 1')
for od in catalog['BTC'].sell_orders:
    print(od)

print('The respective mapping')
for oid in catalog['BTC'].id_mapping.keys():
    print(oid)

catalog['BTC'].process(order.Order(700, 0, 2, 'B'))

print('Sell orders after buying 2')
for od in catalog['BTC'].sell_orders:
    print(od)

print('The respective mapping')
for oid in catalog['BTC'].id_mapping.keys():
    print(oid)

# print('Buy orders after buying 2')
# for od in catalog['BTC'].buy_orders:
#     print(od)

catalog['BTC'].cancel_order(5)
catalog['BTC'].cancel_order(8)
catalog['BTC'].cancel_order(3)

for od in catalog['BTC'].sell_orders:
    print(od)

for oid in catalog['BTC'].id_mapping.keys():
    print(oid)

# catalog2 = defaultdict(order_book.OrderBookPR)
# catalog['ETH'].process(order.Order(300, 10, 1, 1))
# catalog['ETH'].process(order.Order(300, 10, 2, 1))
# catalog['ETH'].process(order.Order(200, 15, 3, 1))
# catalog['ETH'].process(order.Order(200, 20, 4, 1))
# catalog['ETH'].process(order.Order(300, 10, 3, 1))
# catalog['ETH'].process(order.Order(300, 10, 4, 1))
# catalog['ETH'].process(order.Order(300, 10, 5, 1))
# catalog['ETH'].process(order.Order(300, 10, 6, 1))


