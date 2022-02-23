# Enter your code here. Read input from STDIN. Print output to STDOUT
class Order:
    def __init__(self, amount, price, id, side, type, display_size=None):
        self.amount = amount
        self.price = price
        self.id = id
        self.side = side
        self.type = type
        self.display_size = display_size

    def __str__(self):
        if self.type == 'ICE' and self.display_size:
            return '{}({})@{}#{}'.format(self.display_size, self.amount, self.price, self.id)
        return '{}@{}#{}'.format(self.amount, self.price, self.id)

class Trade:
    def __init__(self, buy_id, sell_id, amount, price):
        self.buy_id = buy_id
        self.sell_id = sell_id
        self.amount = amount
        self.price = price

class OrderBook:
    def __init__(self):
        self.buy_orders = []
        self.sell_orders = []
        self.id_mapping = {}

    def process(self, order):
        if order.side == 'B':
            if order.type == 'MO':
                order.price = float('inf')
            self.process_buy(order)
        elif order.side == 'S':
            if order.type == 'MO':
                order.price = 0
            self.process_sell(order)
    
    def process_buy(self, order):
        trades, to_remove = [], []
        index = n = len(self.sell_orders)
        # Market order price == 0
        # Limit order price > 0
        if order.price == 0:
            index = 0
        elif n != 0 and self.sell_orders[0].price <= order.price:
            index = self.find_sell_order_match(order.price)
        
        while index < len(self.sell_orders):
            sell_order = self.sell_orders[index]
            if sell_order.price > order.price:
                break
            if sell_order.type != 'ICE':
                min_amount = min(sell_order.amount, order.amount)
                trades.append(Trade(order.id, sell_order.id, min_amount, sell_order.price))
                order.amount -= min_amount
                if sell_order.amount == min_amount:
                    to_remove.append(index)
                else:
                    sell_order.amount -= min_amount
                index += 1
            else:
                if index+1 == len(self.sell_orders) or self.sell_orders[index+1].price > order.price:
                    min_amount = min(sell_order.amount, order.amount)
                    trades.append(Trade(order.id, sell_order.id, min_amount, sell_order.price))
                    order.amount -= min_amount
                    if sell_order.amount == min_amount:
                        to_remove.append(index)
                    else:
                        sell_order.amount -= min_amount
                        sell_order.display_size -= (min_amount % sell_order.display_size)
                    break
                else:
                    min_amount = min(sell_order.display_size, order.amount)
                    trades.append(Trade(order.id, sell_order.id, min_amount, sell_order.price))
                    order.amount -= min_amount
                    if sell_order.display_size == min_amount:
                        updated_order = sell_order
                        self.remove_sell_order(index)
                        updated_order.amount -= min_amount
                        updated_order.display_size = min(updated_order.amount, updated_order.display_size)
                        self.add_sell_order(updated_order)
                    else:
                        sell_order.amount -= min_amount
                        sell_order.display_size -= min_amount
            if order.amount == 0:
                break
        if order.amount > 0:
            if order.type == 'LO' or order.type == 'ICE':
                self.add_buy_order(order)
            if order.type == 'FOK':
                print(0)
                return
        if to_remove:
            self.remove_sell_orders(to_remove[0], to_remove[-1]+1)
        # Output total cost
        total = 0
        for t in trades:
            total += t.amount * t.price
        print(total)

    def process_sell(self, order):
        trades, to_remove = [], []
        index = n = len(self.buy_orders)
        if order.price == 0:
            index = 0
        elif n != 0 and self.buy_orders[0].price >= order.price:
            index = self.find_buy_order_match(order.price)
        while index < len(self.buy_orders):
            buy_order = self.buy_orders[index]
            if buy_order.price < order.price:
                break
            if buy_order.type != 'ICE':
                min_amount = min(buy_order.amount, order.amount)
                trades.append(Trade(order.id, buy_order.id, min_amount, buy_order.price))
                order.amount -= min_amount
                if buy_order.amount == min_amount:
                    to_remove.append(index)
                else:
                    buy_order.amount -= min_amount
                index += 1
            else:
                if index+1 == len(self.buy_orders) or self.buy_orders[index+1].price < order.price:
                    min_amount = min(buy_order.amount, order.amount)
                    trades.append(Trade(order.id, buy_order.id, min_amount, buy_order.price))
                    order.amount -= min_amount
                    if buy_order.amount == min_amount:
                        to_remove.append(index)
                    else:
                        buy_order.amount -= min_amount
                        buy_order.display_size -= (min_amount % buy_order.display_size)
                    break
                else:
                    min_amount = min(buy_order.display_size, order.amount)
                    trades.append(Trade(order.id, buy_order.id, min_amount, buy_order.price))
                    order.amount -= min_amount
                    if buy_order.display_size == min_amount:
                        updated_order = buy_order
                        self.remove_buy_order(index)
                        updated_order.amount -= min_amount
                        updated_order.display_size = min(updated_order.amount, updated_order.display_size)
                        self.add_buy_order(updated_order)
                    else:
                        buy_order.amount -= min_amount
                        buy_order.display_size -= min_amount
            if order.amount == 0:
                break
        if order.amount > 0:
            if order.type == 'LO' or order.type == 'ICE':
                self.add_sell_order(order)
            if order.type == 'FOK':
                print(0)
                return
        if to_remove:
            self.remove_buy_orders(to_remove[0], to_remove[-1]+1)
        # Output total cost
        total = 0
        for t in trades:
            total += t.amount * t.price
        print(total)
    
    def add_buy_order(self, order):
        index = self.find_buy_order(order.price)
        if index >= len(self.buy_orders):
            self.buy_orders.append(order)
            self.id_mapping[order.id] = (len(self.buy_orders)-1, 'B')
        else:
            self.buy_orders.insert(index, order)
            for i in range(index+1, len(self.buy_orders)):
                oid = self.buy_orders[i].id
                self.id_mapping[oid] = (self.id_mapping[oid][0]+1, self.id_mapping[oid][1])
            self.id_mapping[order.id] = (index, 'B')
    
    def add_sell_order(self, order):
        index = self.find_sell_order(order.price)
        if index >= len(self.sell_orders):
            self.sell_orders.append(order)
            self.id_mapping[order.id] = (len(self.sell_orders)-1, 'S')
        else:
            self.sell_orders.insert(index, order)
            for i in range(index+1, len(self.sell_orders)):
                oid = self.sell_orders[i].id
                self.id_mapping[oid] = (self.id_mapping[oid][0]+1, self.id_mapping[oid][1])
            self.id_mapping[order.id] = (index, 'S')
    
    def cancel_order(self, order_id):
        if order_id in self.id_mapping:
            idx, side = self.id_mapping[order_id]
            if side == 'S':
                self.remove_sell_order(idx)
            elif side == 'B':
                self.remove_buy_order(idx)
        # else:
        #     print('Could not find order for id: {}'.format(order_id))
    
    def cancel_and_replace_order(self, order_id, amount, price):
        if order_id not in self.id_mapping:
            return
        idx, side = self.id_mapping[order_id]
        if side == 'S':
            original_order = self.sell_orders[idx]
            if original_order.price == price and original_order.amount > amount:
                original_order.amount = amount
            else:
                updated_order = original_order
                self.remove_sell_order(idx)
                updated_order.amount = amount
                updated_order.price = price
                self.add_sell_order(updated_order)
        elif side == 'B':
            original_order = self.buy_orders[idx]
            if original_order.price == price and original_order.amount > amount:
                original_order.amount = amount
            else:
                updated_order = original_order
                self.remove_buy_order(idx)
                updated_order.amount = amount
                updated_order.price = price
                self.add_buy_order(updated_order)
            
    def remove_buy_order(self, index):
        order_id = self.buy_orders[index].id
        for i in range(index+1, len(self.buy_orders)):
            oid = self.buy_orders[i].id
            self.id_mapping[oid] = (self.id_mapping[oid][0]-1, self.id_mapping[oid][1])
        del self.buy_orders[index]
        del self.id_mapping[order_id]
    
    def remove_buy_orders(self, start, end):
        order_ids = [self.buy_orders[idx].id for idx in range(start, end)]
        for i in range(end, len(self.buy_orders)):
            oid = self.buy_orders[i].id
            self.id_mapping[oid] = (self.id_mapping[oid][0]-(end-start), self.id_mapping[oid][1])
        del self.buy_orders[start:end]
        for oid in order_ids:
            del self.id_mapping[oid]

    def remove_sell_order(self, index):
        order_id = self.sell_orders[index].id
        for i in range(index+1, len(self.sell_orders)):
            oid = self.sell_orders[i].id
            self.id_mapping[oid] = (self.id_mapping[oid][0]-1, self.id_mapping[oid][1])
        del self.sell_orders[index]
        del self.id_mapping[order_id]
    
    def remove_sell_orders(self, start, end):
        order_ids = [self.sell_orders[idx].id for idx in range(start, end)]
        for i in range(end, len(self.sell_orders)):
            oid = self.sell_orders[i].id
            self.id_mapping[oid] = (self.id_mapping[oid][0]-(end-start), self.id_mapping[oid][1])
        del self.sell_orders[start:end]
        for oid in order_ids:
            del self.id_mapping[oid]
    
    def find_sell_order(self, price):
        n = len(self.sell_orders)
        l, r, idx = 0, n-1, n
        while l <= r:
            mid = (l+r)//2
            # [1,2,3,4,5,5,6,7,7] insert 5
            if self.sell_orders[mid].price > price:
                idx = mid
                r = mid-1
            else:
                l = mid+1
        return idx

    def find_buy_order(self, price):
        n = len(self.buy_orders)
        l, r, idx = 0, n-1, n
        while l <= r:
            mid = (l+r)//2
            # [7,7,6,6,5,3,2,2,2,2,1] insert 5
            if self.buy_orders[mid].price < price:
                idx = mid
                r = mid-1
            else:
                l = mid+1
        return idx

    def find_sell_order_match(self, price):
        n = len(self.sell_orders)
        l, r, idx = 0, n-1, 0
        while l <= r:
            mid = (l+r)//2
            if self.sell_orders[mid].price <= price:
                idx = mid
                r = mid-1
            else:
                l = mid+1
        return idx

    def find_buy_order_match(self, price):
        n = len(self.buy_orders)
        l, r, idx = 0, n-1, 0
        while l <= r:
            mid = (l+r)//2
            if self.buy_orders[mid].price >= price:
                idx = mid
                r = mid-1
            else:
                l = mid+1
        return idx
        
