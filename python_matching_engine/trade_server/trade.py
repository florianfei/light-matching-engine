class Trade:
    def __init__(self, taker_id, maker_id, amount, price):
        self.taker_id = taker_id
        self.maker_id = maker_id
        self.amount = amount
        self.price = price