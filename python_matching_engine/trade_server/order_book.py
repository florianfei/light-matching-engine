from tkinter import N
from trade_server.trade import Trade

class OrderBookFIFO:
    def __init__(self):
        self.buy_orders = []
        self.sell_orders = []
        self.id_mapping = {}

    def process(self, order):
        if order.side == 'B':
            self.process_buy(order)
        elif order.side == 'S':
            self.process_sell(order)
        else:
            return False
    
    def process_buy(self, order):
        trades, to_remove = [], []
        index = n = len(self.sell_orders)
        # Market order price == 0
        # Limit order price > 0
        if order.price == 0:
            index = 0
        elif n != 0 and self.sell_orders[0].price <= order.price:
            index = self.find_sell_order_match(order.price)
        
        while index < n:
            sell_order = self.sell_orders[index]
            min_amount = min(sell_order.amount, order.amount)
            trades.append(Trade(order.id, sell_order.id, min_amount, sell_order.price))
            order.amount -= min_amount
            sell_order.amount -= min_amount
            if sell_order.amount == 0:
                to_remove.append(index)
            if order.amount == 0:
                break
            index += 1
        if order.amount > 0:
            self.add_buy_order(order)
        if to_remove:
            self.remove_sell_orders(to_remove[0], to_remove[-1]+1)
        return trades

    def process_sell(self, order):
        trades, to_remove = [], []
        index = n = len(self.buy_orders)
        if order.price == 0:
            index = 0
        elif n != 0 and self.buy_orders[0].price >= order.price:
            index = self.find_buy_order_match(order.price)
        while index < n:
            buy_order = self.buy_orders[index]
            min_amount = min(buy_order.amount, order.amount)
            trades.append(Trade(order.id, buy_order.id, min_amount, buy_order.price))
            order.amount -= min_amount
            buy_order.amount -= min_amount
            if buy_order.amount == 0:
                to_remove.append(index)
            if order.amount == 0:
                break
            index += 1
        if order.amount > 0:
            self.add_sell_order(order)
        if to_remove:
            self.remove_buy_orders(to_remove[0], to_remove[-1]+1)
        return trades
    
    def add_buy_order(self, order):
        index = self.find_buy_order(order.price)
        if index >= len(self.buy_orders):
            self.buy_orders.append(order)
            self.id_mapping[order.id] = (len(self.buy_orders)-1, 'B')
        else:
            self.buy_orders.insert(index, order)
            self.id_mapping[order.id] = (index, 'B')
    
    def add_sell_order(self, order):
        index = self.find_sell_order(order.price)
        if index >= len(self.sell_orders):
            self.sell_orders.append(order)
            self.id_mapping[order.id] = (len(self.sell_orders)-1, 'S')
        else:
            self.sell_orders.insert(index, order)
            self.id_mapping[order.id] = (index, 'S')
    
    def cancel_order(self, order_id):
        if order_id in self.id_mapping:
            idx, side = self.id_mapping[order_id]
            if side == 'S':
                self.remove_sell_order(idx)
            elif side == 'B':
                self.remove_buy_order(idx)
        else:
            print('Could not find order for id: {}'.format(order_id))
            
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
        del self.buy_order[start:end]
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