# MAIN CODE EXECUTION
# Essentially the matching engine
order_book = OrderBook()
cmd = input()
count = 0
while cmd != 'END':
    # print(cmd)
    args = cmd.split(' ')
    if args[0] == 'SUB':
        price = -1 if args[1] == 'MO' else int(args[5])
        if args[1] == 'ICE':
            order = Order(int(args[4]), price, args[3], args[2], args[1], int(args[6]))
        else:
            order = Order(int(args[4]), price, args[3], args[2], args[1])
        order_book.process(order)
    elif args[0] == 'CXL':
        order_book.cancel_order(args[1])
    elif args[0] == 'CRP':
        order_book.cancel_and_replace_order(args[1], int(args[2]), int(args[3]))
    # if count >= 9:
    #     print('===============')
    #     print('CURRENT STATE')
    #     print('===============')
    #     print('B:', ' '.join([str(order) for order in order_book.buy_orders]))
    #     print('S:', ' '.join([str(order) for order in order_book.sell_orders]))
    cmd = input()
    count += 1

print('B:', ' '.join([str(order) for order in order_book.buy_orders]))
print('S:', ' '.join([str(order) for order in order_book.sell_orders]))


TEST CASE 8

SUB ICE B 8w3k 500 12 80
SUB FOK S k3ow 300 10
SUB FOK S 420c 250 10

