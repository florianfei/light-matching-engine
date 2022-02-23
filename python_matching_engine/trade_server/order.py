class Order:
    def __init__(self, amount, price, id, side):
        self.amount = amount
        self.price = price
        self.id = id
        self.side = side

    def __str__(self):
        return 'Order - price: {} amt: {} id: {} side: {}'.format(self.price, self.amount, self.id, self.side)