class OrderBookPR:
    def __init__(self):
        self.buy_orders = []
        self.sell_orders = []

    def add_buy_order(self, order):
        index = self.find_buy_order(order.price)
        self.buy_orders.insert(index, order)
    
    def add_sell_order(self, order):
        index = self.find_sell_order(order.price, order.amount)
        self.sell_orders.insert(index, order)
    
    def find_sell_order(self, price, amount):
        n = len(self.sell_orders)
        l, r, idx = 0, n-1, 0
        while l <= r:
            mid = (l+r)//2
            # [1,2,3,4,6,7,7] insert 5
            if self.sell_orders[mid].price >= price:
                idx = mid
                r = mid-1
            else:
                l = mid+1
        while idx-1 < n and self.sell_orders[idx].amount < amount:
            idx += 1
        return idx

    def find_buy_order(self, price, amount):
        n = len(self.buy_orders)
        l, r, idx = 0, n-1, 0
        while l <= r:
            mid = (l+r)//2
            # [7,7,6,6,5,3,2,2,2,2,1] insert 5
            if self.buy_orders[mid].price <= price:
                idx = mid
                r = mid-1
            else:
                l = mid+1
        while idx < n and self.buy_orders[idx].amount < amount:
            idx += 1
        return idx
    
    def find_sell_order_larger(self, price):
        n = len(self.sell_orders)
        l, r, idx = 0, n-1, 0
        while l <= r:
            mid = (l+r)//2
            # [1,2,3,4,5,5,6,7,7] insert 5
            if self.sell_orders[mid].price > price:
                idx = mid
                r = mid-1
            else:
                l = mid+1
        return idx

    def find_buy_order_smaller(self, price):
        n = len(self.buy_orders)
        l, r, idx = 0, n-1, 0
        while l <= r:
            mid = (l+r)//2
            # [7,7,6,6,5,3,2,2,2,2,1] insert 5
            if self.buy_orders[mid].price < price:
                idx = mid
                r = mid-1
            else:
                l = mid+1
        return idx
    
    def remove_buy_order(self, index):
        del self.buy_orders[index]

    def remove_sell_order(self, index):
        del self.sell_orders[index]

    def process(self, order):
        if order.side == 1:
            self.process_limit_buy(order)
        else:
            self.process_limit_sell(order)
    
    def process_limit_buy(self, order):
        # PRO RATA
        trades = []
        n = len(self.sell_orders)
        if n != 0 and self.sell_orders[n-1].price <= order.price:
            index = first = self.find_sell_order_larger(order.price)-1
            total_amount = 0

            while index >= 0 and self.sell_orders[index].price == order.price:
                total_amount += self.sell_orders[index].amount
                index -= 1

            to_remove = []
            
            if order.amount < total_amount:
                for i in range(index+1, first+1):
                    sell_order = self.sell_orders[i]
                    amt = round(total_amount * (sell_order.amount/total_amount))
                    if amt > 0:
                        trades.append(Trade(order.id, sell_order.id, amt, sell_order.price))
                        sell_order.amount -= amt
                        if sell_order.amount == 0:
                            to_remove.append(i)
                # TODO: Handle to_remove
                for i in range(len(to_remove)-1, -1, -1):
                    self.remove_sell_order(to_remove[i])
                return trades

            else:
                for i in range(index+1, first+1):
                    sell_order = self.sell_orders[i]
                    trades.append(Trade(order.id, sell_order.id, sell_order.amount, sell_order.price))
                del self.sell_orders[index+1:first+1]
                order.amount -= total_amount
        if order.amount:
            self.add_buy_order(order)
        return trades

    def process_limit_sell(self, order):
        # PRO RATA
        trades = []
        n = len(self.sell_orders)
        if n != 0 and self.sell_orders[n-1].price <= order.price:
            index = first = self.find_buy_order_smaller(order.price)-1
            total_amount = 0

            while index >= 0 and self.buy_orders[index].price == order.price:
                total_amount += self.buy_orders[index].amount
                index -= 1

            to_remove = []
            
            if order.amount < total_amount:
                for i in range(index+1, first+1):
                    buy_order = self.buy_orders[i]
                    amt = round(total_amount * (buy_order.amount/total_amount))
                    if amt > 0:
                        trades.append(Trade(order.id, buy_order.id, amt, buy_order.price))
                        buy_order.amount -= amt
                        if buy_order.amount == 0:
                            to_remove.append(i)
                # TODO: Handle to_remove
                for i in range(len(to_remove)-1, -1, -1):
                    self.remove_buy_order(to_remove[i])
                return trades

            else:
                for i in range(index+1, first+1):
                    buy_order = self.buy_orders[i]
                    trades.append(Trade(order.id, buy_order.id, buy_order.amount, buy_order.price))
                del self.buy_orders[index+1:first+1]
                order.amount -= total_amount
        if order.amount:
            self.add_sell_order(order)
        return trades