TEST CASE 9

SUB ICE B Uo7Z 400 12 120
CRP Uo7Z 600 10
SUB LO S nmqX 90 12
SUB LO S rpDs 200 10

TEST CASE 10

SUB FOK B iUMF 434 977
CRP iUMF 425 977
SUB LO S SJZB 395 569
CRP iUMF 391 977
SUB MO S kdWj 440
CRP SJZB 686 765
CXL iUMF
CRP kdWj 517 459
SUB FOK B RrQj 270 71
SUB ICE S kCYM 982 313 762
CRP iUMF 13 977
CRP iUMF 229 977
SUB MO S RBgY 643
SUB LO B iAM8 34 641
CXL SJZB
SUB MO B DoiC 516
SUB MO B KMOK 304
SUB ICE S cdl1 784 437 559
CRP cdl1 482 437
SUB FOK S QDfw 374 345
SUB MO S VWKD 851
SUB LO B GSY2 277 294
SUB FOK B TRI1 531 803
SUB MO S G6H0 448
CRP iAM8 193 586
SUB MO B 2KIE 344
SUB IOC B qdzL 874 106
SUB FOK B PnSN 240 347
CXL 2KIE
CRP PnSN 183 347
CXL TRI1
SUB FOK S RI61 864 54
SUB FOK B TVMC 76 104
SUB MO S Xsc2 490
SUB ICE S SnN3 768 475 511
SUB ICE S HAbL 569 192 89
CXL SnN3
SUB ICE S OjSf 456 495 199
SUB IOC S q8QU 7 633
SUB MO S VnQ4 336
CRP RrQj 22 71
CRP q8QU 791 926
SUB LO B aA4S 26 613
SUB IOC S rAGT 538 533
SUB MO S oYiO 571
SUB IOC S oEnm 887 93
CXL TRI1
SUB ICE B sb8D 907 802 816
SUB ICE B kGOQ 101 889 99
SUB ICE B K32L 302 380 41
CRP VnQ4 458 875
SUB MO B GAn8 801
CRP RBgY 459 762

SUB IOC B E6oj 376 393
SUB MO S FYGB 632
CXL FYGB
SUB MO S Z5iW 782
SUB MO B iI4G 178
SUB LO S uCmN 723 914
CRP E6oj 181 393
SUB LO B NTQL 407 241
SUB FOK B Yy0e 47 402
SUB MO S iyye 325
SUB MO B gJXV 158
SUB IOC B tZAM 694 191
SUB ICE B uWk4 131 933 68
SUB ICE B 9Zlv 236 732 47
SUB LO S XZxE 615 919
SUB MO B O4FC 975
SUB LO B klAI 949 978
SUB ICE S WsPq 819 737 70
SUB ICE B W19V 881 609 737
CRP klAI 597 978
CRP FYGB 589 360
CRP 9Zlv 16 732
CRP WsPq 305 737
SUB ICE B OXzh 268 783 16
CXL WsPq
CXL W19V
SUB MO B FMQQ 910
CXL O4FC
CRP E6oj 218 393
CXL OXzh
SUB ICE B 7gsG 107 413 106
SUB IOC S Tkdm 726 61
SUB IOC B Z9bK 278 205
CRP iyye 352 378
CRP O4FC 856 104
CXL OXzh
SUB LO B m14U 430 314
SUB FOK S Q5Du 37 69
CRP uWk4 172 541
CRP E6oj 235 384
SUB FOK B VBnr 565 300
SUB IOC S mf3A 397 374
SUB LO S tXnh 277 752
SUB LO B EGyU 448 196
SUB MO B fZRG 240
CXL tXnh
SUB ICE B AWEQ 965 853 743
SUB IOC S jiDJ 896 833
SUB FOK S NjlW 99 529
SUB MO S q98j 127
CRP EGyU 87 144
SUB LO B S7JG 859 80
CXL Z9bK

1)

Time complexity
1. Searching for a match / insertion location takes O(log n) time
2. Searching for an order by ID takes O(1) time
3. Inserting an order into the orderbook buy_orders / sell_orders takes O(n) time (inserting into array + updating all index_mapping locations)
4. Cancelling / removing an order takes O(n) time (updating all index_mapping locations of subsequent elements)
5. Processing a new order (find match + iterate price <= / >= order.price + possible deletion + insertion) takes O(k*n) time, k depends on how much larger the order amount is than the display_size of the Iceberg orders.

Space complexity
The OrderBook object takes O(n) space, O(n) space is each required by the buy_orders, sell_orders and hashmap for the mapping of IDs to index positions.

More suitable data structure
Using a TreeMap (like in Java) for both buy_orders and sell_orders (+ hashmap to keep track of index mapping, index being the price) could have improved the time complexity. The TreeMap would use the price as the key. As multiple orders can be associated with a given price, the stored value is a LinkedList. This also improves the runtime for processing orders as deletion and appending to the end of a list (for Iceberg orders - main bottleneck) is O(1) for an LinkedList. Finding all values that are smaller  / larger than a given price is also achieved in O(log n). Cancelling orders will need to iterate through the list of orders with the same price.

2) 
Abstracting classes, strengths
My code defined classes for the orderbook, trades and orders. The orders could have been split into multiple order classes that inherit from an abstract order class, but I chose to stick with using an attirbute called type to discern between the different orders.

My code relies on maintaining a sorted python array (arraylist equivalent). The advantage is then that searching is relatively fast O(log n), and the functions to do the search for the right starting / insertion point are used quite frequently. Space complexity is also kept to a minimum. The main downside is that modifications (which are frequent) make the runtime O(n) at minimum. In the worst case (many iceberg orders), my code is too slow as the iceberg orders need to be frequently removed and reinserted.

Improve the design to make it more robust
Apart from opting for a different data structure (such as treemap), I would introduce more helper functions to refactor the process_sell / process_buy functions especially. The classes need to handle different cases based on the type of order that was received. Furthermore, opting for a different key - value data structure would help make the code more robust when a different algorithm is used for matching (i.e. pro rata instead of price time).

3)
Difficulties
The addition of the Iceberg order in part 3 was the main difficulty of the challenge. The iceberg orders could be fairly easily handled given the functions that I already had (remove / add orders), however the runtime is sub-optimal. The test cases 10 and 11 would not be able to pass due to TLE, test case 9 I went through manually and am not sure if there might be a bug with the test case (?).

I introduced an optimization in the case that an iceberg order is the last order that matches the order:
In such a case, the frequent deletion and reinsertion is not necessary and the updating of the order can be handled quickly. Realistically this can be expanded to optimize for the case that all remaining orders that still match are iceberg orders.